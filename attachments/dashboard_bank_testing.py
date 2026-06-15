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

# Set page config
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
    np.random.seed(42)
    n = 50000
    df = pd.DataFrame({
        'annual_income': np.random.lognormal(11.2, 0.5, n),
        'loan_amount': np.random.uniform(5000, 40000, n),
        'debt_to_income': np.random.uniform(5, 45, n),
        'fico_score': np.random.normal(700, 40, n).clip(300, 850),
        'revolving_utilization': np.random.uniform(0, 100, n),
        'protected_class': np.random.binomial(1, 0.25, n)
    })
    
    z = -4.5 + (df['debt_to_income']*0.04) + (df['revolving_utilization']*0.015) - ((df['fico_score']-600)*0.012) + (df['loan_amount']/df['annual_income'])
    df['default'] = np.random.binomial(1, 1 / (1 + np.exp(-z)))

    features = ['annual_income', 'loan_amount', 'debt_to_income', 'fico_score', 'revolving_utilization']
    X = df[features]
    y = df['default']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    test_protected = df.loc[X_test.index, 'protected_class']
    
    preprocessor = Pipeline([('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())])
    X_train_s = preprocessor.fit_transform(X_train)
    X_test_s = preprocessor.transform(X_test)
    
    champion = LogisticRegression(class_weight='balanced')
    champion.fit(X_train_s, y_train)
    champ_pd = champion.predict_proba(X_test_s)[:, 1]
    
    challenger = XGBClassifier(n_estimators=100, max_depth=3, scale_pos_weight=(len(y_train)-sum(y_train))/max(sum(y_train),1))
    challenger.fit(X_train_s, y_train)
    chall_pd = challenger.predict_proba(X_test_s)[:, 1]
    
    metrics = {
        'champ_auc': roc_auc_score(y_test, champ_pd),
        'chall_auc': roc_auc_score(y_test, chall_pd),
        'champ_ks': ks_2samp(champ_pd[y_test==1], champ_pd[y_test==0]).statistic,
        'chall_ks': ks_2samp(chall_pd[y_test==1], chall_pd[y_test==0]).statistic,
        'champ_brier': brier_score_loss(y_test, champ_pd),
        'avg_pd': champ_pd.mean()
    }
    
    explainer = shap.LinearExplainer(champion, X_train_s)
    return champion, preprocessor, explainer, features, metrics, X_train, y_test, champ_pd, test_protected, df

champion, preprocessor, explainer, feature_cols, metrics, X_train, y_test, champ_pd, test_protected, raw_df = build_enterprise_pipeline()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. CORE LOGIC
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def calculate_risk_pricing(pd_val, loan_amt):
    LGD = 0.45; EAD = loan_amt; expected_loss = pd_val * LGD * EAD
    apr = (0.05 + (pd_val * 1.5)) * 100
    return EAD, LGD, expected_loss, apr

def generate_adverse_action(shap_df):
    reason_map = {'debt_to_income': "High debt-to-income ratio.", 'fico_score': "Credit score low.", 
                  'revolving_utilization': "Elevated utilization.", 'loan_amount': "Loan amount disproportionate.", 
                  'annual_income': "Insufficient income."}
    top_risks = shap_df[shap_df['Impact'] > 0].head(3)
    return [reason_map.get(row['Feature'], "General risk factor") for _, row in top_risks.iterrows()]

def calculate_psi(expected, actual, buckets=10):
    breakpoints = np.percentile(expected, np.linspace(0, 100, buckets + 1))
    e_pct = np.histogram(expected, breakpoints)[0] / len(expected)
    a_pct = np.histogram(actual, breakpoints)[0] / len(actual)
    e_pct = np.where(e_pct == 0, 0.0001, e_pct); a_pct = np.where(a_pct == 0, 0.0001, a_pct)
    return np.sum((a_pct - e_pct) * np.log(a_pct / e_pct))

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. DASHBOARD UI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.title("🏦 Enterprise Credit Origination & MRM")
tabs = st.tabs(["Origination", "Portfolio Stress Test", "Model Governance", "Fair Lending", "Drift Monitoring", "Audit DB"])

with tabs[0]: # ORIGINATION
    with st.form("app_form"):
        c1, c2, c3 = st.columns(3)
        inc = c1.number_input("Annual Income ($)", value=85000); amt = c1.number_input("Loan Amount ($)", value=25000)
        dti = c2.number_input("Debt-to-Income (%)", value=35.0); fico = c2.number_input("FICO Score", value=640)
        util = c3.number_input("Revolving Util (%)", value=65.0); app_id = c3.text_input("Application ID", "APP-9942")
        submit = st.form_submit_button("Score", type="primary")
    if submit:
        scaled_input = preprocessor.transform([[inc, amt, dti, fico, util]])
        pd_val = champion.predict_proba(scaled_input)[0][1]; score = int(850 - (pd_val * 550))
        decision = "APPROVE" if score >= 620 else ("REVIEW" if score >= 550 else "DECLINE")
        EAD, LGD, EL, apr = calculate_risk_pricing(pd_val, amt)
        st.metric("Decision", decision); st.metric("Recommended APR", f"{apr:.2f}%")

with tabs[1]: # PORTFOLIO STRESS TEST (FIXED)
    scenario = st.selectbox("Scenario", ["Base Case", "Mild Recession", "Severe Recession"])
    mult = 1.0 if scenario == "Base Case" else (1.25 if "Mild" in scenario else 2.0)
    test_df = raw_df.loc[y_test.index]
    stressed_pds = np.clip(champ_pd * mult, 0, 0.99)
    total_el = np.sum(stressed_pds * 0.45 * test_df['loan_amount'].values)
    st.metric("Portfolio Expected Loss", f"${total_el:,.0f}")

with tabs[2]: # MODEL GOVERNANCE
    st.write(f"Champion AUC: {metrics['champ_auc']:.3f} | Challenger AUC: {metrics['chall_auc']:.3f}")

with tabs[3]: # FAIR LENDING
    decisions = np.where(champ_pd < 0.15, 1, 0)
    ref = decisions[test_protected == 0].mean(); prot = decisions[test_protected == 1].mean()
    st.metric("Adverse Impact Ratio", f"{(prot/ref):.3f}")

with tabs[4]: # PSI
    prod_df = raw_df.sample(frac=0.3)
    psi_val = calculate_psi(raw_df['fico_score'].values, prod_df['fico_score'].values)
    st.write(f"FICO PSI: {psi_val:.4f}")

with tabs[5]: # AUDIT
    conn = sqlite3.connect(DB_PATH)
    st.dataframe(pd.read_sql("SELECT * FROM scoring_log", conn))
    conn.close()
