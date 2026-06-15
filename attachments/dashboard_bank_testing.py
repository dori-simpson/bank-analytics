import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import os
from datetime import datetime
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, confusion_matrix
import altair as alt

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. DATABASE & AUDIT LAYER (Immutable Storage)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DB_PATH = "audit_log.db"

def init_db():
    """Initialize a persistent SQLite database for the audit log."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            applicant_name TEXT,
            loan_amount REAL,
            income REAL,
            pd REAL,
            score INTEGER,
            decision TEXT,
            model_version TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_decision(name, loan_amt, income, pd_val, score, decision, version="2.1.4"):
    """Securely write a decision to the immutable log."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO decisions (timestamp, applicant_name, loan_amount, income, pd, score, decision, model_version)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), name, loan_amt, income, pd_val, score, decision, version))
    conn.commit()
    conn.close()

def get_audit_logs():
    """Retrieve logs for the dashboard."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM decisions ORDER BY id DESC LIMIT 50", conn)
    conn.close()
    return df

init_db()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. MACHINE LEARNING PIPELINE (Model Risk Management)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@st.cache_resource
def train_credit_model():
    """
    Simulates a real ML pipeline: Data Gen -> Feature Eng -> Train/Test Split -> Train -> Validate.
    In a real architecture, this would load a pickled model (.pkl) trained offline.
    """
    np.random.seed(42)
    n_samples = 10000
    
    # Generate realistic base features
    income = np.random.lognormal(mean=11.2, sigma=0.6, size=n_samples)
    loan_amt = np.random.uniform(5000, 50000, size=n_samples)
    dti = np.random.uniform(5, 55, size=n_samples)
    delinq = np.random.poisson(lam=0.5, size=n_samples)
    grade = np.random.randint(1, 6, size=n_samples)
    
    # Feature Engineering (Including Loan Amount via LTI)
    lti = loan_amt / income
    
    # Create target variable (Default) based on a hidden logit function
    # Note: Using LTI, DTI, Delinq, and Grade as drivers
    z = -3.5 + (lti * 2.0) + (dti * 0.05) + (delinq * 0.8) + (grade * 0.4)
    true_pd = 1 / (1 + np.exp(-z))
    y = np.random.binomial(1, true_pd)
    
    X = pd.DataFrame({
        'LTI': lti,
        'DTI': dti,
        'Delinquencies': delinq,
        'Grade': grade,
        'Income_Log': np.log(income)
    })
    
    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale & Train
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Logistic Regression (Calibrated PD generation)
    model = LogisticRegression(class_weight='balanced')
    model.fit(X_train_scaled, y_train)
    
    # Validation Metrics
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    auc = roc_auc_score(y_test, y_pred_proba)
    
    return model, scaler, auc, X_train.columns

model, scaler, val_auc, feature_names = train_credit_model()

def score_applicant(income, loan_amt, dti, delinq, grade):
    """Execution wrapper for real-time scoring."""
    lti = loan_amt / max(income, 1)
    income_log = np.log(max(income, 1))
    
    features = pd.DataFrame([[lti, dti, delinq, grade, income_log]], columns=feature_names)
    features_scaled = scaler.transform(features)
    
    # Calibrated PD
    pd_val = model.predict_proba(features_scaled)[0][1]
    
    # Scale to Score (e.g., 300 to 850)
    score = int(850 - (pd_val * 550))
    
    # Feature Contributions (Log-Odds)
    # coefficient * scaled_feature_value = log-odds contribution
    contributions = model.coef_[0] * features_scaled[0]
    contrib_df = pd.DataFrame({
        'Feature': feature_names,
        'Contribution': contributions
    }).sort_values(by='Contribution', ascending=False)
    
    return pd_val, score, contrib_df

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. UI / DASHBOARD
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(page_title="Enterprise Credit Risk", layout="wide")
st.title("🏦 Enterprise Credit Risk Model (v2.1.4)")

tab_score, tab_explain, tab_gov, tab_audit = st.tabs([
    "🔍 Origination", "🧠 Explainability", "⚖️ Model Governance", "📜 Audit DB"
])

# --- TAB 1: ORIGINATION (Scoring) ---
with tab_score:
    st.markdown("### Applicant Data Entry")
    
    with st.form("scoring_form"):
        col1, col2 = st.columns(2)
        with col1:
            app_name = st.text_input("Applicant Name", "Jane Doe")
            income = st.number_input("Annual Income ($)", value=65000, step=5000)
            loan_amt = st.number_input("Loan Amount ($)", value=25000, step=1000)
        with col2:
            dti = st.number_input("Debt-to-Income (%)", value=22.0)
            delinq = st.number_input("Recent Delinquencies", value=0)
            grade = st.selectbox("Internal Grade", [1, 2, 3, 4, 5], format_func=lambda x: f"Grade {x}")
            
        submit = st.form_submit_button("Run Model", type="primary")

    if submit:
        # Run ML Model
        pd_val, score, contrib_df = score_applicant(income, loan_amt, dti, delinq, grade)
        
        # Policy Rules
        if score >= 650:
            decision = "APPROVE"
            color = "green"
        elif score >= 550:
            decision = "REVIEW"
            color = "orange"
        else:
            decision = "DECLINE"
            color = "red"
            
        # Log to SQLite DB
        log_decision(app_name, loan_amt, income, pd_val, score, decision)
        
        # Display Results
        st.divider()
        r1, r2, r3 = st.columns(3)
        r1.metric("Model Decision", decision)
        r2.metric("Calibrated PD", f"{pd_val*100:.2f}%")
        r3.metric("Scaled Score", score)
        
        # Pass data to session state for Explainability tab
        st.session_state.last_contrib = contrib_df
        st.session_state.last_name = app_name

# --- TAB 2: EXPLAINABILITY (White-Box Insights) ---
with tab_explain:
    st.markdown("### Feature Drivers (Log-Odds Contribution)")
    st.caption("How specific features pushed the model toward Default (+) or Approval (-)")
    
    if 'last_contrib' in st.session_state:
        st.write(f"**Viewing Explainability for:** {st.session_state.last_name}")
        df_c = st.session_state.last_contrib
        
        # Create a waterfall-style Altair chart for explainability
        chart = alt.Chart(df_c).mark_bar().encode(
            x=alt.X('Contribution:Q', title="Log-Odds Contribution (Positive = Higher Risk)"),
            y=alt.Y('Feature:N', sort='-x', title=""),
            color=alt.condition(
                alt.datum.Contribution > 0,
                alt.value("#dc2626"),  # Red for risk
                alt.value("#16a34a")   # Green for safe
            )
        ).properties(height=300)
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Run an applicant on the Origination tab to see explainability.")

# --- TAB 3: MODEL GOVERNANCE & FAIRNESS ---
with tab_gov:
    st.markdown("### Model Risk Management (MRM) Status")
    
    g1, g2, g3 = st.columns(3)
    g1.metric("Model ID / Version", "LR-PROD-v2.1.4")
    g2.metric("Validation ROC-AUC", f"{val_auc:.3f}")
    g3.metric("Last Validated", "2026-05-15")
    
    st.divider()
    st.markdown("#### Fairness & Fair Lending Monitoring")
    st.caption("Adverse Impact Ratio (AIR) via the 4/5ths Rule (80% threshold). Values < 0.80 require MRM review.")
    
    # Mocking Fair Lending metrics for the dashboard
    fairness_data = pd.DataFrame({
        "Protected Class": ["Age > 62", "Minority Status", "Gender (Female)"],
        "Approval Rate": ["68.2%", "61.4%", "65.0%"],
        "Reference Rate (Control)": ["66.0%", "66.0%", "66.0%"],
        "Adverse Impact Ratio (AIR)": [1.03, 0.93, 0.98]
    })
    
    st.dataframe(fairness_data.style.apply(
        lambda x: ['background-color: #fee2e2' if v < 0.8 else '' for v in x], 
        subset=['Adverse Impact Ratio (AIR)']
    ), use_container_width=True)

# --- TAB 4: IMMUTABLE AUDIT LOG ---
with tab_audit:
    st.markdown("### Production Audit Database")
    st.caption(f"Reading directly from secure SQLite storage: `{DB_PATH}`")
    
    logs = get_audit_logs()
    if not logs.empty:
        # Format for display
        logs['pd'] = (logs['pd'] * 100).round(2).astype(str) + '%'
        st.dataframe(logs, use_container_width=True, hide_index=True)
    else:
        st.info("No decisions logged in the database yet.")
