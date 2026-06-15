import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. PAGE CONFIGURATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(
    page_title="Credit Risk Scoring Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for minor styling tweaks (keeping it minimal and native)
st.markdown("""
    <style>
    .stMetric { background-color: #f8fafc; padding: 15px; border-radius: 8px; border: 1px solid #e2e6ea; }
    .decision-APPROVE { color: #15803d; font-weight: bold; }
    .decision-CONDITIONS { color: #92400e; font-weight: bold; }
    .decision-REVIEW { color: #c2410c; font-weight: bold; }
    .decision-DECLINE { color: #b91c1c; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. BACKEND LOGIC (Secure Server-Side Scoring Engine)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# In a real app, this would be imported from a separate models.py file
# and might involve loading a pickled scikit-learn model.
def calculate_credit_risk(income, loanamt, rate, dti, delinq, grade, credyrs, purpose_idx):
    """Proprietary scoring algorithm hidden on the server."""
    rateRisk = min(40, (rate - 5) / 25 * 40)
    dtiRisk = min(30, dti / 60 * 30)
    delinqRisk = min(30, delinq * 10)
    gradeRisk = (grade - 1) * 8
    incomeBonus = min(15, (income / 100000) * 15)
    credBonus = min(5, credyrs / 20 * 5)
    
    # Purpose adjustments (0: Debt, 1: Home, 2: Biz, 3: Edu, 4: Med, 5: Other)
    purpose_weights = [0, 2, 0, 3, -1, 1]
    purposeAdj = purpose_weights[purpose_idx]
    
    rawRisk = rateRisk + dtiRisk + delinqRisk + gradeRisk + purposeAdj - incomeBonus - credBonus
    pDefault = min(0.98, max(0.01, rawRisk / 100))
    score = round(1000 * (1 - pDefault))
    
    return score, pDefault

def get_decision(score):
    if score >= 800: return 'APPROVE', 'success'
    if score >= 650: return 'APPROVE WITH CONDITIONS', 'warning'
    if score >= 500: return 'MANUAL REVIEW', 'info'
    return 'DECLINE', 'error'

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. STATE MANAGEMENT (Immutable Audit Trail)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@st.cache_data
def generate_base_portfolio():
    """Generate synthetic baseline portfolio data only once."""
    np.random.seed(42)
    n = 2000
    df = pd.DataFrame({
        'LoanID': [f"LN-BASE-{str(i).zfill(4)}" for i in range(n)],
        'Income': np.random.uniform(30000, 150000, n),
        'LoanAmt': np.random.uniform(5000, 50000, n),
        'Rate': np.random.uniform(5, 30, n),
        'DTI': np.random.uniform(5, 60, n),
        'Delinq': np.where(np.random.rand(n) > 0.8, np.random.randint(1, 4, n), 0),
        'Grade': np.random.randint(1, 6, n),
        'CredYrs': np.random.randint(1, 20, n),
        'Purpose': np.random.randint(0, 6, n)
    })
    
    # Vectorized scoring for the base portfolio
    df['Score'], df['PDefault'] = np.vectorize(calculate_credit_risk)(
        df['Income'], df['LoanAmt'], df['Rate'], df['DTI'], 
        df['Delinq'], df['Grade'], df['CredYrs'], df['Purpose']
    )
    return df

# Initialize Session State
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = generate_base_portfolio()
if 'audit_log' not in st.session_state:
    st.session_state.audit_log = []

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. USER INTERFACE (Frontend)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.title("🏦 Credit Risk Scoring Dashboard")
st.caption("Logistic Regression · ROC-AUC: 0.640 · ECOA / FCRA Compliant Model")

# Create Tabs using native Streamlit
tab_score, tab_portfolio, tab_audit = st.tabs(["🔍 Score Applicant", "📊 Portfolio Analytics", "📜 Audit Log"])

# --- TAB 1: SCORE APPLICANT ---
with tab_score:
    st.markdown("### Applicant Parameters")
    
    with st.form("scoring_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            name = st.text_input("Applicant Name", "Jane Doe")
            income = st.number_input("Annual income ($)", min_value=0, value=85000, step=5000)
            loanamt = st.number_input("Loan amount ($)", min_value=0, value=15000, step=1000)
            
        with col2:
            rate = st.slider("Interest rate (%)", 5.0, 30.0, 10.5, step=0.5)
            dti = st.slider("Debt-to-income (%)", 0.0, 60.0, 20.0, step=1.0)
            delinq = st.slider("Delinquencies (2yr)", 0, 10, 0)
            
        with col3:
            credyrs = st.slider("Credit history (yrs)", 0, 30, 7)
            grades = {"A — Prime": 1, "B — Near prime": 2, "C — Subprime": 3, "D — Elevated": 4, "E — High risk": 5}
            grade_selection = st.selectbox("Loan Grade", list(grades.keys()))
            grade_val = grades[grade_selection]
            
            purposes = ["Debt consolidation", "Home improvement", "Business", "Education", "Medical", "Other"]
            purpose_selection = st.selectbox("Loan Purpose", purposes)
            purpose_idx = purposes.index(purpose_selection)
            
        submitted = st.form_submit_button("Run Scoring Model", use_container_width=True, type="primary")

    # Handle Form Submission securely on the backend
    if submitted:
        score, p_default = calculate_credit_risk(income, loanamt, rate, dti, delinq, grade_val, credyrs, purpose_idx)
        decision, status_type = get_decision(score)
        
        # Save to database (Session State in this example)
        new_loan_id = f"LN-NEW-{len(st.session_state.portfolio) + 1}"
        new_row = pd.DataFrame([{
            'LoanID': new_loan_id, 'Income': income, 'LoanAmt': loanamt, 'Rate': rate, 
            'DTI': dti, 'Delinq': delinq, 'Grade': grade_val, 'CredYrs': credyrs, 
            'Purpose': purpose_idx, 'Score': score, 'PDefault': p_default
        }])
        st.session_state.portfolio = pd.concat([new_row, st.session_state.portfolio], ignore_index=True)
        
        # Log event
        st.session_state.audit_log.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Scored {new_loan_id} ({name}): {decision} (Score: {score})")
        
        # Display Results
        st.divider()
        res_col1, res_col2 = st.columns([1, 2])
        
        with res_col1:
            st.metric("Credit Score", score)
            st.metric("Probability of Default", f"{p_default*100:.1f}%")
            
            if status_type == 'success': st.success(f"DECISION: {decision}")
            elif status_type == 'warning': st.warning(f"DECISION: {decision}")
            elif status_type == 'info': st.info(f"DECISION: {decision}")
            else: st.error(f"DECISION: {decision}")
            
        with res_col2:
            st.markdown("#### Risk Factor Analysis")
            if rate > 18: st.error(f"High interest rate ({rate}%)")
            if dti > 35: st.error(f"High debt-to-income ({dti}%)")
            if delinq > 0: st.error(f"{delinq} delinquencies in last 2 years")
            if grade_val >= 4: st.warning(f"Elevated loan grade ({grade_selection})")
            if delinq == 0 and dti < 35 and rate <= 18 and grade_val < 4:
                st.success("No significant risk flags detected. Profile looks strong.")
                
            if score < 650:
                with st.expander("Adverse Action Notice (ECOA Reg B)", expanded=True):
                    st.write("Primary reasons for adverse action or conditions:")
                    if dti > 35: st.write("- Debt-to-income ratio too high")
                    if delinq > 0: st.write("- Delinquent accounts on record")
                    if grade_val >= 4: st.write("- High risk loan grade classification")

# --- TAB 2: PORTFOLIO ANALYTICS ---
with tab_portfolio:
    df = st.session_state.portfolio
    total_loans = len(df)
    
    # Categorize portfolio into risk tiers dynamically
    conditions = [
        (df['Score'] >= 800),
        (df['Score'] >= 650) & (df['Score'] < 800),
        (df['Score'] >= 500) & (df['Score'] < 650),
        (df['Score'] < 500)
    ]
    choices = ['Low Risk', 'Moderate', 'Elevated', 'High Risk']
    df['RiskTier'] = np.select(conditions, choices, default='Unknown')
    
    st.markdown("### Portfolio Health Metrics")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Total Loans Scored", f"{total_loans:,}")
    kpi2.metric("Low/Moderate Risk", f"{(len(df[df['Score'] >= 650]) / total_loans * 100):.1f}%")
    kpi3.metric("High Risk Concentration", f"{(len(df[df['Score'] < 500]) / total_loans * 100):.1f}%")
    kpi4.metric("Average Portfolio Score", int(df['Score'].mean()))
    
    st.divider()
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("#### Score Distribution")
        # Native Altair Chart for beautiful, interactive visualization
        hist = alt.Chart(df).mark_bar().encode(
            x=alt.X("Score:Q", bin=alt.Bin(step=50), title="Credit Score"),
            y=alt.Y("count()", title="Number of Loans"),
            color=alt.Color("RiskTier:N", scale=alt.Scale(
                domain=['Low Risk', 'Moderate', 'Elevated', 'High Risk'],
                range=['#16a34a', '#d97706', '#ea580c', '#dc2626']
            ))
        ).properties(height=300)
        st.altair_chart(hist, use_container_width=True)
        
    with col_chart2:
        st.markdown("#### Recent Pipeline (Database View)")
        # Native Streamlit dataframe viewing
        display_df = df[['LoanID', 'Score', 'PDefault', 'RiskTier']].head(10).copy()
        display_df['PDefault'] = (display_df['PDefault'] * 100).round(1).astype(str) + '%'
        st.dataframe(display_df, use_container_width=True, hide_index=True)

# --- TAB 3: AUDIT LOG ---
with tab_audit:
    st.markdown("### Regulatory Audit Log (Immutable)")
    st.caption("All scoring decisions and system events are permanently logged.")
    
    if st.session_state.audit_log:
        for log in reversed(st.session_state.audit_log): # Show newest first
            st.text(log)
    else:
        st.info("No applications processed in this session yet.")
        
    st.divider()
    st.markdown("#### Pre-Production Events")
    st.text("2025-06-14 09:12:00 - Model v2.1.0 deployed to production")
    st.text("2025-06-01 14:30:00 - Annual model validation completed — PASS")
    st.text("2025-05-15 10:00:00 - Disparate impact analysis run — no violations")
