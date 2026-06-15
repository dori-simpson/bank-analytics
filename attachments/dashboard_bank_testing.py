import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime

# You were missing this specific import
from sklearn.pipeline import Pipeline 

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, brier_score_loss
from sklearn.calibration import calibration_curve
import altair as alt
# ==============================
# 1. PAGE CONFIG
# ==============================
st.set_page_config(page_title="MRM Engine", layout="wide", initial_sidebar_state="collapsed")

# ==============================
# 2. PERSISTENT AUDIT LAYER
# ==============================
def init_db():
    conn = sqlite3.connect("credit_audit.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS audit_log 
                 (id INTEGER PRIMARY KEY, ts TEXT, name TEXT, pd REAL, score INT, decision TEXT)""")
    conn.commit()
    conn.close()

# ==============================
# 3. ML PIPELINE (Optimized)
# ==============================
@st.cache_resource
def train_model():
    # Synthetic generator - replace with df = pd.read_csv(...)
    n = 10000
    income = np.random.lognormal(11, 0.5, n)
    loan = np.random.uniform(5000, 40000, n)
    dti = np.random.uniform(5, 50, n)
    z = -3 + 0.00002*income + 0.05*dti
    y = np.random.binomial(1, 1/(1+np.exp(-z)))
    X = pd.DataFrame({"inc": income, "loan": loan, "dti": dti})
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    pipe = Pipeline([('s', StandardScaler()), ('clf', LogisticRegression())])
    pipe.fit(X_train, y_train)
    return pipe, roc_auc_score(y_test, pipe.predict_proba(X_test)[:,1])

pipe, auc = train_model()

# ==============================
# 4. MOBILE-FRIENDLY UI
# ==============================
st.title("🏦 Credit Risk Decision Engine")

tab1, tab2, tab3 = st.tabs(["🔍 Origination", "📈 Governance", "📜 Audit"])

with tab1:
    with st.form("score_form"):
        # Automatically stacks on mobile
        col1, col2 = st.columns(2)
        name = col1.text_input("Applicant Name")
        inc = col1.number_input("Annual Income", 0, 500000, 75000)
        dti = col2.slider("DTI (%)", 0, 60, 25)
        loan = col2.number_input("Loan Amount", 0, 100000, 20000)
        
        if st.form_submit_button("Score Application", use_container_width=True):
            # Scoring Logic
            probs = pipe.predict_proba([[inc, loan, dti]])[0][1]
            score = int(850 - probs * 500)
            decision = "APPROVE" if score > 650 else "DECLINE"
            
            # Display results in mobile-friendly metric columns
            c1, c2, c3 = st.columns(3)
            c1.metric("Score", score)
            c2.metric("PD", f"{probs:.1%}")
            c3.metric("Decision", decision)

with tab2: # Governance Tab
    st.markdown("### Model Performance")
    st.metric("ROC-AUC Score", f"{auc:.3f}")
    
    # Calibration Curve (Altair is natively responsive)
    st.markdown("#### Probability Calibration")
    # ... Altair chart code ...

with tab3: # Audit Trail
    st.markdown("### Decision Log")
    st.dataframe(pd.read_sql("SELECT * FROM audit_log", sqlite3.connect("credit_audit.db")), use_container_width=True)
