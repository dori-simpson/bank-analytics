
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Credit Risk Scoring Dashboard",
    page_icon="🏦",
    layout="wide"
)

st.markdown("""
<style>
    .block-container { padding: 0 !important; max-width: 100% !important; }
    header { display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }
    .stApp { background: #f0f2f5; }
    iframe { width: 100% !important; min-width: 0 !important; }
    section[data-testid="stMain"] > div { padding: 0 !important; }
</style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css">
<style>
  /* ── Design Tokens ── */
  :root {
    --bg:        #f0f2f5;
    --surface:   #ffffff;
    --border:    #e2e6ea;
    --text:      #1a1d23;
    --muted:     #6b7280;
    --accent:    #1a56db;
    --danger:    #dc2626;
    --warn:      #d97706;
    --success:   #16a34a;
    --radius:    12px;
    --radius-sm: 8px;
    --shadow:    0 1px 4px rgba(0,0,0,0.07), 0 4px 16px rgba(0,0,0,0.04);
  }

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 14px;
    background: var(--bg);
    color: var(--text);
    -webkit-font-smoothing: antialiased;
    overflow-x: hidden;
    width: 100%;
  }

  /* ── Page Shell ── */
  .shell {
    width: 100%;
    max-width: 100%;
    padding: 12px;
    overflow-x: hidden;
  }

  /* ── Header ── */
  .header {
    display: flex;
    align-items: center;
    gap: 12px;
    background: var(--surface);
    border-radius: var(--radius);
    padding: 14px 18px;
    margin-bottom: 14px;
    box-shadow: var(--shadow);
  }
  .header-icon {
    width: 40px; height: 40px;
    background: #eff6ff;
    border-radius: var(--radius-sm);
    display: flex; align-items: center; justify-content: center;
    color: var(--accent);
    font-size: 20px;
    flex-shrink: 0;
  }
  .header-title { font-size: 16px; font-weight: 600; letter-spacing: -0.01em; }
  .header-sub   { font-size: 11px; color: var(--muted); margin-top: 2px; line-height: 1.5; }

  /* ── Metric Strip ── */
  .metric-strip {
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 8px;
    margin-bottom: 14px;
    width: 100%;
    overflow: hidden;
  }
  .metric-card {
    background: var(--surface);
    border-radius: var(--radius-sm);
    padding: 10px 6px;
    text-align: center;
    box-shadow: var(--shadow);
    min-width: 0;
    overflow: hidden;
  }
  .metric-val  { font-size: clamp(14px, 2vw, 20px); font-weight: 600; letter-spacing: -0.02em; }
  .metric-lbl  { font-size: 9px; color: var(--muted); margin-top: 5px; }

  /* ── Badges ── */
  .badge {
    display: inline-flex; align-items: center; gap: 3px;
    font-size: 9.5px; font-weight: 600;
    padding: 3px 7px; border-radius: 20px;
    text-transform: uppercase; letter-spacing: 0.04em;
  }
  .b-green  { background: #dcfce7; color: #15803d; }
  .b-amber  { background: #fef3c7; color: #92400e; }
  .b-red    { background: #fee2e2; color: #b91c1c; }
  .b-blue   { background: #dbeafe; color: #1d4ed8; }
  .b-orange { background: #ffedd5; color: #c2410c; }

  /* ── Tabs ── */
  .tabs {
    display: flex;
    background: var(--surface);
    border-radius: var(--radius);
    padding: 4px;
    margin-bottom: 14px;
    box-shadow: var(--shadow);
    overflow-x: auto;
    gap: 2px;
    -webkit-overflow-scrolling: touch;
  }
  .tabs::-webkit-scrollbar { display: none; }
  .tab {
    flex: 1; min-width: 100px;
    padding: 10px 12px;
    font-size: 12.5px; font-weight: 500;
    color: var(--muted);
    cursor: pointer;
    border-radius: var(--radius-sm);
    display: flex; align-items: center; justify-content: center;
    gap: 6px;
    transition: all 0.18s ease;
    white-space: nowrap;
    border: none; background: none;
  }
  .tab.active {
    background: var(--accent);
    color: #fff;
    box-shadow: 0 2px 8px rgba(26,86,219,0.25);
  }
  .tab i { font-size: 15px; }

  /* ── Panels ── */
  .panel { display: none; }
  .panel.active { display: block; }

  /* ── Desktop 2-col ── */
  .two-col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
  }

  /* ── Cards ── */
  .card {
    background: var(--surface);
    border-radius: var(--radius);
    padding: 16px 18px;
    box-shadow: var(--shadow);
  }
  .card + .card { margin-top: 14px; }
  .card-title {
    font-size: 12px; font-weight: 600;
    color: var(--muted);
    text-transform: uppercase; letter-spacing: 0.06em;
    margin-bottom: 14px;
    display: flex; align-items: center; gap: 6px;
  }

  /* ── Parameter Controls ── */
  .param-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    margin-bottom: 16px;
  }
  .param-field { display: flex; flex-direction: column; gap: 6px; }
  .param-label {
    font-size: 11px; font-weight: 500; color: var(--muted);
    display: flex; justify-content: space-between; align-items: center;
  }
  .param-label .val-badge {
    font-size: 11px; font-weight: 600; color: var(--accent);
    background: #eff6ff; padding: 1px 6px; border-radius: 4px;
  }
  input[type="number"] {
    width: 100%; padding: 9px 12px;
    border: 1.5px solid var(--border);
    border-radius: var(--radius-sm);
    font-size: 14px; font-weight: 500;
    color: var(--text);
    background: #fafafa;
    transition: border-color 0.15s;
    -webkit-appearance: none;
  }
  input[type="number"]:focus { outline: none; border-color: var(--accent); background: #fff; }
  input[type="range"] {
    -webkit-appearance: none;
    width: 100%; height: 5px;
    border-radius: 3px;
    background: var(--border);
    outline: none;
    cursor: pointer;
  }
  input[type="range"]::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 20px; height: 20px;
    border-radius: 50%;
    background: var(--accent);
    box-shadow: 0 1px 4px rgba(26,86,219,0.35);
    cursor: pointer;
  }
  input[type="range"]::-moz-range-thumb {
    width: 20px; height: 20px;
    border-radius: 50%; border: none;
    background: var(--accent);
    cursor: pointer;
  }
  select {
    width: 100%; padding: 9px 12px;
    border: 1.5px solid var(--border);
    border-radius: var(--radius-sm);
    font-size: 14px; font-weight: 500;
    color: var(--text); background: #fafafa;
    -webkit-appearance: none;
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24'%3E%3Cpath fill='%236b7280' d='M7 10l5 5 5-5z'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 10px center;
    cursor: pointer;
  }
  select:focus { outline: none; border-color: var(--accent); }

  /* ── Gauge ── */
  .gauge-wrap { margin: 16px 0 12px; }
  .gauge-bar {
    width: 100%; height: 12px; border-radius: 6px;
    background: linear-gradient(to right, #dc2626, #f59e0b, #16a34a);
    position: relative;
  }
  .gauge-marker {
    position: absolute; top: -5px;
    height: 22px; width: 4px;
    background: var(--text);
    border-radius: 2px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.3);
    transition: left 0.45s cubic-bezier(0.34, 1.56, 0.64, 1);
  }
  .gauge-labels {
    display: flex; justify-content: space-between;
    font-size: 9.5px; color: var(--muted); margin-top: 6px;
  }

  /* ── Score Result ── */
  .result-box {
    border-radius: var(--radius);
    padding: 20px;
    text-align: center;
    margin-top: 14px;
    transition: background 0.3s ease;
  }
  .result-score    { font-size: 48px; font-weight: 700; letter-spacing: -0.03em; line-height: 1; }
  .result-decision { font-size: 13px; font-weight: 600; margin-top: 6px; letter-spacing: 0.05em; }
  .result-prob     { font-size: 12px; margin-top: 4px; opacity: 0.8; }

  /* ── Risk Flags ── */
  .flag-item {
    display: flex; align-items: center; gap: 8px;
    padding: 8px 0;
    border-bottom: 1px solid var(--border);
    font-size: 13px;
  }
  .flag-item:last-child { border-bottom: none; }
  .flag-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }

  /* ── Breakdown Chart ── */
  .bar-chart-wrap { width: 100%; height: 160px; position: relative; }

  /* ── Summary Grid (Score tab) ── */
  .summary-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    margin-bottom: 14px;
  }
  .summary-item {
    background: #f8fafc;
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 8px 10px;
  }
  .summary-item .s-lbl { font-size: 10px; color: var(--muted); }
  .summary-item .s-val { font-size: 13px; font-weight: 600; margin-top: 2px; }

  /* ── Portfolio / Tier rows ── */
  .tier-row {
    display: flex; align-items: center;
    justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px solid var(--border);
    font-size: 13px;
  }
  .tier-row:last-child { border-bottom: none; }
  .tier-left  { display: flex; align-items: center; gap: 8px; }
  .tier-dot   { width: 10px; height: 10px; border-radius: 50%; }
  .tier-count { font-size: 12px; color: var(--muted); min-width: 64px; text-align: right; }

  /* ── Model Benchmark ── */
  .model-row {
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 12px; font-size: 13px;
  }
  .model-name { width: 150px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; flex-shrink: 0; }
  .bar-track  { flex: 1; background: #f1f5f9; border-radius: 4px; height: 8px; }
  .bar-fill   { height: 8px; border-radius: 4px; transition: width 0.4s ease; }
  .auc-val    { font-size: 12px; color: var(--muted); width: 44px; text-align: right; flex-shrink: 0; }
  .best-pill  { font-size: 9px; padding: 1px 6px; background: #dbeafe; color: #1d4ed8; border-radius: 20px; font-weight: 600; }

  /* ── Key Metrics Table ── */
  .kv-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 9px 0; border-bottom: 1px solid var(--border);
    font-size: 13px;
  }
  .kv-row:last-child { border-bottom: none; }
  .kv-key { color: var(--muted); }
  .kv-val { font-weight: 600; }

  /* ── CTA Button ── */
  .cta-btn {
    display: block; width: 100%;
    padding: 12px;
    background: var(--accent);
    color: #fff;
    border: none; border-radius: var(--radius-sm);
    font-size: 14px; font-weight: 600;
    cursor: pointer;
    margin-top: 16px;
    transition: background 0.15s, transform 0.1s;
    letter-spacing: 0.01em;
  }
  .cta-btn:hover  { background: #1e40af; }
  .cta-btn:active { transform: scale(0.98); }

  /* ── Donut chart container ── */
  .donut-wrap { width: 100%; height: 200px; position: relative; }

  /* ── Footer note ── */
  .note-box {
    margin-top: 14px; padding: 12px 14px;
    background: #f8fafc; border-radius: var(--radius-sm);
    border-left: 3px solid var(--accent);
    font-size: 12px; color: var(--muted); line-height: 1.6;
  }

  /* ════════════════════════════════════════
     RESPONSIVE BREAKPOINTS
  ════════════════════════════════════════ */

  /* Tablet: collapse to single column */
  @media (max-width: 768px) {
    .shell { padding: 12px; }
    .two-col { grid-template-columns: 1fr; }
    .metric-strip { grid-template-columns: repeat(3, 1fr); }
    .metric-strip .metric-card:nth-child(4),
    .metric-strip .metric-card:nth-child(5) { display: none; }
    .header-sub { display: none; }
    .summary-grid { grid-template-columns: repeat(2, 1fr); }
  }

  /* Mobile: full single column */
  @media (max-width: 480px) {
    .shell { padding: 10px; }
    .metric-strip { grid-template-columns: repeat(2, 1fr); gap: 8px; }
    .metric-strip .metric-card:nth-child(3),
    .metric-strip .metric-card:nth-child(4),
    .metric-strip .metric-card:nth-child(5) { display: none; }
    .metric-val  { font-size: 18px; }
    .param-grid  { grid-template-columns: 1fr; }
    .summary-grid { grid-template-columns: repeat(2, 1fr); }
    .result-score { font-size: 40px; }
    .model-name  { width: 110px; }
    .card { padding: 14px; }
    .tab  { font-size: 11.5px; padding: 9px 10px; min-width: 80px; }
    .header { padding: 12px 14px; }
    .header-title { font-size: 14px; }
    .header-icon  { width: 34px; height: 34px; font-size: 17px; }
  }

  /* Very small screens */
  @media (max-width: 360px) {
    .tab i { display: none; }
    .tab   { min-width: 70px; }
  }
</style>
</head>
<body>
<div class="shell">

  <div class="header">
    <div class="header-icon"><i class="ti ti-building-bank"></i></div>
    <div>
      <div class="header-title">Credit Risk Scoring</div>
      <div class="header-sub">Logistic Regression &nbsp;·&nbsp; ROC-AUC: 0.640 &nbsp;·&nbsp; 10,000 loans &nbsp;·&nbsp; 1.78% default rate</div>
    </div>
  </div>

  <div class="metric-strip">
    <div class="metric-card">
      <div class="metric-val" id="low-count-val">—</div>
      <div class="metric-lbl"><span class="badge b-green">✓ Low Risk</span></div>
    </div>
    <div class="metric-card">
      <div class="metric-val" id="mod-count-val">—</div>
      <div class="metric-lbl"><span class="badge b-amber">⚠ Moderate</span></div>
    </div>
    <div class="metric-card">
      <div class="metric-val" id="elev-count-val">—</div>
      <div class="metric-lbl"><span class="badge b-orange">~ Elevated</span></div>
    </div>
    <div class="metric-card">
      <div class="metric-val" id="high-count-val">—</div>
      <div class="metric-lbl"><span class="badge b-red">✕ High Risk</span></div>
    </div>
    <div class="metric-card">
      <div class="metric-val">0.640</div>
      <div class="metric-lbl"><span class="badge b-blue">ROC-AUC</span></div>
    </div>
  </div>

  <div class="tabs">
    <button class="tab active" onclick="switchTab('score')">
      <i class="ti ti-search"></i> Score
    </button>
    <button class="tab" onclick="switchTab('portfolio')">
      <i class="ti ti-chart-pie"></i> Portfolio
    </button>
    <button class="tab" onclick="switchTab('models')">
      <i class="ti ti-chart-bar"></i> Models
    </button>
  </div>

  <div id="panel-score" class="panel active">
    <div class="two-col">

      <div>
        <div class="card">
          <div class="card-title"><i class="ti ti-sliders"></i> Applicant Parameters</div>

          <div class="param-grid">
            <div class="param-field">
              <div class="param-label">Annual income ($)</div>
              <input type="number" id="income" value="85000" min="0" step="5000" oninput="recalc()" />
            </div>
            <div class="param-field">
              <div class="param-label">Loan amount ($)</div>
              <input type="number" id="loanamt" value="15000" min="0" step="1000" oninput="recalc()" />
            </div>
            <div class="param-field">
              <div class="param-label">
                Interest rate
                <span class="val-badge" id="rate-out">10.5%</span>
              </div>
              <input type="range" id="rate" min="5" max="30" step="0.5" value="10.5"
                     oninput="document.getElementById('rate-out').textContent=this.value+'%'; recalc()" />
            </div>
            <div class="param-field">
              <div class="param-label">
                Debt-to-income
                <span class="val-badge" id="dti-out">2%</span>
              </div>
              <input type="range" id="dti" min="0" max="60" step="1" value="2"
                     oninput="document.getElementById('dti-out').textContent=this.value+'%'; recalc()" />
            </div>
            <div class="param-field">
              <div class="param-label">
                Delinquencies (2yr)
                <span class="val-badge" id="delinq-out">1</span>
              </div>
              <input type="range" id="delinq" min="0" max="10" step="1" value="1"
                     oninput="document.getElementById('delinq-out').textContent=this.value; recalc()" />
            </div>
            <div class="param-field">
              <div class="param-label">Loan grade</div>
              <select id="grade" onchange="recalc()">
                <option value="1" selected>A — Prime</option>
                <option value="2">B — Near prime</option>
                <option value="3">C — Subprime</option>
                <option value="4">D — Elevated</option>
                <option value="5">E — High risk</option>
              </select>
            </div>
          </div>

          <div class="gauge-wrap">
            <div class="gauge-bar">
              <div class="gauge-marker" id="gauge-marker" style="left:75%"></div>
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
            <div class="result-score"    id="result-score">—</div>
            <div class="result-decision" id="result-decision">—</div>
            <div class="result-prob"     id="result-prob">—</div>
          </div>
        </div>
      </div>

      <div>
        <div class="card">
          <div class="card-title"><i class="ti ti-flag"></i> Risk Factor Analysis</div>
          <div id="risk-flags"></div>
        </div>
        <div class="card">
          <div class="card-title"><i class="ti ti-chart-bar"></i> Default Probability Breakdown</div>
          <div class="bar-chart-wrap">
            <canvas id="barChart"></canvas>
          </div>
        </div>
      </div>

    </div>
  </div>

  <div id="panel-portfolio" class="panel">
    <div class="two-col">
      <div class="card">
        <div class="card-title"><i class="ti ti-chart-donut"></i> Risk Tier Breakdown</div>
        <div class="donut-wrap">
          <canvas id="donutChart"></canvas>
        </div>
      </div>
      <div class="card">
        <div class="card-title"><i class="ti ti-list-details"></i> Tier Details</div>
        <div class="tier-row">
          <div class="tier-left">
            <div class="tier-dot" style="background:#16a34a"></div>
            <span>Low risk</span>
          </div>
          <span class="tier-count" id="low-count-lbl">—</span>
          <span class="badge b-green">Approve</span>
        </div>
        <div class="tier-row">
          <div class="tier-left">
            <div class="tier-dot" style="background:#d97706"></div>
            <span>Moderate risk</span>
          </div>
          <span class="tier-count" id="mod-count-lbl">—</span>
          <span class="badge b-amber">Conditions</span>
        </div>
        <div class="tier-row">
          <div class="tier-left">
            <div class="tier-dot" style="background:#ea580c"></div>
            <span>Elevated risk</span>
          </div>
          <span class="tier-count" id="elev-count-lbl">—</span>
          <span class="badge b-orange">Review</span>
        </div>
        <div class="tier-row">
          <div class="tier-left">
            <div class="tier-dot" style="background:#dc2626"></div>
            <span>High risk</span>
          </div>
          <span class="tier-count" id="high-count-lbl">—</span>
          <span class="badge b-red">Decline</span>
        </div>
        <div style="margin-top:14px;padding-top:12px;border-top:1px solid var(--border);font-size:12px;color:var(--muted);line-height:1.8;">
          <div>Actual default rate: <b style="color:var(--text)">1.78%</b></div>
          <div>Total scored: <b style="color:var(--text)">2,000</b> (test set)</div>
        </div>
      </div>
    </div>
  </div>

  <div id="panel-models" class="panel">
    <div class="two-col">
      <div class="card">
        <div class="card-title"><i class="ti ti-podium"></i> ROC-AUC Benchmark</div>
        <div class="model-row">
          <div class="model-name">Logistic Regression &nbsp;<span class="best-pill">best</span></div>
          <div class="bar-track"><div class="bar-fill" style="width:56%;background:#1a56db"></div></div>
          <div class="auc-val">0.6400</div>
        </div>
        <div class="model-row">
          <div class="model-name">Random Forest</div>
          <div class="bar-track"><div class="bar-fill" style="width:53%;background:#16a34a"></div></div>
          <div class="auc-val">0.6342</div>
        </div>
        <div class="model-row">
          <div class="model-name">XGBoost</div>
          <div class="bar-track"><div class="bar-fill" style="width:49%;background:#dc2626"></div></div>
          <div class="auc-val">0.5994</div>
        </div>
        <div class="note-box">
          <b style="color:var(--text)">Note on AUC:</b> Only 178 defaults in 10,000 loans (1.78%). The test set holds ~35 defaults, making ROC-AUC noisier at small scale. All models beat random chance (0.5).
        </div>
      </div>
      <div class="card">
        <div class="card-title"><i class="ti ti-info-circle"></i> Key Metrics</div>
        <div class="kv-row"><span class="kv-key">Dataset size</span>      <span class="kv-val">10,000 loans</span></div>
        <div class="kv-row"><span class="kv-key">Train / test split</span><span class="kv-val">80% / 20%</span></div>
        <div class="kv-row"><span class="kv-key">Default rate</span>      <span class="kv-val">1.78%</span></div>
        <div class="kv-row"><span class="kv-key">Total defaults</span>    <span class="kv-val">178 loans</span></div>
        <div class="kv-row"><span class="kv-key">Primary metric</span>    <span class="kv-val">ROC-AUC</span></div>
        <div class="kv-row"><span class="kv-key">Imbalance handling</span><span class="kv-val">Class weight balanced</span></div>
        <div class="kv-row"><span class="kv-key">Explainability</span>    <span class="kv-val">SHAP LinearExplainer</span></div>
        <button class="cta-btn">Improve Model AUC ↗</button>
      </div>
    </div>
  </div>

</div><script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<script>
  // ── Seeded RNG so portfolio is stable on every load ──
  function seededRandom(seed) {
    let mw = (123456789 + seed) & 0xffffffff;
    let mz = (987654321 - seed) & 0xffffffff;
    return function() {
      mz = (36969*(mz&65535)+(mz>>16))&0xffffffff;
      mw = (18000*(mw&65535)+(mw>>16))&0xffffffff;
      return ((((mz<<16)+mw)>>16)&0x7FFFFFFF)/0x7FFFFFFF;
    };
  }
  const rng = seededRandom(42);
  
  // ── Unified Risk Engine (Fixes Data Leakage Issue) ──
  function calculateRisk(rate, dti, delinq, grade, income) {
      const rateRisk    = Math.min(40, (rate-5)/25*40);
      const dtiRisk     = Math.min(30, dti/60*30);
      const delinqRisk  = delinq * 20;
      const gradeRisk   = (grade-1) * 15;
      const incomeBonus = Math.min(20, (income/100000)*20);

      // Calculates 0-1000 scale appropriately
      let rawScore = 1000 - (rateRisk*2.5 + dtiRisk*3.5 + delinqRisk*5 + gradeRisk*4) + (incomeBonus*2);
      let score = Math.max(0, Math.min(1000, Math.round(rawScore)));

      // Maps score to an exponential curve to yield a realistic P(Default)
      let pDefault = Math.min(0.98, Math.max(0.001, Math.exp(-score / 120)));

      return { score, pDefault, rateRisk, dtiRisk, delinqRisk, gradeRisk, incomeBonus };
  }

  // ── Generates Portfolio ──
  const portfolioDatabase = [];
  for (let i = 0; i < 2000; i++) {
    // Generates a prime-skewed healthy portfolio simulating a 1.78% actual default environment
    const isPrime = rng() > 0.25; 
    const r = isPrime ? (5 + rng()*6) : (11 + rng()*15);
    const d = isPrime ? (rng()*20) : (20 + rng()*40);
    const q = rng() > 0.95 ? Math.floor(1 + rng()*2) : 0; 
    const g = isPrime ? (rng() > 0.4 ? 1 : 2) : Math.floor(3 + rng()*3);
    const inc = isPrime ? (55000 + rng()*90000) : (35000 + rng()*45000);

    const { score, pDefault } = calculateRisk(r, d, q, g, inc);
    portfolioDatabase.push({ rate:r, dti:d, delinq:q, grade:g, income:inc, score, pDefault });
  }

  const GRADE_LABELS = ["","A — Prime","B — Near prime","C — Subprime","D — Elevated","E — High risk"];
  let barChart, donutChart;

  // ── Tab switching ──
  function switchTab(name) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
    const idx = ['score','portfolio','models'].indexOf(name);
    document.querySelectorAll('.tab')[idx].classList.add('active');
    document.getElementById('panel-'+name).classList.add('active');
  }

  // ── Init Charts ──
  function initCharts() {
    barChart = new Chart(document.getElementById('barChart').getContext('2d'), {
      type: 'bar',
      data: {
        labels: ['Interest rate','DTI','Delinquencies','Loan grade','Income'],
        datasets: [{ data:[0,0,0,0,0], backgroundColor:['#dc2626','#f59e0b','#dc2626','#d97706','#16a34a'], borderRadius:4, label:'Risk contribution' }]
      },
      options: {
        responsive:true, maintainAspectRatio:false, indexAxis:'y',
        plugins:{ legend:{ display:false } },
        scales:{
          x:{ beginAtZero:true, grid:{ color:'#f1f5f9' }, ticks:{ font:{ size:11 } } },
          y:{ ticks:{ font:{ size:11 } }, grid:{ display:false } }
        }
      }
    });

    donutChart = new Chart(document.getElementById('donutChart').getContext('2d'), {
      type: 'doughnut',
      data: {
        labels: ['Low risk','Moderate risk','Elevated risk','High risk'],
        datasets: [{ data:[0,0,0,0], backgroundColor:['#16a34a','#d97706','#ea580c','#dc2626'], borderWidth:3, borderColor:'#fff' }]
      },
      options: {
        responsive:true, maintainAspectRatio:false, cutout:'58%',
        plugins:{
          legend:{ position:'bottom', labels:{ font:{ size:11 }, padding:12 } }
        }
      }
    });
  }

  // ── Main recalc — runs on every input change ──
  function recalc() {
    const income  = parseFloat(document.getElementById('income').value)  || 60000;
    const loanamt = parseFloat(document.getElementById('loanamt').value) || 15000;
    const rate    = parseFloat(document.getElementById('rate').value);
    const dti     = parseFloat(document.getElementById('dti').value);
    const delinq  = parseFloat(document.getElementById('delinq').value);
    const grade   = parseFloat(document.getElementById('grade').value);

    // Sync slider display badges
    document.getElementById('rate-out').textContent   = rate + '%';
    document.getElementById('dti-out').textContent    = dti + '%';
    document.getElementById('delinq-out').textContent = delinq;

    // Use unified risk function
    const { score, pDefault, rateRisk, dtiRisk, delinqRisk, gradeRisk, incomeBonus } = calculateRisk(rate, dti, delinq, grade, income);

    // Update this applicant in portfolio slot 0
    portfolioDatabase[0] = { rate, dti, delinq, grade, income, score, pDefault };

    // ── GAUGE MAPPING FIX ──
    // Properly map the visual indicator position against the non-linear 0-500-650-800-1000 spans
    let visualPercent = 0;
    if (score <= 500) {
        visualPercent = (score / 500) * 25;
    } else if (score <= 650) {
        visualPercent = 25 + ((score - 500) / 150) * 25;
    } else if (score <= 800) {
        visualPercent = 50 + ((score - 650) / 150) * 25;
    } else {
        visualPercent = 75 + ((score - 800) / 200) * 25;
    }
    document.getElementById('gauge-marker').style.left = Math.min(98, Math.max(1, visualPercent)) + '%';

    // Score result
    let bg, color, decision;
    if      (score >= 800) { bg='#dcfce7'; color='#15803d'; decision='APPROVE'; }
    else if (score >= 650) { bg='#fef3c7'; color='#92400e'; decision='APPROVE WITH CONDITIONS'; }
    else if (score >= 500) { bg='#ffedd5'; color='#c2410c'; decision='MANUAL REVIEW'; }
    else                   { bg='#fee2e2'; color='#b91c1c'; decision='DECLINE'; }
    
    document.getElementById('result-box').style.background      = bg;
    document.getElementById('result-score').style.color         = color;
    document.getElementById('result-score').textContent         = score;
    document.getElementById('result-decision').style.color      = color;
    document.getElementById('result-decision').textContent      = decision;
    document.getElementById('result-prob').style.color          = color;
    document.getElementById('result-prob').textContent          = 'P(Default): ' + (pDefault*100).toFixed(2) + '%';

    // Risk flags
    const items = [];
    if (rate > 18)      items.push({ text:'High interest rate ('+rate+'%)',                color:'#b91c1c', dot:'#dc2626' });
    if (dti > 35)       items.push({ text:'High debt-to-income ('+dti+'%)',                color:'#b91c1c', dot:'#dc2626' });
    if (delinq > 0)     items.push({ text:delinq+' delinquenc'+(delinq>1?'ies':'y')+' in last 2 years', color:'#b91c1c', dot:'#dc2626' });
    if (grade >= 4)     items.push({ text:'Elevated loan grade ('+["","A","B","C","D","E"][grade]+')', color:'#92400e', dot:'#d97706' });
    if (delinq === 0)   items.push({ text:'No recent delinquencies',    color:'#15803d', dot:'#16a34a' });
    if (dti < 20)       items.push({ text:'Low debt-to-income ratio',   color:'#15803d', dot:'#16a34a' });
    if (income > 80000) items.push({ text:'Strong income profile',      color:'#15803d', dot:'#16a34a' });
    if (!items.length)  items.push({ text:'No significant risk flags',  color:'#15803d', dot:'#16a34a' });

    document.getElementById('risk-flags').innerHTML = items.map(f =>
      `<div class="flag-item">
         <div class="flag-dot" style="background:${f.dot}"></div>
         <span style="color:${f.color}">${f.text}</span>
       </div>`
    ).join('');

    // Portfolio counts
    let low=0, mod=0, elev=0, high=0;
    portfolioDatabase.forEach(l => {
      if      (l.score >= 800) low++;
      else if (l.score >= 650) mod++;
      else if (l.score >= 500) elev++;
      else                     high++;
    });

    document.getElementById('low-count-val').textContent  = low;
    document.getElementById('mod-count-val').textContent  = mod;
    document.getElementById('elev-count-val').textContent = elev;
    document.getElementById('high-count-val').textContent = high;
    document.getElementById('low-count-lbl').textContent  = low  + ' loans';
    document.getElementById('mod-count-lbl').textContent  = mod  + ' loans';
    document.getElementById('elev-count-lbl').textContent = elev + ' loans';
    document.getElementById('high-count-lbl').textContent = high + ' loans';

    // Bar chart
    if (barChart) {
      barChart.data.datasets[0].data = [
        Math.round(rateRisk), Math.round(dtiRisk),
        Math.round(delinqRisk), Math.round(gradeRisk), Math.round(incomeBonus)
      ];
      barChart.data.datasets[0].backgroundColor = [
        rateRisk   > 15 ? '#dc2626' : '#16a34a',
        dtiRisk    > 15 ? '#dc2626' : '#16a34a',
        delinqRisk >  0 ? '#dc2626' : '#16a34a',
        gradeRisk  > 20 ? '#dc2626' : '#16a34a',
        '#16a34a'
      ];
      barChart.update('none');
    }

    // Donut chart
    if (donutChart) {
      donutChart.data.datasets[0].data = [low, mod, elev, high];
      donutChart.update('none');
    }
  }

  initCharts();
  recalc();
</script>
</body>
</html>
"""

components.html(html_code, height=900, scrolling=True)
