import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, brier_score_loss, calibration_curve

import altair as alt

# ==============================
# PAGE CONFIG (mobile-friendly)
# ==============================
st.set_page_config(
    page_title="Credit Risk Decision Engine",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================
# PROFESSIONAL UI STYLING
# ==============================
st.markdown("""
<style>
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    .main-title {
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .sub-title {
        color: #6b7280;
        margin-bottom: 20px;
    }

    .card {
        padding: 16px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        background-color: #ffffff;
    }

    .metric-box {
        padding: 12px;
        border-radius: 10px;
        background: #f9fafb;
        border: 1px solid #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)

# ==============================
# DATABASE (AUDIT LAYER)
# ==============================
DB_PATH = "credit_audit.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            applicant TEXT,
            income REAL,
            loan_amt REAL,
            pd REAL,
            score INTEGER,
            decision TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_event(applicant, income, loan_amt, pd, score, decision):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO audit_log VALUES (NULL,?,?,?,?,?,?,?)
    """, (
        datetime.now().isoformat(),
        applicant,
        income,
        loan_amt,
        pd,
        score,
        decision
    ))
    conn.commit()
    conn.close()

def get_logs():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM audit_log ORDER BY id DESC LIMIT 100", conn)
    conn.close()
    return df

init_db()

# ==============================
# ML PIPELINE
# ==============================
@st.cache_resource
def train_model():
    np.random.seed(42)
    n = 12000

    income = np.random.lognormal(11, 0.5, n)
    loan = np.random.uniform(2000, 50000, n)
    dti = np.random.uniform(5, 60, n)
    delinq = np.random.poisson(0.5, n)

    lti = loan / income
    income_log = np.log(income)

    z = -3 + 2*lti + 0.05*dti + 0.8*delinq
    pd_true = 1 / (1 + np.exp(-z))
    y = np.random.binomial(1, pd_true)

    X = pd.DataFrame({
        "LTI": lti,
        "DTI": dti,
        "Delinq": delinq,
        "IncomeLog": income_log
    })

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    model = LogisticRegression(class_weight="balanced")
    model.fit(X_train_s, y_train)

    preds = model.predict_proba(X_test_s)[:, 1]

    auc = roc_auc_score(y_test, preds)
    brier = brier_score_loss(y_test, preds)

    return model, scaler, auc, brier, X.columns

model, scaler, auc, brier, FEATURES = train_model()

# ==============================
# SCORING ENGINE
# ==============================
def score_applicant(income, loan, dti, delinq):
    lti = loan / max(income, 1)
    income_log = np.log(max(income, 1))

    x = pd.DataFrame([[lti, dti, delinq, income_log]], columns=FEATURES)
    x_s = scaler.transform(x)

    pd_val = model.predict_proba(x_s)[0][1]
    score = int(850 - pd_val * 550)

    contrib = model.coef_[0] * x_s[0]

    return pd_val, score, contrib

def decision(score):
    if score >= 700:
        return "APPROVE", "#16a34a"
    elif score >= 600:
        return "REVIEW", "#f59e0b"
    return "DECLINE", "#dc2626"

# ==============================
# HEADER (mobile optimized)
# ==============================
st.markdown('<div class="main-title">🏦 Credit Risk Decision Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Real-time PD scoring · Audit logging · Model governance</div>', unsafe_allow_html=True)

# ==============================
# TABS
# ==============================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Origination",
    "🧠 Explainability",
    "📈 Model Governance",
    "📜 Audit Log"
])

# ==============================
# TAB 1 — ORIGINATION
# ==============================
with tab1:
    st.markdown("### Applicant Scoring")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Applicant Name", "John Doe")
        income = st.number_input("Income ($)", 1000, 500000, 75000)
        loan = st.number_input("Loan Amount ($)", 500, 100000, 20000)

    with col2:
        dti = st.slider("Debt-to-Income (%)", 0.0, 80.0, 25.0)
        delinq = st.slider("Delinquencies", 0, 10, 0)

    if st.button("Run Credit Decision", use_container_width=True):

        pd_val, score, contrib = score_applicant(income, loan, dti, delinq)
        decision_label, color = decision(score)

        log_event(name, income, loan, pd_val, score, decision_label)

        st.markdown("### Decision Result")

        c1, c2, c3 = st.columns(3)
        c1.metric("Decision", decision_label)
        c2.metric("PD", f"{pd_val*100:.2f}%")
        c3.metric("Score", score)

        st.markdown(
            f"<div style='padding:12px;border-radius:10px;background:{color};color:white;'>Risk Decision: {decision_label}</div>",
            unsafe_allow_html=True
        )

        st.session_state.contrib = contrib
        st.session_state.name = name

# ==============================
# TAB 2 — EXPLAINABILITY
# ==============================
with tab2:
    st.markdown("### Feature Impact (Log-Odds Approximation)")

    if "contrib" in st.session_state:
        dfc = pd.DataFrame({
            "Feature": FEATURES,
            "Impact": st.session_state.contrib
        })

        chart = alt.Chart(dfc).mark_bar().encode(
            x="Impact:Q",
            y=alt.Y("Feature:N", sort="-x"),
            color=alt.condition(
                alt.datum.Impact > 0,
                alt.value("#dc2626"),
                alt.value("#16a34a")
            )
        ).properties(height=350)

        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Run a decision first.")

# ==============================
# TAB 3 — GOVERNANCE
# ==============================
with tab3:
    st.markdown("### Model Performance")

    c1, c2 = st.columns(2)
    c1.metric("AUC", f"{auc:.3f}")
    c2.metric("Brier Score", f"{brier:.3f}")

    st.markdown("### Calibration Curve")

    # simple calibration demo
    y_true = np.random.randint(0, 2, 100)
    y_prob = np.linspace(0, 1, 100)

    frac_pos, mean_pred = calibration_curve(y_true, y_prob, n_bins=10)

    fig = alt.Chart(pd.DataFrame({
        "Pred": mean_pred,
        "Actual": frac_pos
    })).mark_line(point=True).encode(
        x="Pred",
        y="Actual"
    )

    st.altair_chart(fig, use_container_width=True)

# ==============================
# TAB 4 — AUDIT LOG
# ==============================
with tab4:
    st.markdown("### Audit Trail")

    df = get_logs()

    if not df.empty:
        df["pd"] = (df["pd"] * 100).round(2).astype(str) + "%"
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No records yet.")
