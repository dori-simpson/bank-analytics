import streamlit as st
import pandas as pd

# Basic page setup
st.set_page_config(page_title="Streamlit Credit Scorer", page_icon="🏦", layout="wide")

st.title("Credit Risk Scoring Dashboard")
st.subheader("Standard Streamlit Implementation (No Embedded HTML)")

# Create two columns
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("#### 🛠️ Applicant Parameters")
    
    # Python-based input widgets
    income = st.number_input("Annual income ($)", value=85000, step=5000)
    loanamt = st.number_input("Loan amount ($)", value=15000, step=1000)
    
    rate = st.slider("Interest rate (%)", 5.0, 30.0, 10.5, step=0.5)
    dti = st.slider("Debt-to-income (%)", 0, 60, 2)
    delinq = st.slider("Delinquencies (2yr)", 0, 10, 1)
    
    grade_map = {"A — Prime": 1, "B — Near prime": 2, "C — Subprime": 3, "D — Elevated": 4, "E — High risk": 5}
    grade_label = st.selectbox("Loan grade", list(grade_map.keys()))
    grade = grade_map[grade_label]
    
    credyrs = st.slider("Credit history (yrs)", 0, 30, 7)

# --- Python Calculation Logic ---
rateRisk = min(40, (rate - 5) / 25 * 40)
dtiRisk = min(30, dti / 60 * 30)
delinqRisk = min(30, delinq * 10)
gradeRisk = (grade - 1) * 8
incomeBonus = min(15, (income / 100000) * 15)
credBonus = min(5, credyrs / 20 * 5)

# Assuming no purpose input to match JS logic
rawRisk = rateRisk + dtiRisk + delinqRisk + gradeRisk - incomeBonus - credBonus
pDefault = min(0.98, max(0.01, rawRisk / 100))
score = round(1000 * (1 - pDefault))

with col2:
    st.markdown("#### 📊 Decision Result")
    
    # Display the metrics in standard Streamlit components
    st.metric(label="Credit Score", value=score)
    st.metric(label="Probability of Default", value=f"{(pDefault * 100):.1f}%")

    if score >= 800:
        st.success("Decision: APPROVE")
    elif score >= 650:
        st.warning("Decision: APPROVE WITH CONDITIONS")
    elif score >= 500:
        st.info("Decision: MANUAL REVIEW")
    else:
        st.error("Decision: DECLINE")
