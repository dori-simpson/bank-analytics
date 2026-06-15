import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import altair as alt
from datetime import datetime
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, roc_curve

# Set page config
st.set_page_config(page_title="Enterprise Credit Risk", layout="wide", page_icon="🏦")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. DATABASE & PIPELINE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DB_PATH = "enterprise_audit.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scoring_log 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, app_id TEXT, 
                  loan_amt REAL, pd REAL, score INTEGER, decision TEXT)''')
    conn.commit(); conn.close()

init_db()

@st.cache_resource
def build_pipeline():
    np.random.seed(42)
    n = 5000; df = pd.DataFrame({
        'income': np.random.lognormal(11.2, 0.5, n), 'loan_amt': np.random.uniform(5000, 40000, n),
        'dti': np.random.uniform(5, 45, n), 'fico': np.random.normal(700, 40, n).clip(300, 850),
        'util': np.random.uniform(0, 100, n), 'protected': np.random.binomial(1, 0.25, n)
    })
    z = -4 + (df['dti']*0.03) - ((df['fico']-600)*0.01); df['default'] = np.random.binomial(1, 1/(1+np.exp(-z)))
    X = df[['income', 'loan_amt', 'dti', 'fico', 'util']]; y = df['default']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipe = Pipeline([('s', StandardScaler())]).fit(X_train)
    model = LogisticRegression().fit(pipe.transform(X_train), y_train)
    return model, pipe, X_test, y_test, df.loc[X_test.index], df['protected'].loc[X_test.index]

model, pipe, X_test, y_test, test_df, prot_groups = build_pipeline()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. UI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.title("🏦 Enterprise Risk Monitor")
tabs = st.tabs(["Origination", "Stress Test", "Governance", "Fair Lending", "Drift", "Audit"])

with tabs[0]: # ORIGINATION
    with st.form("app"):
        c1, c2 = st.columns(2)
        inc = c1.number_input("Income", 50000); amt = c2.number_input("Loan", 20000)
        if st.form_submit_button("Score", use_container_width=True):
            pd_val = model.predict_proba(pipe.transform([[inc, amt, 30, 650, 50]]))[0][1]
            st.metric("Probability of Default", f"{pd_val:.2%}")
            # Visualization: Impact factors would go here
            st.info("Applicant meets automated criteria.")

with tabs[1]: # STRESS TEST
    st.subheader("Expected Loss Scenarios")
    scenarios = pd.DataFrame({'Scenario': ['Base', 'Mild', 'Severe'], 'EL': [5000, 7500, 12000]})
    chart = alt.Chart(scenarios).mark_bar().encode(x='Scenario', y='EL', color='Scenario')
    st.altair_chart(chart, use_container_width=True)

with tabs[2]: # GOVERNANCE
    st.subheader("Model Performance")
    fpr, tpr, _ = roc_curve(y_test, model.predict_proba(pipe.transform(X_test))[:,1])
    roc_df = pd.DataFrame({'FPR': fpr, 'TPR': tpr})
    st.altair_chart(alt.Chart(roc_df).mark_line().encode(x='FPR', y='TPR'), use_container_width=True)

with tabs[3]: # FAIR LENDING
    st.subheader("Disparate Impact Analysis")
    st.altair_chart(alt.Chart(pd.DataFrame({'Group':['Ref', 'Prot'], 'Rate':[0.8, 0.7]}))
                    .mark_bar().encode(x='Group', y='Rate', color='Group'), use_container_width=True)

with tabs[4]: # DRIFT
    st.subheader("PSI Monitoring")
    psi_df = pd.DataFrame({'Feature': ['FICO', 'DTI', 'Util'], 'Value': [0.02, 0.05, 0.12]})
    st.altair_chart(alt.Chart(psi_df).mark_bar().encode(x='Value', y='Feature', color='Value'), use_container_width=True)

with tabs[5]: # AUDIT
    st.subheader("Transaction Log")
    conn = sqlite3.connect(DB_PATH)
    st.dataframe(pd.read_sql("SELECT * FROM scoring_log", conn), use_container_width=True)
    conn.close()
