import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import altair as alt
from datetime import datetime

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve
from sklearn.pipeline import Pipeline

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="Enterprise Credit Risk",
    layout="wide",
    page_icon="🏦"
)

# ==============================
# DATABASE
# ==============================
DB_PATH = "enterprise_audit.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS scoring_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            app_id TEXT,
            loan_amt REAL,
            pd REAL,
            score INTEGER,
            decision TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

def log_score(app_id, loan_amt, pd_val, score, decision):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO scoring_log (timestamp, app_id, loan_amt, pd, score, decision)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        app_id,
        loan_amt,
        pd_val,
        score,
        decision
    ))
    conn.commit()
    conn.close()

# ==============================
# MODEL PIPELINE (FIXED)
# ==============================
@st.cache_resource
def build_pipeline():
    np.random.seed(42)
    n = 5000

    df = pd.DataFrame({
        "income": np.random.lognormal(11.2, 0.5, n),
        "loan_amt": np.random.uniform(5000, 40000, n),
        "dti": np.random.uniform(5, 45, n),
        "fico": np.random.normal(700, 40, n).clip(300, 850),
        "util": np.random.uniform(0, 100, n),
        "protected": np.random.binomial(1, 0.25, n)
    })

    # synthetic default
    z = -4 + (df["dti"] * 0.03) - ((df["fico"] - 600) * 0.01)
    df["default"] = np.random.binomial(1, 1 / (1 + np.exp(-z)))

    X = df[["income", "loan_amt", "dti", "fico", "util"]]
    y = df["default"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = Pipeline([
        ("scale", StandardScaler()),
        ("lr", LogisticRegression())
    ])

    model.fit(X_train, y_train)

    return model, X_test, y_test, df.loc[X_test.index], df.loc[X_test.index, "protected"]

model, X_test, y_test, test_df, protected = build_pipeline()

# ==============================
# PSI FUNCTION (REAL)
# ==============================
def psi(expected, actual, bins=10):
    breakpoints = np.percentile(expected, np.linspace(0, 100, bins + 1))
    expected_perc = np.histogram(expected, breakpoints)[0] / len(expected)
    actual_perc = np.histogram(actual, breakpoints)[0] / len(actual)

    expected_perc = np.where(expected_perc == 0, 0.0001, expected_perc)
    actual_perc = np.where(actual_perc == 0, 0.0001, actual_perc)

    return np.sum((actual_perc - expected_perc) * np.log(actual_perc / expected_perc))

# ==============================
# UI
# ==============================
st.title("🏦 Enterprise Risk Monitor (MRM Grade Upgrade)")

tabs = st.tabs([
    "Origination",
    "Stress Test",
    "Governance",
    "Fair Lending",
    "Drift",
    "Audit"
])

# ==============================
# ORIGINATION
# ==============================
with tabs[0]:
    with st.form("app"):
        c1, c2 = st.columns(2)

        inc = c1.number_input("Income", 50000, 300000, 80000)
        amt = c2.number_input("Loan Amount", 5000, 100000, 20000)
        dti = c1.slider("DTI", 0, 60, 30)
        fico = c2.slider("FICO", 300, 850, 680)

        submitted = st.form_submit_button("Score", use_container_width=True)

    if submitted:
        input_df = pd.DataFrame([[inc, amt, dti, fico, 50]],
                                columns=["income", "loan_amt", "dti", "fico", "util"])

        pd_val = model.predict_proba(input_df)[0][1]
        score = int(850 - pd_val * 550)

        decision = (
            "APPROVE" if score > 650 else
            "REVIEW" if score > 550 else
            "DECLINE"
        )

        log_score("APP-001", amt, pd_val, score, decision)

        st.metric("PD", f"{pd_val:.2%}")
        st.metric("Score", score)
        st.metric("Decision", decision)

# ==============================
# STRESS TEST
# ==============================
with tabs[1]:
    st.subheader("Expected Loss Scenarios")

    base_pd = model.predict_proba(X_test)[:, 1].mean()

    scenarios = pd.DataFrame({
        "Scenario": ["Base", "Mild", "Severe"],
        "EL": [
            base_pd * 0.45 * 10000,
            base_pd * 1.3 * 0.45 * 10000,
            base_pd * 2.0 * 0.45 * 10000
        ]
    })

    st.altair_chart(
        alt.Chart(scenarios)
        .mark_bar()
        .encode(x="Scenario", y="EL", color="Scenario"),
        use_container_width=True
    )

# ==============================
# GOVERNANCE
# ==============================
with tabs[2]:
    st.subheader("Model Performance")

    fpr, tpr, _ = roc_curve(y_test, model.predict_proba(X_test)[:, 1])

    roc_df = pd.DataFrame({"FPR": fpr, "TPR": tpr})

    st.altair_chart(
        alt.Chart(roc_df).mark_line()
        .encode(x="FPR", y="TPR"),
        use_container_width=True
    )

# ==============================
# FAIR LENDING
# ==============================
with tabs[3]:
    st.subheader("Disparate Impact")

    ref = model.predict_proba(test_df)[:, 1][protected == 0].mean()
    prot = model.predict_proba(test_df)[:, 1][protected == 1].mean()

    air = prot / ref if ref > 0 else 0

    st.metric("Reference PD", f"{ref:.2%}")
    st.metric("Protected PD", f"{prot:.2%}")
    st.metric("AIR", f"{air:.2f}")

# ==============================
# DRIFT (REAL PSI)
# ==============================
with tabs[4]:
    st.subheader("PSI Monitoring")

    prod = test_df.sample(frac=0.5, random_state=1)

    psi_vals = {
        "Income": psi(test_df["income"], prod["income"]),
        "DTI": psi(test_df["dti"], prod["dti"]),
        "FICO": psi(test_df["fico"], prod["fico"])
    }

    psi_df = pd.DataFrame({
        "Feature": list(psi_vals.keys()),
        "PSI": list(psi_vals.values())
    })

    st.altair_chart(
        alt.Chart(psi_df).mark_bar().encode(
            x="Feature",
            y="PSI",
            color="PSI"
        ),
        use_container_width=True
    )

# ==============================
# AUDIT
# ==============================
with tabs[5]:
    st.subheader("Audit Log")

    conn = sqlite3.connect(DB_PATH)
    logs = pd.read_sql("SELECT * FROM scoring_log ORDER BY id DESC", conn)
    conn.close()

    st.dataframe(logs, use_container_width=True)
