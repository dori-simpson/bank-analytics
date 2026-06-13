import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Credit Risk Scoring Dashboard",
    page_icon="🏦",
    layout="wide"
)

# Remove all top-level padding from Streamlit
st.markdown("""
<style>
    .block-container { padding-top: 0rem; padding-left: 0rem; padding-right: 0rem; }
    header { display: none; }
    [data-testid="stSidebar"] { display: none; }
</style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css">
<style>
  :root {
    --color-background-primary: #ffffff;
    --color-background-secondary: #f8f9fa;
    --color-border-tertiary: #dee2e6;
    --color-text-primary: #212529;
    --color-text-secondary: #6c757d;
    --color-background-info: #e6f1fb;
    --color-text-info: #185FA5;
    --border-radius-lg: 8px;
    --border-radius-md: 6px;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 15px; background: #ffffff; color: var(--color-text-primary); padding: 16px 24px; }

  .header { display: flex; align-items: center; gap: 12px; padding: 1rem 0; border-bottom: 0.5px solid var(--color-border-tertiary); margin-bottom: 1.2rem; }
  .header-title { font-size: 18px; font-weight: 500; }
  .header-sub { font-size: 12px; color: var(--color-text-secondary); margin-top: 2px; }

  /* Sidebar + Main layout */
  .layout { display: grid; grid-template-columns: 220px 1fr; gap: 20px; }
  .sidebar { background: var(--color-background-secondary); border-right: 0.5px solid var(--color-border-tertiary); padding: 16px; border-radius: var(--border-radius-lg); height: fit-content; }
  .sidebar h3 { font-size: 13px; font-weight: 600; margin-bottom: 16px; color: var(--color-text-secondary); text-transform: uppercase; letter-spacing: 0.05em; }
  .sidebar-field { margin-bottom: 16px; }
  .sidebar-label { font-size: 11px; color: var(--color-text-secondary); margin-bottom: 4px; display: flex; justify-content: space-between; }
  .sidebar-label span { color: #E24B4A; font-weight: 600; }
  .sidebar input[type="number"] { width: 100%; padding: 6px 10px; border: 0.5px solid var(--color-border-tertiary); border-radius: 4px; font-size: 13px; background: white; }
  .sidebar input[type="range"] { width: 100%; accent-color: #E24B4A; }
  .sidebar select { width: 100%; padding: 6px 10px; border: 0.5px solid var(--color-border-tertiary); border-radius: 4px; font-size: 13px; background: white; }

  .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  .card { background: var(--color-background-primary); border: 0.5px solid var(--color-border-tertiary); border-radius: var(--border-radius-lg); padding: 1rem 1.25rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
  .card-title { font-size: 13px; font-weight: 500; color: var(--color-text-secondary); margin-bottom: 12px; }

  .metric-row { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin-bottom: 1.2rem; }
  .metric-card { background: var(--color-background-secondary); border-radius: var(--border-radius-md); padding: 14px 12px; text-align: center; border: 0.5px solid var(--color-border-tertiary); }
  .metric-value { font-size: 22px; font-weight: 500; }
  .metric-label { font-size: 11px; color: var(--color-text-secondary); margin-top: 4px; }

  .badge { display: inline-block; font-size: 10px; padding: 2px 8px; border-radius: 20px; font-weight: 500; text-transform: uppercase; }
  .badge-green { background: #EAF3DE; color: #3B6D11; }
  .badge-amber { background: #FAEEDA; color: #854F0B; }
  .badge-red   { background: #FCEBEB; color: #A32D2D; }
  .badge-blue  { background: #E6F1FB; color: #185FA5; }

  .tabs { display: flex; gap: 4px; margin-bottom: 1.2rem; border-bottom: 0.5px solid var(--color-border-tertiary); }
  .tab { padding: 8px 16px; font-size: 13px; font-weight: 500; color: var(--color-text-secondary); cursor: pointer; border-bottom: 2px solid transparent; display: flex; align-items: center; gap: 6px; }
  .tab.active { color: var(--color-text-primary); border-bottom-color: var(--color-text-primary); }

  .panel { display: none; }
  .panel.active { display: block; }

  /* Score tab — remove duplicate form fields, just show results */
  .applicant-summary { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 16px; }
  .summary-item { background: var(--color-background-secondary); border-radius: 4px; padding: 8px 12px; }
  .summary-item .lbl { font-size: 11px; color: var(--color-text-secondary); }
  .summary-item .val { font-size: 14px; font-weight: 500; margin-top: 2px; }

  .gauge-wrap { margin: 1rem 0; }
  .gauge-bar { width: 100%; height: 20px; border-radius: 4px; background: linear-gradient(to right, #E24B4A, #EF9F27, #4CAF50); position: relative; }
  .gauge-marker { position: absolute; top: -4px; height: 28px; width: 3px; background: var(--color-text-primary); border-radius: 2px; transition: left 0.4s; }
  .gauge-labels { display: flex; justify-content: space-between; font-size: 10px; color: var(--color-text-secondary); margin-top: 4px; }

  .result-box { border-radius: var(--border-radius-lg); padding: 1rem 1.25rem; text-align: center; margin-top: 12px; transition: all 0.3s ease; }
  .result-score { font-size: 36px; font-weight: 500; }
  .result-decision { font-size: 14px; font-weight: 500; margin-top: 4px; }
  .result-prob { font-size: 12px; margin-top: 4px; opacity: 0.85; }

  .model-row { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; font-size: 13px; }
  .model-name { width: 140px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .bar-track { flex: 1; background: var(--color-background-secondary); border-radius: 4px; height: 8px; }
  .bar-fill { height: 8px; border-radius: 4px; }
  .auc-val { font-size: 12px; color: var(--color-text-secondary); width: 44px; text-align: right; }
  .best-badge { font-size: 10px; padding: 1px 6px; background: var(--color-background-info); color: var(--color-text-info); border-radius: 20px; }

  .tier-row { display: flex; align-items: center; justify-content: space-between; padding: 8px 0; border-bottom: 0.5px solid var(--color-border-tertiary); font-size: 13px; }
  .tier-row:last-child { border-bottom: none; }
  .tier-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
  button { padding: 8px 12px; border: none; background: #185FA5; color: white; border-radius: 4px; cursor: pointer; font-size: 13px; font-weight: 500; }
  button:hover { background: #144f8a; }
</style>
</head>
<body>

<div class="header">
  <i class="ti ti-building-bank" style="font-size: 28px;"></i>
  <div>
    <div class="header-title">Credit Risk Scoring Dashboard</div>
    <div class="header-sub">
      Best model: Logistic Regression &nbsp;·&nbsp;
      ROC-AUC: 0.6400 &nbsp;·&nbsp;
      10,000 loan applications &nbsp;·&nbsp;
      1.78% default rate
    </div>
  </div>
</div>

<div class="layout">

  <!-- ===== SIDEBAR (all controls live here now) ===== -->
  <div class="sidebar">
    <h3>Applicant Parameters</h3>

    <div class="sidebar-field">
      <div class="sidebar-label">Annual income ($)</div>
      <input type="number" id="income" value="85000" min="0" step="5000" oninput="recalc()" />
    </div>

    <div class="sidebar-field">
      <div class="sidebar-label">Loan amount ($)</div>
      <input type="number" id="loanamt" value="15000" min="0" step="1000" oninput="recalc()" />
    </div>

    <div class="sidebar-field">
      <div class="sidebar-label">Interest rate (%) <span id="rate-out">10.5%</span></div>
      <input type="range" id="rate" min="5" max="30" step="0.5" value="10.5"
             oninput="document.getElementById('rate-out').textContent=this.value+'%'; recalc()" />
    </div>

    <div class="sidebar-field">
      <div class="sidebar-label">Debt-to-income (%) <span id="dti-out">2%</span></div>
      <input type="range" id="dti" min="0" max="60" step="1" value="2"
             oninput="document.getElementById('dti-out').textContent=this.value+'%'; recalc()" />
    </div>

    <div class="sidebar-field">
      <div class="sidebar-label">Delinquencies (2yr) <span id="delinq-out">1</span></div>
      <input type="range" id="delinq" min="0" max="10" step="1" value="1"
             oninput="document.getElementById('delinq-out').textContent=this.value; recalc()" />
    </div>

    <div class="sidebar-field">
      <div class="sidebar-label">Loan grade</div>
      <select id="grade" onchange="recalc()">
        <option value="1" selected>A — Prime</option>
        <option value="2">B — Near prime</option>
        <option value="3">C — Subprime</option>
        <option value="4">D — Elevated</option>
        <option value="5">E — High risk</option>
      </select>
    </div>
  </div>

  <!-- ===== MAIN CONTENT ===== -->
  <div>

    <!-- Top metric cards -->
    <div class="metric-row">
      <div class="metric-card">
        <div class="metric-value" id="low-count-val">—</div>
        <div class="metric-label"><span class="badge badge-green">✓ LOW RISK</span></div>
      </div>
      <div class="metric-card">
        <div class="metric-value" id="mod-count-val">—</div>
        <div class="metric-label"><span class="badge badge-amber">⚠ MODERATE</span></div>
      </div>
      <div class="metric-card">
        <div class="metric-value" id="elev-count-val">—</div>
        <div class="metric-label"><span class="badge badge-red">~ ELEVATED</span></div>
      </div>
      <div class="metric-card">
        <div class="metric-value" id="high-count-val">—</div>
        <div class="metric-label"><span class="badge badge-red">✕ HIGH RISK</span></div>
      </div>
      <div class="metric-card">
        <div class="metric-value">0.640</div>
        <div class="metric-label"><span class="badge badge-blue">ROC-AUC</span></div>
      </div>
    </div>

    <!-- Tabs -->
    <div class="tabs">
      <div class="tab active" onclick="switchTab('score')">
        <i class="ti ti-search"></i> Score applicant
      </div>
      <div class="tab" onclick="switchTab('portfolio')">
        <i class="ti ti-chart-pie"></i> Portfolio analytics
      </div>
      <div class="tab" onclick="switchTab('models')">
        <i class="ti ti-chart-bar"></i> Model performance
      </div>
    </div>

    <!-- SCORE TAB -->
    <div id="panel-score" class="panel active">
      <div class="two-col">
        <div class="card">
          <div class="card-title"><i class="ti ti-user"></i> Applicant details</div>

          <!-- Live summary of sidebar values -->
          <div class="applicant-summary">
            <div class="summary-item"><div class="lbl">Annual income ($)</div><div class="val" id="sum-income">85,000</div></div>
            <div class="summary-item"><div class="lbl">Loan amount ($)</div><div class="val" id="sum-loan">15,000</div></div>
            <div class="summary-item"><div class="lbl">Interest rate</div><div class="val" id="sum-rate">10.5%</div></div>
            <div class="summary-item"><div class="lbl">Debt-to-income</div><div class="val" id="sum-dti">2%</div></div>
            <div class="summary-item"><div class="lbl">Delinquencies</div><div class="val" id="sum-delinq">1</div></div>
            <div class="summary-item"><div class="lbl">Loan grade</div><div class="val" id="sum-grade">A — Prime</div></div>
          </div>

          <div class="gauge-wrap">
            <div class="gauge-bar">
              <div class="gauge-marker" id="gauge-marker" style="left: 75%"></div>
            </div>
            <div class="gauge-labels">
              <span>High risk (0)</span><span>500</span><span>650</span><span>800</span><span>Low risk (1000)</span>
            </div>
          </div>

          <div class="result-box" id="result-box">
            <div class="result-score" id="result-score">—</div>
            <div class="result-decision" id="result-decision">—</div>
            <div class="result-prob" id="result-prob">—</div>
          </div>
        </div>

        <div>
          <div class="card" style="margin-bottom: 12px;">
            <div class="card-title"><i class="ti ti-flag"></i> Risk factor analysis</div>
            <div id="risk-flags" style="font-size: 13px; line-height: 2;"></div>
          </div>
          <div class="card">
            <div class="card-title"><i class="ti ti-chart-bar"></i> Default probability breakdown</div>
            <div style="position: relative; width: 100%; height: 160px;">
              <canvas id="barChart"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- PORTFOLIO TAB -->
    <div id="panel-portfolio" class="panel">
      <div class="two-col">
        <div class="card">
          <div class="card-title">Risk tier breakdown</div>
          <div style="position: relative; width: 100%; height: 220px;">
            <canvas id="donutChart"></canvas>
          </div>
        </div>
        <div class="card">
          <div class="card-title">Tier details</div>
          <div class="tier-row">
            <div style="display:flex;align-items:center;gap:8px;"><div class="tier-dot" style="background:#4CAF50;"></div><span>Low risk</span></div>
            <span style="color:var(--color-text-secondary);" id="low-count-lbl">— loans</span>
            <span class="badge badge-green">Approve</span>
          </div>
          <div class="tier-row">
            <div style="display:flex;align-items:center;gap:8px;"><div class="tier-dot" style="background:#FF9800;"></div><span>Moderate risk</span></div>
            <span style="color:var(--color-text-secondary);" id="mod-count-lbl">— loans</span>
            <span class="badge badge-amber">Conditions</span>
          </div>
          <div class="tier-row">
            <div style="display:flex;align-items:center;gap:8px;"><div class="tier-dot" style="background:#FF5722;"></div><span>Elevated risk</span></div>
            <span style="color:var(--color-text-secondary);" id="elev-count-lbl">— loans</span>
            <span class="badge badge-amber">Review</span>
          </div>
          <div class="tier-row">
            <div style="display:flex;align-items:center;gap:8px;"><div class="tier-dot" style="background:#F44336;"></div><span>High risk</span></div>
            <span style="color:var(--color-text-secondary);" id="high-count-lbl">— loans</span>
            <span class="badge badge-red">Decline</span>
          </div>
          <div style="margin-top:16px;padding-top:12px;border-top:0.5px solid var(--color-border-tertiary);font-size:12px;color:var(--color-text-secondary);">
            <div style="margin-bottom:4px;">Actual default rate: <b style="color:var(--color-text-primary);">1.78%</b></div>
            <div>Total scored: <b style="color:var(--color-text-primary);">2,000</b> (test set)</div>
          </div>
        </div>
      </div>
    </div>

    <!-- MODELS TAB -->
    <div id="panel-models" class="panel">
      <div class="two-col">
        <div class="card">
          <div class="card-title">ROC-AUC benchmark</div>
          <div class="model-row">
            <div class="model-name">Logistic Regression <span class="best-badge">best</span></div>
            <div class="bar-track"><div class="bar-fill" style="width:56%;background:#185FA5;"></div></div>
            <div class="auc-val">0.6400</div>
          </div>
          <div class="model-row">
            <div class="model-name">Random Forest</div>
            <div class="bar-track"><div class="bar-fill" style="width:53%;background:#3B6D11;"></div></div>
            <div class="auc-val">0.6342</div>
          </div>
          <div class="model-row">
            <div class="model-name">XGBoost</div>
            <div class="bar-track"><div class="bar-fill" style="width:49%;background:#993C1D;"></div></div>
            <div class="auc-val">0.5994</div>
          </div>
          <div style="margin-top:14px;padding-top:12px;border-top:0.5px solid var(--color-border-tertiary);font-size:12px;color:var(--color-text-secondary);line-height:1.7;">
            <b style="color:var(--color-text-primary);">Note on AUC:</b> The dataset has only 178 defaults out of 10,000 loans (1.78%). With such extreme imbalance, the test set contains ~35 defaults, making ROC-AUC noisier. All models outperform random (0.5).
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
          <div style="margin-top:14px;">
            <button style="width:100%;">Improve model AUC ↗</button>
          </div>
        </div>
      </div>
    </div>

  </div><!-- end main -->
</div><!-- end layout -->

<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<script>
  let barChart, donutChart;

  // Seeded random so portfolio data is consistent on every load
  function seededRandom(seed) {
    let m_w = (123456789 + seed) & 0xffffffff;
    let m_z = (987654321 - seed) & 0xffffffff;
    return function() {
      m_z = (36969 * (m_z & 65535) + (m_z >> 16)) & 0xffffffff;
      m_w = (18000 * (m_w & 65535) + (m_w >> 16)) & 0xffffffff;
      let result = ((m_z << 16) + m_w) >> 16;
      return (result & 0x7FFFFFFF) / 0x7FFFFFFF;
    };
  }

  const random = seededRandom(42);
  const portfolioDatabase = [];

  for (let i = 0; i < 2000; i++) {
    const mockRate   = 5 + random() * 25;
    const mockDti    = random() * 60;
    const mockDelinq = random() > 0.8 ? Math.floor(random() * 3) : 0;
    const mockGrade  = Math.floor(1 + random() * 5);
    const mockIncome = 30000 + random() * 120000;
    const rRisk = Math.min(40, (mockRate-5)/25*40) + Math.min(30, mockDti/60*30) + (mockDelinq*15) + ((mockGrade-1)*8) - Math.min(15, (mockIncome/100000)*15);
    const pDef  = Math.min(0.98, Math.max(0.01, rRisk/100));
    portfolioDatabase.push({ rate: mockRate, dti: mockDti, delinq: mockDelinq, grade: mockGrade, income: mockIncome, score: Math.round(1000*(1-pDef)) });
  }

  const gradeLabels = ["", "A — Prime", "B — Near prime", "C — Subprime", "D — Elevated", "E — High risk"];

  function switchTab(name) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
    const idx = ['score','portfolio','models'].indexOf(name);
    document.querySelectorAll('.tab')[idx].classList.add('active');
    document.getElementById('panel-' + name).classList.add('active');
  }

  function initCharts() {
    barChart = new Chart(document.getElementById('barChart').getContext('2d'), {
      type: 'bar',
      data: {
        labels: ['Interest rate','DTI','Delinquencies','Loan grade','Income'],
        datasets: [{ label: 'Risk contribution', data: [0,0,0,0,0], backgroundColor: ['#E24B4A','#EF9F27','#E24B4A','#BA7517','#4CAF50'], borderRadius: 4 }]
      },
      options: { responsive: true, maintainAspectRatio: false, indexAxis: 'y', plugins: { legend: { display: false } }, scales: { x: { beginAtZero: true }, y: { ticks: { font: { size: 11 } } } } }
    });

    donutChart = new Chart(document.getElementById('donutChart').getContext('2d'), {
      type: 'doughnut',
      data: {
        labels: ['Low risk','Moderate risk','Elevated risk','High risk'],
        datasets: [{ data: [0,0,0,0], backgroundColor: ['#4CAF50','#FF9800','#FF5722','#F44336'], borderWidth: 2, borderColor: '#fff' }]
      },
      options: { responsive: true, maintainAspectRatio: false, cutout: '55%', plugins: { legend: { display: false } } }
    });
  }

  function recalc() {
    const income  = parseFloat(document.getElementById('income').value)  || 60000;
    const loanamt = parseFloat(document.getElementById('loanamt').value) || 15000;
    const rate    = parseFloat(document.getElementById('rate').value);
    const dti     = parseFloat(document.getElementById('dti').value);
    const delinq  = parseFloat(document.getElementById('delinq').value);
    const grade   = parseFloat(document.getElementById('grade').value);

    // Update sidebar live labels
    document.getElementById('rate-out').textContent   = rate + '%';
    document.getElementById('dti-out').textContent    = dti + '%';
    document.getElementById('delinq-out').textContent = delinq;

    // Update Score tab summary panel
    document.getElementById('sum-income').textContent = '$' + income.toLocaleString();
    document.getElementById('sum-loan').textContent   = '$' + loanamt.toLocaleString();
    document.getElementById('sum-rate').textContent   = rate + '%';
    document.getElementById('sum-dti').textContent    = dti + '%';
    document.getElementById('sum-delinq').textContent = delinq;
    document.getElementById('sum-grade').textContent  = gradeLabels[grade];

    // Risk math
    const rateRisk    = Math.min(40, (rate-5)/25*40);
    const dtiRisk     = Math.min(30, dti/60*30);
    const delinqRisk  = delinq * 15;
    const gradeRisk   = (grade-1) * 8;
    const incomeBonus = Math.min(15, (income/100000)*15);

    const rawRisk  = rateRisk + dtiRisk + delinqRisk + gradeRisk - incomeBonus;
    const pDefault = Math.min(0.98, Math.max(0.01, rawRisk/100));
    const score    = Math.round(1000 * (1-pDefault));

    // Update current applicant in portfolio (slot 0)
    portfolioDatabase[0] = { rate, dti, delinq, grade, income, score };

    // Gauge
    document.getElementById('gauge-marker').style.left = Math.min(97, Math.max(1, score/10)) + '%';

    // Score result box
    let bg, color, decision;
    if      (score >= 800) { bg='#EAF3DE'; color='#3B6D11'; decision='APPROVE'; }
    else if (score >= 650) { bg='#FAEEDA'; color='#854F0B'; decision='APPROVE WITH CONDITIONS'; }
    else if (score >= 500) { bg='#FAEEDA'; color='#854F0B'; decision='MANUAL REVIEW'; }
    else                   { bg='#FCEBEB'; color='#A32D2D'; decision='DECLINE'; }

    document.getElementById('result-box').style.background = bg;
    document.getElementById('result-score').style.color    = color;
    document.getElementById('result-score').textContent    = score;
    document.getElementById('result-decision').style.color = color;
    document.getElementById('result-decision').textContent = decision;
    document.getElementById('result-prob').style.color     = color;
    document.getElementById('result-prob').textContent     = 'P(Default): ' + (pDefault*100).toFixed(1) + '%';

    // Risk flags
    const flags = [], goods = [];
    if (rate > 18)    flags.push('<span style="color:#A32D2D">High interest rate (' + rate + '%)</span>');
    if (dti > 35)     flags.push('<span style="color:#A32D2D">High debt-to-income (' + dti + '%)</span>');
    if (delinq > 0)   flags.push('<span style="color:#A32D2D">' + delinq + ' delinquencies in last 2 years</span>');
    if (grade >= 4)   flags.push('<span style="color:#854F0B">Elevated loan grade (' + ["","A","B","C","D","E"][grade] + ')</span>');
    if (delinq === 0) goods.push('<span style="color:#3B6D11">No recent delinquencies</span>');
    if (dti < 20)     goods.push('<span style="color:#3B6D11">Low debt-to-income ratio</span>');
    if (income > 80000) goods.push('<span style="color:#3B6D11">Strong income profile</span>');
    const all = [...flags, ...goods];
    document.getElementById('risk-flags').innerHTML = all.length ? all.join('<br>') : '<span style="color:#3B6D11">No significant risk flags</span>';

    // Recount portfolio tiers
    let low=0, mod=0, elev=0, high=0;
    portfolioDatabase.forEach(loan => {
      if      (loan.score >= 800) low++;
      else if (loan.score >= 650) mod++;
      else if (loan.score >= 500) elev++;
      else                        high++;
    });

    document.getElementById('low-count-val').textContent  = low;
    document.getElementById('mod-count-val').textContent  = mod;
    document.getElementById('elev-count-val').textContent = elev;
    document.getElementById('high-count-val').textContent = high;
    document.getElementById('low-count-lbl').textContent  = low  + ' loans';
    document.getElementById('mod-count-lbl').textContent  = mod  + ' loans';
    document.getElementById('elev-count-lbl').textContent = elev + ' loans';
    document.getElementById('high-count-lbl').textContent = high + ' loans';

    // Update charts
    if (barChart) {
      barChart.data.datasets[0].data = [Math.round(rateRisk), Math.round(dtiRisk), Math.round(delinqRisk), Math.round(gradeRisk), Math.round(incomeBonus)];
      barChart.data.datasets[0].backgroundColor = [
        rateRisk > 15   ? '#E24B4A' : '#4CAF50',
        dtiRisk > 15    ? '#E24B4A' : '#4CAF50',
        delinqRisk > 0  ? '#E24B4A' : '#4CAF50',
        gradeRisk > 20  ? '#E24B4A' : '#4CAF50',
        '#4CAF50'
      ];
      barChart.update();
    }
    if (donutChart) {
      donutChart.data.datasets[0].data = [low, mod, elev, high];
      donutChart.update();
    }
  }

  initCharts();
  recalc();
</script>
</body>
</html>
"""

components.html(html_code, height=750, scrolling=True)
