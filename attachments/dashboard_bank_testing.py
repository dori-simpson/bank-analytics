import streamlit as st
import streamlit.components.v1 as components

# --- Page Configuration ---
st.set_page_config(
    page_title="Credit Risk Scoring Dashboard",
    page_icon="🏦",
    layout="wide"
)

# --- Python Engine Side Controls ---
# We render inputs in the native Streamlit sidebar to control the embedded view state
st.sidebar.header("Applicant Live Parameters")
income = st.sidebar.number_input("Annual income ($)", min_value=0, value=60000, step=5000)
loanamt = st.sidebar.number_input("Loan amount ($)", min_value=0, value=15000, step=1000)
rate = st.sidebar.slider("Interest rate (%)", min_value=5.0, max_value=30.0, value=13.0, step=0.5)
dti = st.sidebar.slider("Debt-to-income (%)", min_value=0, max_value=60, value=18)
delinq = st.sidebar.slider("Delinquencies (2yr)", min_value=0, max_value=10, value=0)

grade_options = {1: "A — Prime", 2: "B — Near prime", 3: "C — Subprime", 4: "D — Elevated", 5: "E — High risk"}
grade = st.sidebar.selectbox(
    "Loan grade", 
    options=list(grade_options.keys()), 
    format_func=lambda x: grade_options[x], 
    index=2
)

# --- Raw HTML Injection with Dynamic Sync ---
# We inject the original HTML code exactly as provided, but update the initial values
# and DOM interaction hooks to sync from Python's inputs on load.
html_code = f"""
<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css">
<style>
  /* --- Original Design Tokens & Variables Reset --- */
  :root {{
    --color-background-primary: #ffffff;
    --color-background-secondary: #f8f9fa;
    --color-border-tertiary: #dee2e6;
    --color-text-primary: #212529;
    --color-text-secondary: #6c757d;
    --color-background-info: #e6f1fb;
    --color-text-info: #185FA5;
    --border-radius-lg: 8px;
    --border-radius-md: 6px;
  }}

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 15px; background: transparent; color: var(--color-text-primary); }}

  /* --- Layout & Typography --- */
  .header {{ display: flex; align-items: center; gap: 12px; padding: 1.2rem 0 1rem; border-bottom: 0.5px solid var(--color-border-tertiary); margin-bottom: 1.2rem; }}
  .header-title {{ font-size: 18px; font-weight: 500; color: var(--color-text-primary); }}
  .header-sub {{ font-size: 12px; color: var(--color-text-secondary); margin-top: 2px; }}
  .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
  .card {{ background: var(--color-background-primary); border: 0.5px solid var(--color-border-tertiary); border-radius: var(--border-radius-lg); padding: 1rem 1.25rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
  .card-title {{ font-size: 13px; font-weight: 500; color: var(--color-text-secondary); margin-bottom: 12px; }}

  /* --- Metrics Grid --- */
  .metric-row {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin-bottom: 1.2rem; }}
  .metric-card {{ background: var(--color-background-secondary); border-radius: var(--border-radius-md); padding: 14px 12px; text-align: center; border: 0.5px solid var(--color-border-tertiary); }}
  .metric-value {{ font-size: 22px; font-weight: 500; color: var(--color-text-primary); }}
  .metric-label {{ font-size: 11px; color: var(--color-text-secondary); margin-top: 4px; }}

  /* --- Status Badges --- */
  .badge {{ display: inline-block; font-size: 10px; padding: 2px 8px; border-radius: 20px; font-weight: 500; text-transform: uppercase; }}
  .badge-green {{ background: #EAF3DE; color: #3B6D11; }}
  .badge-amber {{ background: #FAEEDA; color: #854F0B; }}
  .badge-red   {{ background: #FCEBEB; color: #A32D2D; }}
  .badge-blue  {{ background: #E6F1FB; color: #185FA5; }}

  /* --- Navigation Tabs --- */
  .tabs {{ display: flex; gap: 4px; margin-bottom: 1.2rem; border-bottom: 0.5px solid var(--color-border-tertiary); }}
  .tab {{ padding: 8px 16px; font-size: 13px; font-weight: 500; color: var(--color-text-secondary); cursor: pointer; border-bottom: 2px solid transparent; display: flex; align-items: center; gap: 6px; }}
  .tab.active {{ color: var(--color-text-primary); border-bottom-color: var(--color-text-primary); }}

  /* --- Panels --- */
  .panel {{ display: none; }}
  .panel.active {{ display: block; }}

  /* --- Calculator Fields --- */
  .form-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 16px; }}
  .field-group {{ display: flex; flex-direction: column; gap: 4px; }}
  .field-label {{ font-size: 11px; color: var(--color-text-secondary); }}
  input, select {{ width: 100%; padding: 6px 10px; border: 0.5px solid var(--color-border-tertiary); border-radius: 4px; font-size: 13px; background: var(--color-background-secondary); color: var(--color-text-primary); }}

  /* --- Visual Gauge Component --- */
  .gauge-wrap {{ margin: 1rem 0; }}
  .gauge-bar {{ width: 100%; height: 20px; border-radius: 4px; background: linear-gradient(to right, #E24B4A, #EF9F27, #4CAF50); position: relative; }}
  .gauge-marker {{ position: absolute; top: -4px; height: 28px; width: 3px; background: var(--color-text-primary); border-radius: 2px; transition: left 0.4s; }}
  .gauge-labels {{ display: flex; justify-content: space-between; font-size: 10px; color: var(--color-text-secondary); margin-top: 4px; }}

  /* --- Scoring Results Card --- */
  .result-box {{ border-radius: var(--border-radius-lg); padding: 1rem 1.25rem; text-align: center; margin-top: 12px; transition: all 0.3s ease; }}
  .result-score {{ font-size: 36px; font-weight: 500; }}
  .result-decision {{ font-size: 14px; font-weight: 500; margin-top: 4px; }}
  .result-prob {{ font-size: 12px; margin-top: 4px; opacity: 0.85; }}

  /* --- Benchmark Comparison Charts --- */
  .model-row {{ display: flex; align-items: center; gap: 10px; margin-bottom: 10px; font-size: 13px; }}
  .model-name {{ width: 140px; color: var(--color-text-primary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
  .bar-track {{ flex: 1; background: var(--color-background-secondary); border-radius: 4px; height: 8px; }}
  .bar-fill {{ height: 8px; border-radius: 4px; }}
  .auc-val {{ font-size: 12px; color: var(--color-text-secondary); width: 44px; text-align: right; }}
  .best-badge {{ font-size: 10px; padding: 1px 6px; background: var(--color-background-info); color: var(--color-text-info); border-radius: 20px; }}

  /* --- Portfolio breakdown tables --- */
  .tier-row {{ display: flex; align-items: center; justify-content: space-between; padding: 8px 0; border-bottom: 0.5px solid var(--color-border-tertiary); font-size: 13px; }}
  .tier-row:last-child {{ border-bottom: none; }}
  .tier-dot {{ width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }}
  button {{ padding: 8px 12px; border: none; background: #185FA5; color: white; border-radius: 4px; cursor: pointer; font-size: 13px; font-weight: 500; }}
  button:hover {{ background: #144f8a; }}
</style>
</head>
<body>

<div class="header">
  <i class="ti ti-building-bank" style="font-size: 28px; color: var(--color-text-primary);" aria-hidden="true"></i>
  <div>
    <div class="header-title">Credit Risk Scoring Dashboard</div>
    <div class="header-sub">
      Best model: Logistic Regression <span style="margin: 0 4px;">·</span> 
      ROC-AUC: 0.6400 <span style="margin: 0 4px;">·</span> 
      10,000 loan applications <span style="margin: 0 4px;">·</span> 
      1.78% default rate
    </div>
  </div>
</div>

<div class="metric-row">
  <div class="metric-card">
    <div class="metric-value" id="low-count-val">574</div>
    <div class="metric-label"><span class="badge badge-green">✓ LOW RISK</span></div>
  </div>
  <div class="metric-card">
    <div class="metric-value" id="mod-count-val">521</div>
    <div class="metric-label"><span class="badge badge-amber">⚠ MODERATE</span></div>
  </div>
  <div class="metric-card">
    <div class="metric-value" id="elev-count-val">389</div>
    <div class="metric-label"><span class="badge badge-red">~ ELEVATED</span></div>
  </div>
  <div class="metric-card">
    <div class="metric-value" id="high-count-val">516</div>
    <div class="metric-label"><span class="badge badge-red">✕ HIGH RISK</span></div>
  </div>
  <div class="metric-card">
    <div class="metric-value">0.640</div>
    <div class="metric-label"><span class="badge badge-blue">ROC-AUC</span></div>
  </div>
</div>

<div class="tabs">
  <div class="tab active" onclick="switchTab('score')">
    <i class="ti ti-search" aria-hidden="true"></i> Score applicant
  </div>
  <div class="tab" onclick="switchTab('portfolio')">
    <i class="ti ti-chart-pie" aria-hidden="true"></i> Portfolio analytics
  </div>
  <div class="tab" onclick="switchTab('models')">
    <i class="ti ti-chart-bar" aria-hidden="true"></i> Model performance
  </div>
</div>

<div id="panel-score" class="panel active">
  <div class="two-col">
    <div class="card">
      <div class="card-title"><i class="ti ti-user" aria-hidden="true"></i> Applicant details</div>
      
      <div class="form-grid">
        <div class="field-group">
          <div class="field-label">Annual income ($)</div>
          <input type="number" id="income" value="{income}" oninput="recalc()" />
        </div>
        
        <div class="field-group">
          <div class="field-label">Loan amount ($)</div>
          <input type="number" id="loanamt" value="{loanamt}" oninput="recalc()" />
        </div>
        
        <div class="field-group">
          <div class="field-label">Interest rate (%)</div>
          <input type="range" id="rate" min="5" max="30" step="0.5" value="{rate}" oninput="document.getElementById('rate-out').textContent=this.value+'%'; recalc()" />
          <span id="rate-out" style="font-size: 12px; color: var(--color-text-secondary);">{rate}%</span>
        </div>
        
        <div class="field-group">
          <div class="field-label">Debt-to-income (%)</div>
          <input type="range" id="dti" min="0" max="60" step="1" value="{dti}" oninput="document.getElementById('dti-out').textContent=this.value+'%'; recalc()" />
          <span id="dti-out" style="font-size: 12px; color: var(--color-text-secondary);">{dti}%</span>
        </div>
        
        <div class="field-group">
          <div class="field-label">Delinquencies (2yr)</div>
          <input type="range" id="delinq" min="0" max="10" step="1" value="{delinq}" oninput="document.getElementById('delinq-out').textContent=this.value; recalc()" />
          <span id="delinq-out" style="font-size: 12px; color: var(--color-text-secondary);">{delinq}</span>
        </div>
        
        <div class="field-group">
          <div class="field-label">Loan grade</div>
          <select id="grade" onchange="recalc()">
            <option value="1" {"selected" if grade==1 else ""}>A — Prime</option>
            <option value="2" {"selected" if grade==2 else ""}>B — Near prime</option>
            <option value="3" {"selected" if grade==3 else ""}>C — Subprime</option>
            <option value="4" {"selected" if grade==4 else ""}>D — Elevated</option>
            <option value="5" {"selected" if grade==5 else ""}>E — High risk</option>
          </select>
        </div>
      </div>

      <div class="gauge-wrap">
        <div class="gauge-bar">
          <div class="gauge-marker" id="gauge-marker" style="left: 75%"></div>
        </div>
        <div class="gauge-labels">
          <span>High risk (0)</span>
          <span>500</span>
          <span>650</span>
          <span>800</span>
          <span>Low risk (1000)</span>
        </div>
      </div>

      <div class="result-box" id="result-box">
        <div class="result-score" id="result-score">750</div>
        <div class="result-decision" id="result-decision">APPROVE WITH CONDITIONS</div>
        <div class="result-prob" id="result-prob">P(Default): 25.0%</div>
      </div>
    </div>

    <div>
      <div class="card" style="margin-bottom: 12px;">
        <div class="card-title"><i class="ti ti-flag" aria-hidden="true"></i> Risk factor analysis</div>
        <div id="risk-flags" style="font-size: 13px; line-height: 2;"></div>
      </div>
      
      <div class="card">
        <div class="card-title"><i class="ti ti-chart-bar" aria-hidden="true"></i> Default probability breakdown</div>
        <div style="position: relative; width: 100%; height: 160px;">
          <canvas id="barChart" role="img"></canvas>
        </div>
      </div>
    </div>
  </div>
</div>

<div id="panel-portfolio" class="panel">
  <div class="two-col">
    <div class="card">
      <div class="card-title">Risk tier breakdown</div>
      <div style="position: relative; width: 100%; height: 220px;">
        <canvas id="donutChart" role="img"></canvas>
      </div>
    </div>
    
    <div class="card">
      <div class="card-title">Tier details</div>
      <div class="tier-row">
        <div style="display: flex; align-items: center; gap: 8px;">
          <div class="tier-dot" style="background: #4CAF50;"></div>
          <span>Low risk</span>
        </div>
        <span style="color: var(--color-text-secondary);" id="low-count-lbl">574 loans</span>
        <span class="badge badge-green">Approve</span>
      </div>
      
      <div class="tier-row">
        <div style="display: flex; align-items: center; gap: 8px;">
          <div class="tier-dot" style="background: #FF9800;"></div>
          <span>Moderate risk</span>
        </div>
        <span style="color: var(--color-text-secondary);" id="mod-count-lbl">521 loans</span>
        <span class="badge badge-amber">Conditions</span>
      </div>
      
      <div class="tier-row">
        <div style="display: flex; align-items: center; gap: 8px;">
          <div class="tier-dot" style="background: #FF5722;"></div>
          <span>Elevated risk</span>
        </div>
        <span style="color: var(--color-text-secondary);" id="elev-count-lbl">389 loans</span>
        <span class="badge badge-amber">Review</span>
      </div>
      
      <div class="tier-row">
        <div style="display: flex; align-items: center; gap: 8px;">
          <div class="tier-dot" style="background: #F44336;"></div>
          <span>High risk</span>
        </div>
        <span style="color: var(--color-text-secondary);" id="high-count-lbl">516 loans</span>
        <span class="badge badge-red">Decline</span>
      </div>
      
      <div style="margin-top: 16px; padding-top: 12px; border-top: 0.5px solid var(--color-border-tertiary); font-size: 12px; color: var(--color-text-secondary);">
        <div style="margin-bottom: 4px;">Actual default rate: <b style="color: var(--color-text-primary);">1.78%</b></div>
        <div>Total scored: <b style="color: var(--color-text-primary);">2,000</b> (test set)</div>
      </div>
    </div>
  </div>
</div>

<div id="panel-models" class="panel">
  <div class="two-col">
    <div class="card">
      <div class="card-title">ROC-AUC benchmark</div>
      
      <div class="model-row">
        <div class="model-name">Logistic Regression <span class="best-badge">best</span></div>
        <div class="bar-track"><div class="bar-fill" style="width: 56%; background: #185FA5;"></div></div>
        <div class="auc-val">0.6400</div>
      </div>
      
      <div class="model-row">
        <div class="model-name">Random Forest</div>
        <div class="bar-track"><div class="bar-fill" style="width: 53%; background: #3B6D11;"></div></div>
        <div class="auc-val">0.6342</div>
      </div>
      
      <div class="model-row">
        <div class="model-name">XGBoost</div>
        <div class="bar-track"><div class="bar-fill" style="width: 49%; background: #993C1D;"></div></div>
        <div class="auc-val">0.5994</div>
      </div>
      
      <div style="margin-top: 14px; padding-top: 12px; border-top: 0.5px solid var(--color-border-tertiary); font-size: 12px; color: var(--color-text-secondary); line-height: 1.7;">
        <b style="color: var(--color-text-primary);">Note on AUC:</b> The dataset has only 178 defaults out of 10,000 loans (1.78%). With such extreme imbalance, the test set contains ~35 defaults, making ROC-AUC noisier. All models outperform random (0.5).
      </div>
    </div>
    
    <div class="card">
      <div class="card-title">Key metrics</div>
      <div class="tier-row"><span>Dataset size</span><b>10,000 loans</b></div>
      <div class="tier-row"><span>Train / test split</span><b>80% / 20%</b></div>
      <div class="tier-row"><span>Default rate</span><b>1.78%</b></div>
      <div class="tier-row"><span>Total defaults</span><b>178 loans</b></div>
      <div class="tier-row"><span>Primary metric</span><b>ROC-AUC</b></div>
      <div class="tier-row"><span>Imbalance handling</span><b>class weight balanced</b></div>
      <div class="tier-row"><span>Explainability</span><b>SHAP TreeExplainer</b></div>
      
      <div style="margin-top: 14px;">
        <button style="width: 100%;">
          Improve model AUC ↗
        </button>
      </div>
    </div>
  </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<script>
  let barChart;
  let donutChart;

  // Generate mock portfolio array
  const portfolioDatabase = [];
  Math.seedrandom = function(s) {{
    var mask = 0xffffffff, m_w = (123456789 + s) & mask, m_z = (987654321 - s) & mask;
    return function() {{
      m_z = (36969 * (m_z & 65535) + (m_z >> 16)) & mask;  m_w = (18000 * (m_w & 65535) + (m_w >> 16)) & mask;
      var result = ((m_z << 16) + m_w) >> 16; return (result & 0x7FFFFFFF) / 0x7FFFFFFF;
    }}
  }};
  const random = Math.seedrandom(42);

  for (let i = 0; i < 2000; i++) {{
    const mockRate = 5 + random() * 25;
    const mockDti = random() * 60;
    const mockDelinq = random() > 0.8 ? Math.floor(random() * 3) : 0;
    const mockGrade = Math.floor(1 + random() * 5);
    const mockIncome = 30000 + random() * 120000;
    
    const rRisk = Math.min(40, (mockRate - 5) / 25 * 40) + Math.min(30, mockDti / 60 * 30) + (mockDelinq * 15) + ((mockGrade - 1) * 8) - Math.min(15, (mockIncome / 100000) * 15);
    const pDef = Math.min(0.98, Math.max(0.01, rRisk / 100));
    const score = Math.round(1000 * (1 - pDef));
    
    portfolioDatabase.push({{ rate: mockRate, dti: mockDti, delinq: mockDelinq, grade: mockGrade, income: mockIncome, score: score }});
  }}

  function switchTab(name) {{
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
    const idx = ['score', 'portfolio', 'models'].indexOf(name);
    document.querySelectorAll('.tab')[idx].classList.add('active');
    document.getElementById('panel-' + name).classList.add('active');
  }}

  function initCharts() {{
    const ctxBar = document.getElementById('barChart').getContext('2d');
    barChart = new Chart(ctxBar, {{
      type: 'bar',
      data: {{
        labels: ['Interest rate', 'DTI', 'Delinquencies', 'Loan grade', 'Income'],
        datasets: [{{ label: 'Risk contribution', data: [0, 0, 0, 0, 0], backgroundColor: ['#E24B4A', '#EF9F27', '#E24B4A', '#BA7517', '#4CAF50'], borderRadius: 4 }}]
      }},
      options: {{ responsive: true, maintainAspectRatio: false, indexAxis: 'y', plugins: {{ legend: {{ display: false }} }}, scales: {{ x: {{ beginAtZero: true }}, y: {{ ticks: {{ font: {{ size: 11 }} }} }} }} }}
    }});

    const ctxDonut = document.getElementById('donutChart').getContext('2d');
    donutChart = new Chart(ctxDonut, {{
      type: 'doughnut',
      data: {{
        labels: ['Low risk', 'Moderate risk', 'Elevated risk', 'High risk'],
        datasets: [{{ data: [0, 0, 0, 0], backgroundColor: ['#4CAF50', '#FF9800', '#FF5722', '#F44336'], borderWidth: 2, borderColor: '#fff' }}]
      }},
      options: {{ responsive: true, maintainAspectRatio: false, cutout: '55%', plugins: {{ legend: {{ display: false }} }} }}
    }});
  }}

  function recalc() {{
    const income   = parseFloat(document.getElementById('income').value) || 60000;
    const loanamt  = parseFloat(document.getElementById('loanamt').value) || 15000;
    const rate     = parseFloat(document.getElementById('rate').value);
    const dti      = parseFloat(document.getElementById('dti').value);
    const delinq   = parseFloat(document.getElementById('delinq').value);
    const grade    = parseFloat(document.getElementById('grade').value);

    const rateRisk   = Math.min(40, (rate - 5) / 25 * 40);
    const dtiRisk    = Math.min(30, dti / 60 * 30);
    const delinqRisk = delinq * 15;
    const gradeRisk  = (grade - 1) * 8;
    const incomeBonus = Math.min(15, (income / 100000) * 15);
    
    const rawRisk = rateRisk + dtiRisk + delinqRisk + gradeRisk - incomeBonus;
    const pDefault = Math.min(0.98, Math.max(0.01, rawRisk / 100));
    const score = Math.round(1000 * (1 - pDefault));

    portfolioDatabase[0] = {{ rate, dti, delinq, grade, income, score }};

    const marker = document.getElementById('gauge-marker');
    marker.style.left = Math.min(97, Math.max(1, score / 10)) + '%';

    const rb = document.getElementById('result-box');
    const rs = document.getElementById('result-score');
    const rd = document.getElementById('result-decision');
    const rp = document.getElementById('result-prob');

    let bg, color, decision;
    if (score >= 800) {{ bg = '#EAF3DE'; color = '#3B6D11'; decision = 'APPROVE'; }}
    else if (score >= 650) {{ bg = '#FAEEDA'; color = '#854F0B'; decision = 'APPROVE WITH CONDITIONS'; }}
    else if (score >= 500) {{ bg = '#FAEEDA'; color = '#854F0B'; decision = 'MANUAL REVIEW'; }}
    else {{ bg = '#FCEBEB'; color = '#A32D2D'; decision = 'DECLINE'; }}

    rb.style.background = bg;
    rs.style.color = color; rs.textContent = score;
    rd.style.color = color; rd.textContent = decision;
    rp.style.color = color; rp.textContent = 'P(Default): ' + (pDefault * 100).toFixed(1) + '%';

    const flags = []; const goods = [];
    if (rate > 18) flags.push('<span style="color:#A32D2D">High interest rate (' + rate + '%)</span>');
    if (dti > 35)  flags.push('<span style="color:#A32D2D">High debt-to-income (' + dti + '%)</span>');
    if (delinq > 0) flags.push('<span style="color:#A32D2D">' + delinq + ' delinquencies in last 2 years</span>');
    if (grade >= 4) flags.push('<span style="color:#854F0B">Elevated loan grade (' + ["", "A", "B", "C", "D", "E"][grade] + ')</span>');
    if (delinq === 0) goods.push('<span style="color:#3B6D11">No recent delinquencies</span>');
    if (dti < 20)  goods.push('<span style="color:#3B6D11">Low debt-to-income ratio</span>');
    if (income > 80000) goods.push('<span style="color:#3B6D11">Strong income profile</span>');
    
    const all = [...flags, ...goods];
    document.getElementById('risk-flags').innerHTML = all.length ? all.join('<br>') : '<span style="color:#3B6D11">No significant risk flags</span>';

    let lowCount = 0, modCount = 0, elevCount = 0, highCount = 0;
    portfolioDatabase.forEach(loan => {{
      if (loan.score >= 800) lowCount++;
      else if (loan.score >= 650) modCount++;
      else if (loan.score >= 500) elevCount++;
      else highCount++;
    }});

    document.getElementById('low-count-val').textContent = lowCount;
    document.getElementById('mod-count-val').textContent = modCount;
    document.getElementById('elev-count-val').textContent = elevCount;
    document.getElementById('high-count-val').textContent = highCount;

    document.getElementById('low-count-lbl').textContent = lowCount + ' loans';
    document.getElementById('mod-count-lbl').textContent = modCount + ' loans';
    document.getElementById('elev-count-lbl').textContent = elevCount + ' loans';
    document.getElementById('high-count-lbl').textContent = highCount + ' loans';

    if (barChart) {{
      barChart.data.datasets[0].data = [Math.round(rateRisk), Math.round(dtiRisk), Math.round(delinqRisk), Math.round(gradeRisk), Math.round(incomeBonus)];
      barChart.data.datasets[0].backgroundColor = [rateRisk > 15 ? '#E24B4A' : '#4CAF50', dtiRisk > 15 ? '#E24B4A' : '#4CAF50', delinqRisk > 0 ? '#E24B4A' : '#4CAF50', gradeRisk > 20 ? '#E24B4A' : '#4CAF50', '#4CAF50'];
      barChart.update();
    }}
    if (donutChart) {{ donutChart.data.datasets[0].data = [lowCount, modCount, elevCount, highCount]; donutChart.update(); }}
  }}

  initCharts();
  recalc();
</script>
</body>
</html>
"""

# --- Component Injection ---
# We render your exact document within an insulated container passing the sidebar state tokens
components.html(html_code, height=650, scrolling=True)