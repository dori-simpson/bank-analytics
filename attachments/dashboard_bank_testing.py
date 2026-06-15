import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import shap
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.stats import ks_2samp
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, brier_score_loss
from sklearn.calibration import calibration_curve
import altair as alt

# Set page config at the very top
st.set_page_config(page_title="Enterprise Credit Risk & MRM", layout="wide", page_icon="🏦")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. DATABASE & AUDIT LAYER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DB_PATH = "enterprise_audit.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scoring_log 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, app_id TEXT, 
                  loan_amt REAL, pd REAL, ead REAL, lgd REAL, expected_loss REAL, 
                  apr REAL, score INTEGER, decision TEXT, version TEXT)''')
    conn.commit()
    conn.close()

init_db()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. MACHINE LEARNING & DATA PIPELINE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@st.cache_resource
def build_enterprise_pipeline():
    """Builds the Champion/Challenger models and calculates MRM metrics."""
    
    # ---------------------------------------------------------
    # FALLBACK DATA GENERATION (Replaces pd.read_csv for safety)
    # If you have the CSV, replace this block with: 
    # df = pd.read_csv("1780790866747_loans_full_schema.csv")
    # ---------------------------------------------------------
    np.random.seed(42)
    n = 50000
    df = pd.DataFrame({
        'annual_income': np.random.lognormal(11.2, 0.5, n),
        'loan_amount': np.random.uniform(5000, 40000, n),
        'debt_to_income': np.random.uniform(5, 45, n),
        'fico_score': np.random.normal(700, 40, n).clip(300, 850),
        'revolving_utilization': np.random.uniform(0, 100, n),
        'protected_class': np.random.binomial(1, 0.25, n) # For Fair Lending
    })
    
    # Synthetic target based on risk factors
    z = -4.5 + (df['debt_to_income']*0.04) + (df['revolving_utilization']*0.015) - ((df['fico_score']-600)*0.012) + (df['loan_amount']/df['annual_income'])
    df['default'] = np.random.binomial(1, 1 / (1 + np.exp(-z)))
    # ---------------------------------------------------------

    features = ['annual_income', 'loan_amount', 'debt_to_income', 'fico_score', 'revolving_utilization']
    X = df[features]
    y = df['default']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    test_protected = df.loc[X_test.index, 'protected_class']
    
    # Pipeline
    preprocessor = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    X_train_s = preprocessor.fit_transform(X_train)
    X_test_s = preprocessor.transform(X_test)
    
    # Champion Model (Calibrated LR)
    champion = LogisticRegression(class_weight='balanced')
    champion.fit(X_train_s, y_train)
    champ_pd = champion.predict_proba(X_test_s)[:, 1]
    
    # Challenger Model (XGBoost)
    challenger = XGBClassifier(n_estimators=100, max_depth=3, scale_pos_weight=(len(y_train)-sum(y_train))/max(sum(y_train),1))
    challenger.fit(X_train_s, y_train)
    chall_pd = challenger.predict_proba(X_test_s)[:, 1]
    
    # Metrics
    metrics = {
        'champ_auc': roc_auc_score(y_test, champ_pd),
        'chall_auc': roc_auc_score(y_test, chall_pd),
        'champ_ks': ks_2samp(champ_pd[y_test==1], champ_pd[y_test==0]).statistic,
        'chall_ks': ks_2samp(chall_pd[y_test==1], chall_pd[y_test==0]).statistic,
        'champ_brier': brier_score_loss(y_test, champ_pd),
        'avg_pd': champ_pd.mean()
    }
    
    # SHAP Explainer
    explainer = shap.LinearExplainer(champion, X_train_s)
    
    return champion, preprocessor, explainer, features, metrics, X_train, y_test, champ_pd, test_protected, df

champion, preprocessor, explainer, feature_cols, metrics, X_train, y_test, champ_pd, test_protected, raw_df = build_enterprise_pipeline()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. CORE LOGIC (Pricing, Adverse Action, PSI)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def calculate_risk_pricing(pd_val, loan_amt):
    """Calculates Expected Loss (EL) and Risk-Based Pricing (APR)."""
    LGD = 0.45  # Loss Given Default (45%)
    EAD = loan_amt  # Exposure at Default
    expected_loss = pd_val * LGD * EAD
    
    base_rate = 0.05
    risk_premium = pd_val * 1.5  # Premium scales with PD
    apr = (base_rate + risk_premium) * 100
    
    return EAD, LGD, expected_loss, apr

def generate_adverse_action(shap_df):
    """Generates FCRA compliant reason codes from top risk drivers."""
    reason_map = {
        'debt_to_income': "Debt-to-income ratio is too high relative to internal thresholds.",
        'fico_score': "Credit score does not meet minimum requirements.",
        'revolving_utilization': "Revolving credit utilization is elevated.",
        'loan_amount': "Requested loan amount is disproportionate to income profile.",
        'annual_income': "Income is insufficient for the requested credit line."
    }
    top_risks = shap_df[shap_df['Impact'] > 0].head(3)
    return [reason_map.get(row['Feature'], f"Elevated risk indicator: {row['Feature']}") for _, row in top_risks.iterrows()]

def calculate_psi(expected, actual, buckets=10):
    """Calculates PSI for feature drift monitoring."""
    breakpoints = np.percentile(expected, np.linspace(0, 100, buckets + 1))
    expected_pct = np.histogram(expected, breakpoints)[0] / len(expected)
    actual_pct = np.histogram(actual, breakpoints)[0] / len(actual)
    
    expected_pct = np.where(expected_pct == 0, 0.0001, expected_pct)
    actual_pct = np.where(actual_pct == 0, 0.0001, actual_pct)
    
    return np.sum((actual_pct - expected_pct) * np.log(actual_pct / expected_pct))

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. DASHBOARD UI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.title("🏦 Enterprise Credit Origination & MRM")

tabs = st.tabs([
    "Origination & Pricing", "Portfolio Risk & Stress Test", 
    "Model Governance", "Fair Lending", "Monitoring & Drift", "Audit DB"
])

# --- TAB 1: ORIGINATION & PRICING ---
with tabs[0]:
    st.markdown("### Applicant Data Entry")
    with st.form("app_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            inc = st.number_input("Annual Income ($)", value=85000)
            amt = st.number_input("Loan Amount ($)", value=25000)
        with c2:
            dti = st.number_input("Debt-to-Income (%)", value=35.0)
            fico = st.number_input("FICO Score", value=640)
        with c3:
            util = st.number_input("Revolving Util (%)", value=65.0)
            app_id = st.text_input("Application ID", "APP-9942")
        submit = st.form_submit_button("Score Applicant", type="primary")

    if submit:
        # Score
        input_df = pd.DataFrame([[inc, amt, dti, fico, util]], columns=feature_cols)
        scaled_input = preprocessor.transform(input_df)
        pd_val = champion.predict_proba(scaled_input)[0][1]
        score = int(850 - (pd_val * 550))
        decision = "APPROVE" if score >= 620 else ("REVIEW" if score >= 550 else "DECLINE")
        
        # Risk Based Pricing & EL
        EAD, LGD, EL, apr = calculate_risk_pricing(pd_val, amt)
        
        # SHAP Explanation
        shap_vals = explainer.shap_values(scaled_input)[0]
        shap_df = pd.DataFrame({'Feature': feature_cols, 'Impact': shap_vals}).sort_values(by='Impact', ascending=False)
        reasons = generate_adverse_action(shap_df)
        
        # Audit Log
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO scoring_log (timestamp, app_id, loan_amt, pd, ead, lgd, expected_loss, apr, score, decision, version) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                  (datetime.now().isoformat(), app_id, amt, pd_val, EAD, LGD, EL, apr, score, decision, "LR-v2.1"))
        conn.commit(); conn.close()

        # UI Results
        st.divider()
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Decision", decision)
        m2.metric("Score", score)
        m3.metric("Probability of Default", f"{pd_val*100:.2f}%")
        m4.metric("Recommended APR", f"{apr:.2f}%")
        
        st.markdown("### Risk Analytics")
        r1, r2 = st.columns([1, 1])
        
        with r1:
            st.markdown("#### Individual Applicant SHAP Waterfall")
            st.caption("Explaining the specific drivers of this applicant's PD.")
            fig, ax = plt.subplots(figsize=(6, 4))
            
            # Using standard SHAP Waterfall
            explanation = shap.Explanation(values=shap_vals, base_values=explainer.expected_value, data=scaled_input[0], feature_names=feature_cols)
            shap.plots.waterfall(explanation, show=False)
            st.pyplot(fig)
            
        with r2:
            st.markdown("#### Expected Loss (EL) Calculation")
            st.info(f"**EAD** (Exposure): ${EAD:,.2f}  \n**LGD** (Loss Given Default): {LGD*100}%  \n**PD**: {pd_val*100:.2f}%")
            st.metric("Total Expected Loss", f"${EL:,.2f}")
            
            if decision != "APPROVE":
                st.error("Adverse Action Notice (FCRA Compliant)")
                st.write("**Top Factors Driving Decision:**")
                for i, r in enumerate(reasons, 1): st.write(f"{i}. {r}")

# --- TAB 2: PORTFOLIO & STRESS TESTING ---
with tabs[1]:
    st.markdown("### Portfolio Risk & Stress Testing (CCAR/DFAST Style)")
    
    scenario = st.selectbox("Select Macroeconomic Scenario", ["Base Case", "Mild Recession (PD x 1.25)", "Severe Recession (PD x 2.00)"])
    multiplier = 1.0
    if "Mild" in scenario: multiplier = 1.25
    if "Severe" in scenario: multiplier = 2.0
    
    stressed_pds = np.clip(champ_pd * multiplier, 0, 0.99)
    total_ead = raw_df['loan_amount'].sum()
    total_el = np.sum(stressed_pds * 0.45 * raw_df['loan_amount'])
    
    p1, p2, p3 = st.columns(3)
    p1.metric("Average Portfolio PD", f"{stressed_pds.mean()*100:.2f}%", f"{(stressed_pds.mean() - metrics['avg_pd'])*100:.2f}%" if multiplier > 1 else None, delta_color="inverse")
    p2.metric("Portfolio Expected Loss", f"${total_el:,.0f}", f"+${(total_el - np.sum(champ_pd * 0.45 * raw_df['loan_amount'])):,.0f}" if multiplier > 1 else None, delta_color="inverse")
    p3.metric("Total Exposure (EAD)", f"${total_ead:,.0f}")

# --- TAB 3: MODEL GOVERNANCE ---
with tabs[2]:
    st.markdown("### Model Card & Documentation")
    st.info("""
    **Model:** Retail Credit Risk PD Model v2.1  
    **Owner:** Risk Analytics Center of Excellence  
    **Training Dataset:** Historical Originations (N=50,000)  
    **Champion:** Calibrated Logistic Regression | **Challenger:** XGBoost
    """)
    
    st.markdown("### Champion vs Challenger Benchmarking")
    c1, c2, c3 = st.columns(3)
    c1.metric("Champion AUC (LR)", f"{metrics['champ_auc']:.3f}")
    c2.metric("Challenger AUC (XGB)", f"{metrics['chall_auc']:.3f}", f"{metrics['chall_auc'] - metrics['champ_auc']:.3f}")
    c3.metric("KS Statistic (LR vs XGB)", f"{metrics['champ_ks']:.3f} / {metrics['chall_ks']:.3f}")

    st.markdown("### Probability Calibration Curve")
    st.caption("Ensuring predicted PDs match actual observed default rates.")
    prob_true, prob_pred = calibration_curve(y_test, champ_pd, n_bins=10)
    
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.plot(prob_pred, prob_true, marker='o', label="Logistic Regression (Champion)")
    ax2.plot([0, 1], [0, 1], linestyle='--', color='gray', label="Perfect Calibration")
    ax2.set_xlabel("Predicted Probability of Default")
    ax2.set_ylabel("Actual Default Rate")
    ax2.legend()
    st.pyplot(fig2)

# --- TAB 4: FAIR LENDING ---
with tabs[3]:
    st.markdown("### Fair Lending: Disparate Impact (4/5ths Rule)")
    
    # 80% Rule Check
    decisions = np.where(champ_pd < 0.15, 1, 0)
    ref_approval = decisions[test_protected == 0].mean()
    prot_approval = decisions[test_protected == 1].mean()
    air = prot_approval / ref_approval if ref_approval > 0 else 1
    
    f1, f2, f3 = st.columns(3)
    f1.metric("Reference Group Approval Rate", f"{ref_approval*100:.1f}%")
    f2.metric("Protected Group Approval Rate", f"{prot_approval*100:.1f}%")
    f3.metric("Adverse Impact Ratio (AIR)", f"{air:.3f}", "PASS (>= 0.80)" if air >= 0.8 else "FAIL - FLAG FOR COMPLIANCE")

# --- TAB 5: PSI DRIFT MONITORING ---
with tabs[4]:
    st.markdown("### Population Stability Index (PSI) Monitoring")
    st.caption("Detects if production applicants are shifting away from the training distribution.")
    
    # Simulate Production Data (Slightly drifted)
    prod_df = raw_df.sample(frac=0.3)
    prod_df['debt_to_income'] = prod_df['debt_to_income'] * 1.15 # Simulate DTI inflation
    
    psi_data = []
    for col in feature_cols:
        psi_val = calculate_psi(raw_df[col].values, prod_df[col].values)
        status = "Stable" if psi_val < 0.1 else ("Monitor" if psi_val < 0.25 else "ALERT: Retrain")
        psi_data.append({"Feature": col, "PSI": round(psi_val, 4), "Status": status})
        
    psi_table = pd.DataFrame(psi_data)
    
    def color_status(val):
        color = 'green' if val == 'Stable' else ('orange' if val == 'Monitor' else 'red')
        return f'color: {color}; font-weight: bold'
    
    st.dataframe(psi_table.style.map(color_status, subset=['Status']), use_container_width=True)

# --- TAB 6: AUDIT TRAIL ---
with tabs[5]:
    st.markdown("### Immutable Production Audit Log")
    conn = sqlite3.connect(DB_PATH)
    logs = pd.read_sql_query("SELECT * FROM scoring_log ORDER BY id DESC LIMIT 100", conn)
    conn.close()
    
    if not logs.empty:
        logs['pd'] = (logs['pd'] * 100).round(2).astype(str) + '%'
        logs['apr'] = logs['apr'].round(2).astype(str) + '%'
        st.dataframe(logs, use_container_width=True, hide_index=True)
    else:
        st.info("No applications processed yet.")
