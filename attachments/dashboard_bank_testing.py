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
    iframe { width: 100% !important; min-width: 0 !important; height: 100vh !important; border: none; }
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
  :root {
    --bg:#f0f2f5; --surface:#ffffff; --border:#e2e6ea;
    --text:#1a1d23; --muted:#6b7280; --accent:#1a56db;
    --danger:#dc2626; --warn:#d97706; --success:#16a34a;
    --radius:12px; --radius-sm:8px;
    --shadow:0 1px 4px rgba(0,0,0,0.07),0 4px 16px rgba(0,0,0,0.04);
  }
  *,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
  body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:14px;background:var(--bg);color:var(--text);-webkit-font-smoothing:antialiased;overflow-x:hidden;width:100%}
  .shell{width:100%;max-width:100%;padding:12px;overflow-x:hidden}
 
  /* ── Header ── */
  .header{display:flex;align-items:center;gap:12px;background:var(--surface);border-radius:var(--radius);padding:14px 18px;margin-bottom:14px;box-shadow:var(--shadow);flex-wrap:wrap}
  .header-icon{width:40px;height:40px;background:#eff6ff;border-radius:var(--radius-sm);display:flex;align-items:center;justify-content:center;color:var(--accent);font-size:20px;flex-shrink:0}
  .header-body{flex:1;min-width:0}
  .header-title{font-size:16px;font-weight:600;letter-spacing:-0.01em}
  .header-sub{font-size:11px;color:var(--muted);margin-top:2px;line-height:1.5}
  .header-actions{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
  .header-btn{display:flex;align-items:center;gap:5px;padding:7px 12px;border:1.5px solid var(--border);border-radius:var(--radius-sm);background:#fff;font-size:12px;font-weight:500;color:var(--text);cursor:pointer;white-space:nowrap;transition:all 0.15s}
  .header-btn:hover{border-color:var(--accent);color:var(--accent)}
  .header-btn.primary{background:var(--accent);color:#fff;border-color:var(--accent)}
  .header-btn.primary:hover{background:#1e40af}
 
  /* ── Alert ── */
  .alert-banner{display:none;align-items:center;gap:10px;background:#fef3c7;border:1px solid #fcd34d;border-radius:var(--radius-sm);padding:10px 14px;margin-bottom:10px;font-size:12px;color:#92400e}
  .alert-banner.show{display:flex}
  .alert-close{margin-left:auto;cursor:pointer;opacity:0.6}
  .alert-close:hover{opacity:1}
 
  /* ── Applicant Badge ── */
  .applicant-badge{display:flex;align-items:center;gap:8px;background:#eff6ff;border:1px solid #bfdbfe;border-radius:var(--radius-sm);padding:8px 12px;margin-bottom:12px;font-size:12px}
  .applicant-badge i{color:var(--accent);font-size:16px}
  .applicant-badge .ab-name{font-weight:600;color:var(--text)}
  .applicant-badge .ab-id{color:var(--muted);font-size:11px;margin-left:4px}
  .applicant-badge .ab-clear{margin-left:auto;cursor:pointer;color:var(--muted);font-size:11px;border:1px solid var(--border);padding:2px 8px;border-radius:4px;background:#fff}
  .applicant-badge .ab-clear:hover{color:var(--danger);border-color:var(--danger)}
 
  /* ── Metric Strip ── */
  .metric-strip{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px;margin-bottom:14px;width:100%;overflow:hidden}
  .metric-card{background:var(--surface);border-radius:var(--radius-sm);padding:10px 6px;text-align:center;box-shadow:var(--shadow);min-width:0;overflow:hidden;cursor:pointer;transition:box-shadow 0.15s}
  .metric-card:hover{box-shadow:0 2px 8px rgba(0,0,0,0.12)}
  .metric-val{font-size:clamp(14px,2vw,20px);font-weight:600;letter-spacing:-0.02em}
  .metric-lbl{font-size:9px;color:var(--muted);margin-top:5px}
 
  /* ── Badges ── */
  .badge{display:inline-flex;align-items:center;gap:3px;font-size:9.5px;font-weight:600;padding:3px 7px;border-radius:20px;text-transform:uppercase;letter-spacing:0.04em}
  .b-green{background:#dcfce7;color:#15803d}
  .b-amber{background:#fef3c7;color:#92400e}
  .b-red{background:#fee2e2;color:#b91c1c}
  .b-blue{background:#dbeafe;color:#1d4ed8}
  .b-orange{background:#ffedd5;color:#c2410c}
  .b-gray{background:#f1f5f9;color:#475569}
  .b-purple{background:#ede9fe;color:#6d28d9}
 
  /* ── Tabs ── */
  .tabs{display:flex;background:var(--surface);border-radius:var(--radius);padding:4px;margin-bottom:14px;box-shadow:var(--shadow);overflow-x:auto;gap:2px;-webkit-overflow-scrolling:touch}
  .tabs::-webkit-scrollbar{display:none}
  .tab{flex:1;min-width:80px;padding:10px 12px;font-size:12.5px;font-weight:500;color:var(--muted);cursor:pointer;border-radius:var(--radius-sm);display:flex;align-items:center;justify-content:center;gap:6px;transition:all 0.18s ease;white-space:nowrap;border:none;background:none}
  .tab.active{background:var(--accent);color:#fff;box-shadow:0 2px 8px rgba(26,86,219,0.25)}
  .tab i{font-size:15px}
  .panel{display:none}
  .panel.active{display:block}
 
  /* ── Layout ── */
  .two-col{display:grid;grid-template-columns:1fr 1fr;gap:14px}
  .three-col{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin-bottom:14px}
 
  /* ── Cards ── */
  .card{background:var(--surface);border-radius:var(--radius);padding:16px 18px;box-shadow:var(--shadow)}
  .card+.card{margin-top:14px}
  .card-title{font-size:12px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:14px;display:flex;align-items:center;gap:6px}
 
  /* ── Params ── */
  .param-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:16px}
  .param-field{display:flex;flex-direction:column;gap:6px}
  .param-label{font-size:11px;font-weight:500;color:var(--muted);display:flex;justify-content:space-between;align-items:center}
  .param-label .val-badge{font-size:11px;font-weight:600;color:var(--accent);background:#eff6ff;padding:1px 6px;border-radius:4px}
  input[type="number"],input[type="text"]{width:100%;padding:9px 12px;border:1.5px solid var(--border);border-radius:var(--radius-sm);font-size:14px;font-weight:500;color:var(--text);background:#fafafa;transition:border-color 0.15s;-webkit-appearance:none}
  input[type="number"]:focus,input[type="text"]:focus{outline:none;border-color:var(--accent);background:#fff}
  input[type="range"]{-webkit-appearance:none;width:100%;height:5px;border-radius:3px;background:var(--border);outline:none;cursor:pointer}
  input[type="range"]::-webkit-slider-thumb{-webkit-appearance:none;width:20px;height:20px;border-radius:50%;background:var(--accent);box-shadow:0 1px 4px rgba(26,86,219,0.35);cursor:pointer}
  input[type="range"]::-moz-range-thumb{width:20px;height:20px;border-radius:50%;border:none;background:var(--accent);cursor:pointer}
  select{width:100%;padding:9px 12px;border:1.5px solid var(--border);border-radius:var(--radius-sm);font-size:14px;font-weight:500;color:var(--text);background:#fafafa;-webkit-appearance:none;appearance:none;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24'%3E%3Cpath fill='%236b7280' d='M7 10l5 5 5-5z'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 10px center;cursor:pointer}
  select:focus{outline:none;border-color:var(--accent)}
 
  /* ── Gauge ── */
  .gauge-wrap{margin:16px 0 12px}
  .gauge-bar{width:100%;height:12px;border-radius:6px;background:linear-gradient(to right,#dc2626,#f59e0b,#16a34a);position:relative}
  .gauge-marker{position:absolute;top:-5px;height:22px;width:4px;background:var(--text);border-radius:2px;box-shadow:0 1px 4px rgba(0,0,0,0.3);transition:left 0.45s cubic-bezier(0.34,1.56,0.64,1)}
  .gauge-labels{display:flex;justify-content:space-between;font-size:9.5px;color:var(--muted);margin-top:6px}
 
  /* ── Result ── */
  .result-box{border-radius:var(--radius);padding:20px;text-align:center;margin-top:14px;transition:background 0.3s ease}
  .result-score{font-size:48px;font-weight:700;letter-spacing:-0.03em;line-height:1}
  .result-decision{font-size:13px;font-weight:600;margin-top:6px;letter-spacing:0.05em}
  .result-prob{font-size:12px;margin-top:4px;opacity:0.8}
  .result-meta{font-size:11px;margin-top:8px;opacity:0.65}
 
  /* ── Compliance strip ── */
  .compliance-strip{display:flex;align-items:flex-start;gap:8px;background:#f0fdf4;border:1px solid #bbf7d0;border-radius:var(--radius-sm);padding:10px 12px;margin-top:12px;font-size:11px;color:#15803d;line-height:1.5}
  .compliance-strip i{font-size:15px;flex-shrink:0;margin-top:1px}
 
  /* ── Adverse action ── */
  .adverse-box{background:#fff7ed;border:1px solid #fed7aa;border-radius:var(--radius-sm);padding:12px 14px;margin-top:10px;font-size:12px;color:#92400e}
  .adverse-box .adverse-title{font-weight:600;margin-bottom:6px;display:flex;align-items:center;gap:6px}
  .adverse-list{list-style:none;padding:0}
  .adverse-list li{padding:3px 0;padding-left:14px;position:relative}
  .adverse-list li::before{content:"•";position:absolute;left:0}
 
  /* ── Risk flags ── */
  .flag-item{display:flex;align-items:center;gap:8px;padding:8px 0;border-bottom:1px solid var(--border);font-size:13px}
  .flag-item:last-child{border-bottom:none}
  .flag-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
 
  /* ── Charts ── */
  .bar-chart-wrap{width:100%;height:160px;position:relative}
  .donut-wrap{width:100%;height:200px;position:relative}
  .line-wrap{width:100%;height:200px;position:relative}
 
  /* ── Summary grid ── */
  .summary-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:14px}
  .summary-item{background:#f8fafc;border:1px solid var(--border);border-radius:var(--radius-sm);padding:8px 10px}
  .summary-item .s-lbl{font-size:10px;color:var(--muted)}
  .summary-item .s-val{font-size:13px;font-weight:600;margin-top:2px}
 
  /* ── Tier rows ── */
  .tier-row{display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:1px solid var(--border);font-size:13px}
  .tier-row:last-child{border-bottom:none}
  .tier-left{display:flex;align-items:center;gap:8px}
  .tier-dot{width:10px;height:10px;border-radius:50%}
  .tier-count{font-size:12px;color:var(--muted);min-width:64px;text-align:right}
 
  /* ── Model bench ── */
  .model-row{display:flex;align-items:center;gap:10px;margin-bottom:12px;font-size:13px}
  .model-name{width:150px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex-shrink:0}
  .bar-track{flex:1;background:#f1f5f9;border-radius:4px;height:8px}
  .bar-fill{height:8px;border-radius:4px;transition:width 0.4s ease}
  .auc-val{font-size:12px;color:var(--muted);width:44px;text-align:right;flex-shrink:0}
  .best-pill{font-size:9px;padding:1px 6px;background:#dbeafe;color:#1d4ed8;border-radius:20px;font-weight:600}
 
  /* ── KV rows ── */
  .kv-row{display:flex;justify-content:space-between;align-items:center;padding:9px 0;border-bottom:1px solid var(--border);font-size:13px}
  .kv-row:last-child{border-bottom:none}
  .kv-key{color:var(--muted)}
  .kv-val{font-weight:600}
 
  /* ── Buttons ── */
  .cta-btn{display:block;width:100%;padding:12px;background:var(--accent);color:#fff;border:none;border-radius:var(--radius-sm);font-size:14px;font-weight:600;cursor:pointer;margin-top:16px;transition:background 0.15s,transform 0.1s;letter-spacing:0.01em}
  .cta-btn:hover{background:#1e40af}
  .cta-btn:active{transform:scale(0.98)}
  .cta-btn.secondary{background:#fff;color:var(--accent);border:1.5px solid var(--accent);margin-top:8px}
  .cta-btn.secondary:hover{background:#eff6ff}
 
  /* ── Notes ── */
  .note-box{margin-top:14px;padding:12px 14px;background:#f8fafc;border-radius:var(--radius-sm);border-left:3px solid var(--accent);font-size:12px;color:var(--muted);line-height:1.6}
  .note-box.warn{border-color:var(--warn);background:#fffbeb}
  .note-box.danger{border-color:var(--danger);background:#fef2f2}
 
  /* ── Timeline ── */
  .timeline{position:relative;padding-left:20px}
  .timeline::before{content:'';position:absolute;left:6px;top:8px;bottom:8px;width:2px;background:var(--border)}
  .tl-item{position:relative;padding:0 0 14px 14px;font-size:12px}
  .tl-item:last-child{padding-bottom:0}
  .tl-dot{position:absolute;left:-14px;top:3px;width:10px;height:10px;border-radius:50%;border:2px solid #fff;box-shadow:0 0 0 2px var(--border)}
  .tl-item.done .tl-dot{background:var(--success);box-shadow:0 0 0 2px var(--success)}
  .tl-item.active .tl-dot{background:var(--accent);box-shadow:0 0 0 2px var(--accent);animation:pulse 1.5s infinite}
  .tl-item.pending .tl-dot{background:#fff}
  @keyframes pulse{0%,100%{box-shadow:0 0 0 2px var(--accent)}50%{box-shadow:0 0 0 4px rgba(26,86,219,0.25)}}
  .tl-label{font-weight:600;color:var(--text)}
  .tl-meta{color:var(--muted);margin-top:1px}
 
  /* ── Scorecard factors ── */
  .factor-row{display:flex;align-items:center;gap:8px;padding:8px 0;border-bottom:1px solid var(--border);font-size:12px}
  .factor-row:last-child{border-bottom:none}
  .factor-name{flex:1;color:var(--muted)}
  .factor-pts{font-weight:700;min-width:44px;text-align:right}
  .factor-bar{flex:2;background:#f1f5f9;border-radius:3px;height:6px;overflow:hidden}
  .factor-fill{height:6px;border-radius:3px;transition:width 0.4s ease}
 
  /* ── SHAP ── */
  .shap-row{display:flex;align-items:center;gap:8px;margin-bottom:8px;font-size:12px}
  .shap-name{width:110px;flex-shrink:0;color:var(--muted)}
  .shap-bar-wrap{flex:1;display:flex;align-items:center;gap:2px}
  .shap-neg{height:8px;border-radius:3px 0 0 3px;background:#dc2626}
  .shap-pos{height:8px;border-radius:0 3px 3px 0;background:#2563eb}
  .shap-zero{width:2px;background:var(--border);height:12px;flex-shrink:0}
  .shap-val{width:44px;text-align:right;font-weight:600;flex-shrink:0}
 
  /* ── Risk matrix ── */
  .rm-cell{aspect-ratio:1;border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:9px;font-weight:600;color:#fff;cursor:default;transition:transform 0.15s}
  .rm-cell:hover{transform:scale(1.08)}
  .rm-low{background:#16a34a}
  .rm-mod{background:#d97706}
  .rm-high{background:#dc2626}
  .rm-active{outline:2px solid #1a1d23;outline-offset:1px}
 
  /* ── Reg items ── */
  .reg-item{display:flex;align-items:flex-start;gap:10px;padding:10px 0;border-bottom:1px solid var(--border);font-size:12px}
  .reg-item:last-child{border-bottom:none}
  .reg-icon{width:28px;height:28px;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0}
  .reg-body{flex:1}
  .reg-name{font-weight:600;color:var(--text)}
  .reg-desc{color:var(--muted);margin-top:2px;line-height:1.4}
 
  /* ── Queue table ── */
  .search-bar{display:flex;gap:8px;margin-bottom:12px}
  .search-bar input{flex:1;padding:8px 12px;border:1.5px solid var(--border);border-radius:var(--radius-sm);font-size:13px}
  .filter-btn{padding:8px 12px;border:1.5px solid var(--border);border-radius:var(--radius-sm);background:#fff;cursor:pointer;font-size:12px;font-weight:500;display:flex;align-items:center;gap:4px;color:var(--text)}
  .filter-btn:hover{border-color:var(--accent);color:var(--accent)}
  .loan-table{width:100%;border-collapse:collapse;font-size:12px}
  .loan-table th{text-align:left;padding:8px 10px;background:#f8fafc;border-bottom:1px solid var(--border);font-weight:600;color:var(--muted);text-transform:uppercase;font-size:10px;letter-spacing:0.05em;white-space:nowrap}
  .loan-table td{padding:9px 10px;border-bottom:1px solid var(--border);color:var(--text)}
  .loan-table tr:last-child td{border-bottom:none}
  .loan-table tr:hover td{background:#f8fafc}
  .loan-table .loan-id{font-weight:600;font-family:monospace}
  .loan-table tr.highlight-row td{background:#eff6ff!important}
 
  /* ── Modal ── */
  .modal-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.45);z-index:1000;align-items:center;justify-content:center;padding:16px}
  .modal-overlay.open{display:flex}
  .modal{background:var(--surface);border-radius:var(--radius);padding:24px;max-width:500px;width:100%;max-height:88vh;overflow-y:auto;position:relative}
  .modal-title{font-size:15px;font-weight:600;margin-bottom:4px}
  .modal-sub{font-size:12px;color:var(--muted);margin-bottom:16px}
  .modal-close{position:absolute;top:14px;right:14px;background:none;border:none;cursor:pointer;color:var(--muted);font-size:18px}
  .modal-section{margin-bottom:14px}
  .modal-section-title{font-size:11px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:8px}
 
  /* ── Form row ── */
  .form-row{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px}
  .form-field{display:flex;flex-direction:column;gap:5px}
  .form-label{font-size:11px;font-weight:500;color:var(--muted)}
  .form-input{padding:9px 12px;border:1.5px solid var(--border);border-radius:var(--radius-sm);font-size:13px;font-weight:500;color:var(--text);background:#fafafa;-webkit-appearance:none}
  .form-input:focus{outline:none;border-color:var(--accent);background:#fff}
  .form-select{padding:9px 12px;border:1.5px solid var(--border);border-radius:var(--radius-sm);font-size:13px;font-weight:500;color:var(--text);background:#fafafa;-webkit-appearance:none;appearance:none;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24'%3E%3Cpath fill='%236b7280' d='M7 10l5 5 5-5z'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 10px center;width:100%}
  .form-select:focus{outline:none;border-color:var(--accent)}
  .form-divider{grid-column:1/-1;border:none;border-top:1px solid var(--border);margin:4px 0}
 
  /* ── Responsive ── */
  @media(max-width:992px){
    .shell{padding:10px}
    .header{padding:12px 16px;margin-bottom:12px}
    .header-icon{width:36px;height:36px;font-size:18px}
    .header-title{font-size:15px}
    .header-sub{font-size:10px}
    .metric-strip{gap:6px;margin-bottom:12px}
    .metric-card{padding:8px 4px}
    .metric-val{font-size:clamp(13px,2vw,18px)}
    .metric-lbl{font-size:8px;margin-top:4px}
    .tabs{padding:3px;margin-bottom:12px}
    .tab{padding:8px 10px;font-size:11.5px;min-width:72px}
    .two-col{gap:12px}
    .three-col{gap:10px}
    .card{padding:14px 16px}
    .card+.card{margin-top:12px}
    .card-title{font-size:11px;margin-bottom:12px}
    .param-grid{gap:12px;margin-bottom:14px}
    input[type="number"],select{padding:8px 10px;font-size:13px}
    .result-box{padding:18px;margin-top:12px}
    .result-score{font-size:44px}
    .model-name{width:120px}
  }
  @media(max-width:768px){
    .shell{padding:12px}
    .two-col{grid-template-columns:1fr}
    .three-col{grid-template-columns:1fr 1fr}
    .metric-strip{grid-template-columns:repeat(3,minmax(0,1fr))}
    .metric-strip .metric-card:nth-child(4),
    .metric-strip .metric-card:nth-child(5){display:none}
    .header-sub{display:none}
    .header-actions{flex-wrap:wrap}
    .summary-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
    .card{width:100%}
    .loan-table .hide-mobile{display:none}
    .form-row{grid-template-columns:1fr}
    .shap-name{width:80px}
  }
  @media(max-width:480px){
    .shell{padding:10px}
    .metric-strip{grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
    .metric-strip .metric-card:nth-child(3),
    .metric-strip .metric-card:nth-child(4),
    .metric-strip .metric-card:nth-child(5){display:none}
    .metric-val{font-size:18px}
    .param-grid{grid-template-columns:1fr}
    .three-col{grid-template-columns:1fr}
    .gauge-labels{font-size:8px}
    .result-score{font-size:40px}
    .flag-item{font-size:12px}
    .donut-wrap{height:180px}
    .model-name{width:100px}
    .card{padding:14px}
    .tabs{padding:2px}
    .tab{font-size:11px;padding:8px;min-width:60px}
    .header{padding:12px 14px}
    .header-title{font-size:14px}
    .header-icon{width:34px;height:34px;font-size:17px}
    .header-actions{display:none}
    .summary-grid{grid-template-columns:1fr 1fr}
    .form-row{grid-template-columns:1fr}
  }
  @media(max-width:360px){
    .tab i{display:none}
    .tab{min-width:50px;font-size:10.5px;padding:8px 6px}
    .header{padding:10px 12px}
    .header-icon{width:30px;height:30px;font-size:15px}
    .header-title{font-size:13px}
  }
</style>
</head>
<body>
<div class="shell">
 
  <div class="alert-banner" id="alert-banner">
    <i class="ti ti-alert-triangle"></i>
    <span id="alert-text">High concentration of elevated risk loans detected.</span>
    <span class="alert-close" onclick="document.getElementById('alert-banner').classList.remove('show')"><i class="ti ti-x"></i></span>
  </div>
 
  <!-- ── Header ── -->
  <div class="header">
    <div class="header-icon"><i class="ti ti-building-bank"></i></div>
    <div class="header-body">
      <div class="header-title">Credit Risk Scoring Dashboard</div>
      <div class="header-sub">Logistic Regression &nbsp;·&nbsp; ROC-AUC 0.640 &nbsp;·&nbsp; 10,000 loans &nbsp;·&nbsp; 1.78% default rate &nbsp;·&nbsp; ECOA / FCRA Compliant</div>
    </div>
    <div class="header-actions">
      <button class="header-btn" onclick="openModal('report-modal')"><i class="ti ti-file-report"></i> Report</button>
      <button class="header-btn primary" onclick="openModal('new-app-modal')"><i class="ti ti-plus"></i> New Application</button>
    </div>
  </div>
 
  <!-- ── Metric Strip ── -->
  <div class="metric-strip">
    <div class="metric-card" onclick="switchTab('portfolio')">
      <div class="metric-val" id="low-count-val">—</div>
      <div class="metric-lbl"><span class="badge b-green">✓ Low Risk</span></div>
    </div>
    <div class="metric-card" onclick="switchTab('portfolio')">
      <div class="metric-val" id="mod-count-val">—</div>
      <div class="metric-lbl"><span class="badge b-amber">⚠ Moderate</span></div>
    </div>
    <div class="metric-card" onclick="switchTab('portfolio')">
      <div class="metric-val" id="elev-count-val">—</div>
      <div class="metric-lbl"><span class="badge b-orange">~ Elevated</span></div>
    </div>
    <div class="metric-card" onclick="switchTab('portfolio')">
      <div class="metric-val" id="high-count-val">—</div>
      <div class="metric-lbl"><span class="badge b-red">✕ High Risk</span></div>
    </div>
    <div class="metric-card" onclick="switchTab('models')">
      <div class="metric-val">0.640</div>
      <div class="metric-lbl"><span class="badge b-blue">ROC-AUC</span></div>
    </div>
  </div>
 
  <!-- ── Tabs ── -->
  <div class="tabs">
    <button class="tab active" onclick="switchTab('score')"><i class="ti ti-search"></i> Score</button>
    <button class="tab" onclick="switchTab('portfolio')"><i class="ti ti-chart-pie"></i> Portfolio</button>
    <button class="tab" onclick="switchTab('models')"><i class="ti ti-chart-bar"></i> Models</button>
    <button class="tab" onclick="switchTab('compliance')"><i class="ti ti-shield-check"></i> Compliance</button>
    <button class="tab" onclick="switchTab('queue')"><i class="ti ti-list"></i> Queue</button>
  </div>
 
  <!-- ══════════ SCORE PANEL ══════════ -->
  <div id="panel-score" class="panel active">
    <div id="applicant-badge-score" style="display:none"></div>
    <div class="two-col">
      <div>
        <div class="card">
          <div class="card-title"><i class="ti ti-sliders"></i> Applicant Parameters</div>
          <div class="param-grid">
            <div class="param-field">
              <div class="param-label">Annual income ($)</div>
              <input type="number" id="income" value="85000" min="0" step="5000" oninput="recalc()"/>
            </div>
            <div class="param-field">
              <div class="param-label">Loan amount ($)</div>
              <input type="number" id="loanamt" value="15000" min="0" step="1000" oninput="recalc()"/>
            </div>
            <div class="param-field">
              <div class="param-label">Interest rate <span class="val-badge" id="rate-out">10.5%</span></div>
              <input type="range" id="rate" min="5" max="30" step="0.5" value="10.5"
                oninput="document.getElementById('rate-out').textContent=this.value+'%';recalc()"/>
            </div>
            <div class="param-field">
              <div class="param-label">Debt-to-income <span class="val-badge" id="dti-out">2%</span></div>
              <input type="range" id="dti" min="0" max="60" step="1" value="2"
                oninput="document.getElementById('dti-out').textContent=this.value+'%';recalc()"/>
            </div>
            <div class="param-field">
              <div class="param-label">Delinquencies (2yr) <span class="val-badge" id="delinq-out">1</span></div>
              <input type="range" id="delinq" min="0" max="10" step="1" value="1"
                oninput="document.getElementById('delinq-out').textContent=this.value;recalc()"/>
            </div>
            <div class="param-field">
              <div class="param-label">Credit history (yrs) <span class="val-badge" id="credyrs-out">7</span></div>
              <input type="range" id="credyrs" min="0" max="30" step="1" value="7"
                oninput="document.getElementById('credyrs-out').textContent=this.value;recalc()"/>
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
            <div class="param-field">
              <div class="param-label">Loan purpose</div>
              <select id="purpose" onchange="recalc()">
                <option value="1">Debt consolidation</option>
                <option value="2" selected>Home improvement</option>
                <option value="3">Business</option>
                <option value="4">Education</option>
                <option value="5">Medical</option>
                <option value="6">Other</option>
              </select>
            </div>
          </div>
 
          <div class="gauge-wrap">
            <div class="gauge-bar"><div class="gauge-marker" id="gauge-marker" style="left:75%"></div></div>
            <div class="gauge-labels">
              <span>High risk (0)</span><span>250</span><span>500</span><span>750</span><span>Low risk (1000)</span>
            </div>
          </div>
 
          <div class="result-box" id="result-box">
            <div class="result-score"    id="result-score">—</div>
            <div class="result-decision" id="result-decision">—</div>
            <div class="result-prob"     id="result-prob">—</div>
            <div class="result-meta"     id="result-meta">—</div>
          </div>
 
          <div class="compliance-strip">
            <i class="ti ti-shield-check"></i>
            <div><strong>ECOA/FCRA Compliant:</strong> This scoring model uses only permitted credit variables. Race, sex, religion, national origin, and age are not factors in this decision.</div>
          </div>
 
          <div class="adverse-box" id="adverse-box" style="display:none">
            <div class="adverse-title"><i class="ti ti-alert-circle"></i> Adverse Action Notice (ECOA Reg B)</div>
            <div style="margin-bottom:6px;font-size:11px">Primary reasons for adverse action:</div>
            <ul class="adverse-list" id="adverse-list"></ul>
            <div style="margin-top:8px;font-size:11px;opacity:0.75">Applicant has the right to a free copy of their credit report. Contact: risk@bank.com | 1-800-555-0100</div>
          </div>
        </div>
      </div>
 
      <div>
        <div class="card">
          <div class="card-title"><i class="ti ti-flag"></i> Risk Factor Analysis</div>
          <div id="risk-flags"></div>
        </div>
        <div class="card">
          <div class="card-title"><i class="ti ti-calculator"></i> Scorecard Points</div>
          <div id="scorecard-rows"></div>
          <div style="display:flex;justify-content:space-between;align-items:center;padding-top:10px;border-top:1px solid var(--border);margin-top:4px;font-size:13px">
            <span style="font-weight:600">Total Score</span>
            <span style="font-weight:700;font-size:16px" id="scorecard-total">—</span>
          </div>
        </div>
        <div class="card">
          <div class="card-title"><i class="ti ti-chart-bar"></i> Default Probability Breakdown</div>
          <div class="bar-chart-wrap"><canvas id="barChart"></canvas></div>
        </div>
        <div class="card">
          <div class="card-title"><i class="ti ti-git-branch"></i> Approval Workflow</div>
          <div class="timeline" id="workflow-timeline"></div>
        </div>
      </div>
    </div>
  </div>
 
  <!-- ══════════ PORTFOLIO PANEL ══════════ -->
  <div id="panel-portfolio" class="panel">
    <div id="applicant-badge-portfolio" style="display:none;margin-bottom:12px"></div>
    <div class="three-col" style="margin-bottom:14px">
      <div class="card" style="text-align:center;padding:14px">
        <div style="font-size:11px;color:var(--muted);margin-bottom:4px">Portfolio Default Rate</div>
        <div style="font-size:26px;font-weight:700;color:var(--danger)" id="port-default-rate">—</div>
        <div style="font-size:11px;color:var(--muted);margin-top:4px" id="port-defaults-abs">—</div>
      </div>
      <div class="card" style="text-align:center;padding:14px">
        <div style="font-size:11px;color:var(--muted);margin-bottom:4px">Expected Loss (EL)</div>
        <div style="font-size:26px;font-weight:700;color:var(--warn)" id="port-el">—</div>
        <div style="font-size:11px;color:var(--muted);margin-top:4px">Avg LGD 45% assumed</div>
      </div>
      <div class="card" style="text-align:center;padding:14px">
        <div style="font-size:11px;color:var(--muted);margin-bottom:4px">Approval Rate</div>
        <div style="font-size:26px;font-weight:700;color:var(--success)" id="port-approval-rate">—</div>
        <div style="font-size:11px;color:var(--muted);margin-top:4px" id="port-approved-abs">—</div>
      </div>
    </div>
    <div class="two-col">
      <div>
        <div class="card">
          <div class="card-title"><i class="ti ti-chart-donut"></i> Risk Tier Breakdown</div>
          <div class="donut-wrap"><canvas id="donutChart"></canvas></div>
        </div>
        <div class="card">
          <div class="card-title"><i class="ti ti-trending-up"></i> Score Distribution</div>
          <div class="line-wrap"><canvas id="distChart"></canvas></div>
        </div>
      </div>
      <div class="card">
        <div class="card-title"><i class="ti ti-list-details"></i> Tier Details</div>
        <div class="tier-row">
          <div class="tier-left"><div class="tier-dot" style="background:#16a34a"></div><span>Low risk</span></div>
          <span class="tier-count" id="low-count-lbl">—</span>
          <span class="badge b-green">Approve</span>
        </div>
        <div class="tier-row">
          <div class="tier-left"><div class="tier-dot" style="background:#d97706"></div><span>Moderate risk</span></div>
          <span class="tier-count" id="mod-count-lbl">—</span>
          <span class="badge b-amber">Conditions</span>
        </div>
        <div class="tier-row">
          <div class="tier-left"><div class="tier-dot" style="background:#ea580c"></div><span>Elevated risk</span></div>
          <span class="tier-count" id="elev-count-lbl">—</span>
          <span class="badge b-orange">Review</span>
        </div>
        <div class="tier-row">
          <div class="tier-left"><div class="tier-dot" style="background:#dc2626"></div><span>High risk</span></div>
          <span class="tier-count" id="high-count-lbl">—</span>
          <span class="badge b-red">Decline</span>
        </div>
        <div style="margin-top:14px;padding-top:12px;border-top:1px solid var(--border);font-size:12px;color:var(--muted);line-height:1.8">
          <div>Dataset default rate: <b style="color:var(--text)">1.78%</b></div>
          <div>Total scored: <b style="color:var(--text)" id="port-total-scored">2,000</b></div>
        </div>
        <div style="margin-top:14px;padding-top:14px;border-top:1px solid var(--border)">
          <div class="card-title" style="margin-bottom:10px"><i class="ti ti-alert-triangle"></i> Concentration Risk</div>
          <div id="concentration-flags"></div>
        </div>
        <div style="margin-top:14px;padding-top:14px;border-top:1px solid var(--border)">
          <div class="card-title" style="margin-bottom:8px"><i class="ti ti-grid-dots"></i> Risk Matrix (Grade × DTI)</div>
          <div style="display:flex;gap:4px;margin-bottom:4px;font-size:10px;color:var(--muted)">
            <span style="width:20px"></span>
            <span style="flex:1;text-align:center">Low</span>
            <span style="flex:1;text-align:center">Mid</span>
            <span style="flex:1;text-align:center">High</span>
            <span style="flex:1;text-align:center">V.High</span>
          </div>
          <div id="risk-matrix"></div>
          <div style="display:flex;gap:8px;margin-top:8px;font-size:10px;color:var(--muted)">
            <span><span style="display:inline-block;width:8px;height:8px;background:#16a34a;border-radius:2px;margin-right:3px"></span>Low</span>
            <span><span style="display:inline-block;width:8px;height:8px;background:#d97706;border-radius:2px;margin-right:3px"></span>Moderate</span>
            <span><span style="display:inline-block;width:8px;height:8px;background:#dc2626;border-radius:2px;margin-right:3px"></span>High</span>
          </div>
        </div>
      </div>
    </div>
  </div>
 
  <!-- ══════════ MODELS PANEL ══════════ -->
  <div id="panel-models" class="panel">
    <div id="applicant-badge-models" style="display:none;margin-bottom:12px"></div>
    <div class="two-col">
      <div>
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
          <div class="model-row">
            <div class="model-name">Decision Tree</div>
            <div class="bar-track"><div class="bar-fill" style="width:45%;background:#d97706"></div></div>
            <div class="auc-val">0.5741</div>
          </div>
          <div class="model-row">
            <div class="model-name">Naive Bayes</div>
            <div class="bar-track"><div class="bar-fill" style="width:38%;background:#9333ea"></div></div>
            <div class="auc-val">0.5502</div>
          </div>
          <div class="note-box">
            <b style="color:var(--text)">Note on AUC:</b> Only 178 defaults in 10,000 loans (1.78%). The test set holds ~35 defaults, making ROC-AUC noisier at small scale. All models beat random chance (0.5).
          </div>
        </div>
        <div class="card">
          <div class="card-title"><i class="ti ti-antenna"></i> SHAP Feature Importance <span id="shap-applicant-note" style="font-size:10px;color:var(--accent);font-weight:400;text-transform:none;letter-spacing:0;margin-left:4px"></span></div>
          <div style="display:flex;gap:8px;font-size:10px;color:var(--muted);margin-bottom:10px">
            <span><span style="display:inline-block;width:20px;height:6px;background:#dc2626;border-radius:2px;margin-right:3px;vertical-align:middle"></span>Risk-increasing</span>
            <span><span style="display:inline-block;width:20px;height:6px;background:#2563eb;border-radius:2px;margin-right:3px;vertical-align:middle"></span>Risk-reducing</span>
          </div>
          <div id="shap-rows"></div>
        </div>
        <div class="card">
          <div class="card-title"><i class="ti ti-chart-line"></i> ROC Curve</div>
          <div class="line-wrap"><canvas id="rocChart"></canvas></div>
        </div>
      </div>
      <div>
        <div class="card">
          <div class="card-title"><i class="ti ti-info-circle"></i> Key Metrics — Current Applicant</div>
          <div class="kv-row"><span class="kv-key">Applicant name</span>    <span class="kv-val" id="mdl-name">—</span></div>
          <div class="kv-row"><span class="kv-key">Loan ID</span>            <span class="kv-val" id="mdl-id">—</span></div>
          <div class="kv-row"><span class="kv-key">Credit score</span>       <span class="kv-val" id="mdl-score">—</span></div>
          <div class="kv-row"><span class="kv-key">P(Default)</span>         <span class="kv-val" id="mdl-pd">—</span></div>
          <div class="kv-row"><span class="kv-key">Decision</span>           <span class="kv-val" id="mdl-decision">—</span></div>
          <div class="kv-row"><span class="kv-key">Income</span>             <span class="kv-val" id="mdl-income">—</span></div>
          <div class="kv-row"><span class="kv-key">Loan amount</span>        <span class="kv-val" id="mdl-loanamt">—</span></div>
          <div class="kv-row"><span class="kv-key">DTI</span>                <span class="kv-val" id="mdl-dti">—</span></div>
          <div class="kv-row"><span class="kv-key">Grade</span>              <span class="kv-val" id="mdl-grade">—</span></div>
          <div class="kv-row"><span class="kv-key">Dataset size</span>       <span class="kv-val">10,000 loans</span></div>
          <div class="kv-row"><span class="kv-key">Train / test split</span> <span class="kv-val">80% / 20%</span></div>
          <div class="kv-row"><span class="kv-key">Imbalance handling</span> <span class="kv-val">Class weight balanced</span></div>
          <div class="kv-row"><span class="kv-key">Explainability</span>     <span class="kv-val">SHAP TreeExplainer</span></div>
          <div class="kv-row"><span class="kv-key">Last trained</span>       <span class="kv-val">2025-06-01</span></div>
          <button class="cta-btn">Improve Model AUC ↗</button>
          <button class="cta-btn secondary">Download Model Card</button>
        </div>
        <div class="card">
          <div class="card-title"><i class="ti ti-table"></i> Confusion Matrix (Test Set)</div>
          <div style="overflow-x:auto">
            <table style="width:100%;border-collapse:collapse;font-size:12px;text-align:center">
              <thead><tr>
                <th style="padding:8px;border:1px solid var(--border);background:#f8fafc;color:var(--muted)"></th>
                <th style="padding:8px;border:1px solid var(--border);background:#f8fafc;color:var(--muted)">Pred: No Default</th>
                <th style="padding:8px;border:1px solid var(--border);background:#f8fafc;color:var(--muted)">Pred: Default</th>
              </tr></thead>
              <tbody>
                <tr>
                  <td style="padding:8px;border:1px solid var(--border);font-weight:600;background:#f8fafc">Actual: No Default</td>
                  <td style="padding:8px;border:1px solid var(--border);background:#dcfce7;font-weight:700;color:#15803d">1,927<br><span style="font-size:10px;font-weight:400">True Neg</span></td>
                  <td style="padding:8px;border:1px solid var(--border);background:#fef2f2;font-weight:700;color:#b91c1c">38<br><span style="font-size:10px;font-weight:400">False Pos</span></td>
                </tr>
                <tr>
                  <td style="padding:8px;border:1px solid var(--border);font-weight:600;background:#f8fafc">Actual: Default</td>
                  <td style="padding:8px;border:1px solid var(--border);background:#fef2f2;font-weight:700;color:#b91c1c">18<br><span style="font-size:10px;font-weight:400">False Neg</span></td>
                  <td style="padding:8px;border:1px solid var(--border);background:#dcfce7;font-weight:700;color:#15803d">17<br><span style="font-size:10px;font-weight:400">True Pos</span></td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="three-col" style="margin-top:10px;gap:8px">
            <div style="text-align:center;background:#f8fafc;border-radius:6px;padding:8px"><div style="font-size:18px;font-weight:700">48.6%</div><div style="font-size:10px;color:var(--muted)">Precision</div></div>
            <div style="text-align:center;background:#f8fafc;border-radius:6px;padding:8px"><div style="font-size:18px;font-weight:700">31.0%</div><div style="font-size:10px;color:var(--muted)">Recall</div></div>
            <div style="text-align:center;background:#f8fafc;border-radius:6px;padding:8px"><div style="font-size:18px;font-weight:700">37.8%</div><div style="font-size:10px;color:var(--muted)">F1 Score</div></div>
          </div>
        </div>
      </div>
    </div>
  </div>
 
  <!-- ══════════ COMPLIANCE PANEL ══════════ -->
  <div id="panel-compliance" class="panel">
    <div id="applicant-badge-compliance" style="display:none;margin-bottom:12px"></div>
    <div class="two-col">
      <div>
        <div class="card">
          <div class="card-title"><i class="ti ti-shield-check"></i> Regulatory Framework</div>
          <div class="reg-item">
            <div class="reg-icon" style="background:#dcfce7;color:#15803d"><i class="ti ti-check"></i></div>
            <div class="reg-body"><div class="reg-name">Equal Credit Opportunity Act (ECOA / Reg B)</div><div class="reg-desc">Model uses only permitted variables. Adverse action notices generated automatically on decline. No prohibited factors included.</div></div>
          </div>
          <div class="reg-item">
            <div class="reg-icon" style="background:#dcfce7;color:#15803d"><i class="ti ti-check"></i></div>
            <div class="reg-body"><div class="reg-name">Fair Credit Reporting Act (FCRA)</div><div class="reg-desc">Credit data obtained only from permissible-purpose CRAs. Applicants notified of right to free credit report on adverse action.</div></div>
          </div>
          <div class="reg-item">
            <div class="reg-icon" style="background:#dcfce7;color:#15803d"><i class="ti ti-check"></i></div>
            <div class="reg-body"><div class="reg-name">Community Reinvestment Act (CRA)</div><div class="reg-desc">Lending patterns monitored quarterly. LMI geography distribution tracked in portfolio analytics.</div></div>
          </div>
          <div class="reg-item">
            <div class="reg-icon" style="background:#fef3c7;color:#92400e"><i class="ti ti-clock"></i></div>
            <div class="reg-body"><div class="reg-name">Basel III / IRB Approach</div><div class="reg-desc">PD/LGD/EAD framework partially implemented. Capital adequacy pending final model validation. Target: SR 11-7 compliant Q4 2025.</div></div>
          </div>
          <div class="reg-item">
            <div class="reg-icon" style="background:#dcfce7;color:#15803d"><i class="ti ti-check"></i></div>
            <div class="reg-body"><div class="reg-name">Model Risk Management (SR 11-7)</div><div class="reg-desc">Independent model validation completed. Annual review scheduled. Documentation includes conceptual soundness and outcomes analysis.</div></div>
          </div>
        </div>
        <div class="card">
          <div class="card-title"><i class="ti ti-report-analytics"></i> Disparate Impact — Current Applicant Decision</div>
          <div id="compliance-applicant-summary" style="margin-bottom:12px"></div>
          <table style="width:100%;border-collapse:collapse;font-size:12px">
            <thead><tr style="background:#f8fafc">
              <th style="padding:8px;border-bottom:1px solid var(--border);text-align:left;color:var(--muted);font-size:10px;text-transform:uppercase;letter-spacing:0.05em">Group</th>
              <th style="padding:8px;border-bottom:1px solid var(--border);text-align:center;color:var(--muted);font-size:10px;text-transform:uppercase;letter-spacing:0.05em">Approval Rate</th>
              <th style="padding:8px;border-bottom:1px solid var(--border);text-align:center;color:var(--muted);font-size:10px;text-transform:uppercase;letter-spacing:0.05em">4/5 Ratio</th>
              <th style="padding:8px;border-bottom:1px solid var(--border);text-align:center;color:var(--muted);font-size:10px;text-transform:uppercase;letter-spacing:0.05em">Status</th>
            </tr></thead>
            <tbody>
              <tr><td style="padding:8px;border-bottom:1px solid var(--border)">Reference group</td><td style="padding:8px;border-bottom:1px solid var(--border);text-align:center;font-weight:600">72.4%</td><td style="padding:8px;border-bottom:1px solid var(--border);text-align:center">—</td><td style="padding:8px;border-bottom:1px solid var(--border);text-align:center"><span class="badge b-gray">Baseline</span></td></tr>
              <tr><td style="padding:8px;border-bottom:1px solid var(--border)">Group A</td><td style="padding:8px;border-bottom:1px solid var(--border);text-align:center;font-weight:600">68.1%</td><td style="padding:8px;border-bottom:1px solid var(--border);text-align:center">94.1%</td><td style="padding:8px;border-bottom:1px solid var(--border);text-align:center"><span class="badge b-green">Pass</span></td></tr>
              <tr><td style="padding:8px;border-bottom:1px solid var(--border)">Group B</td><td style="padding:8px;border-bottom:1px solid var(--border);text-align:center;font-weight:600">61.3%</td><td style="padding:8px;border-bottom:1px solid var(--border);text-align:center">84.7%</td><td style="padding:8px;border-bottom:1px solid var(--border);text-align:center"><span class="badge b-green">Pass</span></td></tr>
              <tr><td style="padding:8px;border-bottom:1px solid var(--border)">Group C</td><td style="padding:8px;border-bottom:1px solid var(--border);text-align:center;font-weight:600">57.8%</td><td style="padding:8px;border-bottom:1px solid var(--border);text-align:center">79.8%</td><td style="padding:8px;border-bottom:1px solid var(--border);text-align:center"><span class="badge b-amber">Monitor</span></td></tr>
              <tr><td style="padding:8px">Group D</td><td style="padding:8px;text-align:center;font-weight:600">65.9%</td><td style="padding:8px;text-align:center">91.0%</td><td style="padding:8px;text-align:center"><span class="badge b-green">Pass</span></td></tr>
            </tbody>
          </table>
          <div class="note-box warn" style="margin-top:10px">Group C approaching 80% threshold. Enhanced monitoring and root-cause analysis recommended.</div>
        </div>
      </div>
      <div>
        <div class="card">
          <div class="card-title"><i class="ti ti-check"></i> Model Governance Checklist</div>
          <div id="governance-checklist"></div>
        </div>
        <div class="card">
          <div class="card-title"><i class="ti ti-history"></i> Audit Log</div>
          <div id="audit-log-entries" style="font-size:12px"></div>
        </div>
        <div class="card">
          <div class="card-title"><i class="ti ti-bell"></i> Monitoring Alerts</div>
          <div class="reg-item">
            <div class="reg-icon" style="background:#dcfce7;color:#15803d"><i class="ti ti-check"></i></div>
            <div class="reg-body"><div class="reg-name">Population Stability Index (PSI)</div><div class="reg-desc">PSI = 0.04 — Stable. Threshold &lt; 0.10. No model redevelopment required.</div></div>
          </div>
          <div class="reg-item">
            <div class="reg-icon" style="background:#dcfce7;color:#15803d"><i class="ti ti-check"></i></div>
            <div class="reg-body"><div class="reg-name">Gini Coefficient Drift</div><div class="reg-desc">Current Gini: 0.280. Baseline: 0.271. Within ±5% tolerance.</div></div>
          </div>
          <div class="reg-item">
            <div class="reg-icon" style="background:#fef3c7;color:#92400e"><i class="ti ti-clock"></i></div>
            <div class="reg-body"><div class="reg-name">Vintage Analysis</div><div class="reg-desc">2024 Q4 vintage showing 2.1% 90-DPD at 6 months. Above 1.8% baseline — scheduled for review.</div></div>
          </div>
        </div>
      </div>
    </div>
  </div>
 
  <!-- ══════════ QUEUE PANEL ══════════ -->
  <div id="panel-queue" class="panel">
    <div id="applicant-badge-queue" style="display:none;margin-bottom:12px"></div>
    <div class="card" style="margin-bottom:14px">
      <div class="card-title"><i class="ti ti-list"></i> Pending Applications</div>
      <div class="search-bar">
        <input type="text" placeholder="Search by ID, name, grade, or decision…" oninput="filterQueue(this.value)"/>
        <button class="filter-btn" onclick="filterQueue('')"><i class="ti ti-refresh"></i></button>
      </div>
      <div style="overflow-x:auto">
        <table class="loan-table" id="queue-table">
          <thead><tr>
            <th>Loan ID</th>
            <th>Applicant</th>
            <th>Score</th>
            <th class="hide-mobile">Grade</th>
            <th class="hide-mobile">P(Default)</th>
            <th>Decision</th>
            <th class="hide-mobile">Income</th>
            <th>Action</th>
          </tr></thead>
          <tbody id="queue-body"></tbody>
        </table>
      </div>
      <div style="margin-top:12px;font-size:12px;color:var(--muted)" id="queue-footer">Showing loans in queue</div>
    </div>
    <div class="two-col">
      <div class="card">
        <div class="card-title"><i class="ti ti-clock"></i> Processing Summary</div>
        <div class="kv-row"><span class="kv-key">Pending review</span>     <span class="kv-val" id="q-pending">—</span></div>
        <div class="kv-row"><span class="kv-key">Auto-approved today</span> <span class="kv-val" id="q-approved">—</span></div>
        <div class="kv-row"><span class="kv-key">Auto-declined today</span> <span class="kv-val" id="q-declined">—</span></div>
        <div class="kv-row"><span class="kv-key">Manual review</span>       <span class="kv-val" id="q-review">—</span></div>
        <div class="kv-row"><span class="kv-key">Avg decision time</span>   <span class="kv-val">4.2 min</span></div>
        <div class="kv-row"><span class="kv-key">SLA breach risk</span>     <span class="kv-val"><span class="badge b-green">None</span></span></div>
      </div>
      <div class="card">
        <div class="card-title"><i class="ti ti-git-branch"></i> Decision Distribution (Today)</div>
        <div class="line-wrap"><canvas id="decisionChart"></canvas></div>
      </div>
    </div>
  </div>
 
</div><!-- /.shell -->
 
<!-- ══ NEW APPLICATION MODAL ══ -->
<div class="modal-overlay" id="new-app-modal">
  <div class="modal">
    <button class="modal-close" onclick="closeModal('new-app-modal')"><i class="ti ti-x"></i></button>
    <div class="modal-title">New Loan Application</div>
    <div class="modal-sub">Enter all applicant details. The application will populate and score across every tab instantly.</div>
 
    <div class="modal-section">
      <div class="modal-section-title">Applicant Identity</div>
      <div class="form-row">
        <div class="form-field">
          <label class="form-label">Full Name *</label>
          <input type="text" class="form-input" id="new-name" placeholder="e.g. Jane Smith"/>
        </div>
        <div class="form-field">
          <label class="form-label">Loan ID *</label>
          <input type="text" class="form-input" id="new-lid" placeholder="e.g. LN-2025-0048"/>
        </div>
      </div>
    </div>
 
    <div class="modal-section">
      <div class="modal-section-title">Financial Profile</div>
      <div class="form-row">
        <div class="form-field">
          <label class="form-label">Annual Income ($) *</label>
          <input type="number" class="form-input" id="new-income" placeholder="75000" min="0" step="1000"/>
        </div>
        <div class="form-field">
          <label class="form-label">Loan Amount ($) *</label>
          <input type="number" class="form-input" id="new-loanamt" placeholder="20000" min="0" step="500"/>
        </div>
        <div class="form-field">
          <label class="form-label">Interest Rate (%)</label>
          <input type="number" class="form-input" id="new-rate" placeholder="12.5" min="5" max="30" step="0.5"/>
        </div>
        <div class="form-field">
          <label class="form-label">Debt-to-Income (%)</label>
          <input type="number" class="form-input" id="new-dti" placeholder="18" min="0" max="60" step="1"/>
        </div>
        <div class="form-field">
          <label class="form-label">Delinquencies (2yr)</label>
          <input type="number" class="form-input" id="new-delinq" placeholder="0" min="0" max="10" step="1"/>
        </div>
        <div class="form-field">
          <label class="form-label">Credit History (yrs)</label>
          <input type="number" class="form-input" id="new-credyrs" placeholder="5" min="0" max="40" step="1"/>
        </div>
      </div>
    </div>
 
    <div class="modal-section">
      <div class="modal-section-title">Loan Details</div>
      <div class="form-row">
        <div class="form-field">
          <label class="form-label">Loan Grade</label>
          <select class="form-select" id="new-grade">
            <option value="1">A — Prime</option>
            <option value="2" selected>B — Near prime</option>
            <option value="3">C — Subprime</option>
            <option value="4">D — Elevated</option>
            <option value="5">E — High risk</option>
          </select>
        </div>
        <div class="form-field">
          <label class="form-label">Loan Purpose</label>
          <select class="form-select" id="new-purpose">
            <option value="1">Debt consolidation</option>
            <option value="2" selected>Home improvement</option>
            <option value="3">Business</option>
            <option value="4">Education</option>
            <option value="5">Medical</option>
            <option value="6">Other</option>
          </select>
        </div>
      </div>
    </div>
 
    <div id="new-app-error" style="display:none;background:#fee2e2;color:#b91c1c;border-radius:6px;padding:10px 12px;font-size:12px;margin-bottom:8px"></div>
 
    <button class="cta-btn" onclick="submitNewApp()"><i class="ti ti-send"></i> Submit & Score Application</button>
    <button class="cta-btn secondary" onclick="closeModal('new-app-modal')">Cancel</button>
  </div>
</div>
 
<!-- ══ REPORT MODAL ══ -->
<div class="modal-overlay" id="report-modal">
  <div class="modal">
    <button class="modal-close" onclick="closeModal('report-modal')"><i class="ti ti-x"></i></button>
    <div class="modal-title">Full Credit Decision Report</div>
    <div class="modal-sub">Generated: <span id="report-date"></span></div>
    <div class="modal-section">
      <div class="modal-section-title">Score Summary</div>
      <div class="summary-grid">
        <div class="summary-item"><div class="s-lbl">Credit Score</div><div class="s-val" id="rpt-score">—</div></div>
        <div class="summary-item"><div class="s-lbl">P(Default)</div><div class="s-val" id="rpt-pd">—</div></div>
        <div class="summary-item"><div class="s-lbl">Decision</div><div class="s-val" id="rpt-decision">—</div></div>
      </div>
    </div>
    <div class="modal-section">
      <div class="modal-section-title">Application Data</div>
      <div class="kv-row"><span class="kv-key">Applicant</span>      <span class="kv-val" id="rpt-name">—</span></div>
      <div class="kv-row"><span class="kv-key">Loan ID</span>         <span class="kv-val" id="rpt-lid">—</span></div>
      <div class="kv-row"><span class="kv-key">Annual income</span>   <span class="kv-val" id="rpt-income">—</span></div>
      <div class="kv-row"><span class="kv-key">Loan amount</span>     <span class="kv-val" id="rpt-loanamt">—</span></div>
      <div class="kv-row"><span class="kv-key">Interest rate</span>   <span class="kv-val" id="rpt-rate">—</span></div>
      <div class="kv-row"><span class="kv-key">Debt-to-income</span> <span class="kv-val" id="rpt-dti">—</span></div>
      <div class="kv-row"><span class="kv-key">Delinquencies</span>  <span class="kv-val" id="rpt-delinq">—</span></div>
      <div class="kv-row"><span class="kv-key">Credit history</span> <span class="kv-val" id="rpt-credyrs">—</span></div>
      <div class="kv-row"><span class="kv-key">Loan grade</span>     <span class="kv-val" id="rpt-grade">—</span></div>
      <div class="kv-row"><span class="kv-key">Purpose</span>        <span class="kv-val" id="rpt-purpose">—</span></div>
    </div>
    <div class="modal-section">
      <div class="modal-section-title">Compliance Statement</div>
      <div style="font-size:12px;color:var(--muted);line-height:1.6">This report was generated in accordance with ECOA Regulation B and FCRA. Decision is based solely on credit-related factors. Applicant may request an explanation of any adverse decision within 60 days.</div>
    </div>
    <button class="cta-btn secondary" onclick="closeModal('report-modal')">Close</button>
  </div>
</div>
 
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<script>
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  CONSTANTS & LABELS
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
const GRADE_LABELS   = ['','A — Prime','B — Near prime','C — Subprime','D — Elevated','E — High risk'];
const GRADE_SHORT    = ['','A','B','C','D','E'];
const PURPOSE_LABELS = ['','Debt consolidation','Home improvement','Business','Education','Medical','Other'];
 
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  ACTIVE APPLICANT STATE (shared across all tabs)
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
let activeApplicant = null; // null = no custom applicant loaded
 
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  SEEDED RNG + PORTFOLIO SEED DATA
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
function seededRandom(seed) {
  let mw=(123456789+seed)&0xffffffff, mz=(987654321-seed)&0xffffffff;
  return function(){
    mz=(36969*(mz&65535)+(mz>>16))&0xffffffff;
    mw=(18000*(mw&65535)+(mw>>16))&0xffffffff;
    return ((((mz<<16)+mw)>>16)&0x7FFFFFFF)/0x7FFFFFFF;
  };
}
const rng=seededRandom(42);
const basePortfolio=[];
for(let i=0;i<2000;i++){
  const r=5+rng()*25,d=rng()*60,q=rng()>0.8?Math.floor(rng()*3):0,
        g=Math.floor(1+rng()*5),inc=30000+rng()*120000,
        cy=Math.floor(rng()*20),la=5000+rng()*45000,
        pur=Math.floor(1+rng()*6);
  const risk=Math.min(40,(r-5)/25*40)+Math.min(30,d/60*30)+(q*10)+((g-1)*8)-Math.min(15,(inc/100000)*15)-Math.min(5,cy/20*5)+([0,2,0,3,-1,1,1][pur]||0);
  const pDef=Math.min(0.98,Math.max(0.01,risk/100));
  basePortfolio.push({rate:r,dti:d,delinq:q,grade:g,income:inc,credyrs:cy,loanamt:la,purpose:pur,score:Math.round(1000*(1-pDef)),pDefault:pDef,name:'',lid:'',isApplicant:false});
}
 
// Working copy — slot 0 is the "current applicant" slot
let portfolioData=[...basePortfolio];
 
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  CHART HANDLES
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
let barChart,donutChart,distChart,rocChart,decisionChart;
 
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  SCORING ENGINE
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
function scoreApplicant(income,loanamt,rate,dti,delinq,grade,credyrs,purpose){
  const rateRisk   =Math.min(40,(rate-5)/25*40);
  const dtiRisk    =Math.min(30,dti/60*30);
  const delinqRisk =Math.min(30,delinq*10);
  const gradeRisk  =(grade-1)*8;
  const incomeBonus=Math.min(15,(income/100000)*15);
  const credBonus  =Math.min(5,credyrs/20*5);
  const purposeAdj =[0,2,0,3,-1,1,1][purpose]||0;
  const rawRisk    =rateRisk+dtiRisk+delinqRisk+gradeRisk+purposeAdj-incomeBonus-credBonus;
  const pDefault   =Math.min(0.98,Math.max(0.01,rawRisk/100));
  const score      =Math.round(1000*(1-pDefault));
  return{rateRisk,dtiRisk,delinqRisk,gradeRisk,incomeBonus,credBonus,purposeAdj,rawRisk,pDefault,score};
}
 
function decisionFromScore(score){
  if(score>=800) return{decision:'APPROVE',bg:'#dcfce7',color:'#15803d',badgeClass:'b-green'};
  if(score>=650) return{decision:'APPROVE WITH CONDITIONS',bg:'#fef3c7',color:'#92400e',badgeClass:'b-amber'};
  if(score>=500) return{decision:'MANUAL REVIEW',bg:'#ffedd5',color:'#c2410c',badgeClass:'b-orange'};
  return{decision:'DECLINE',bg:'#fee2e2',color:'#b91c1c',badgeClass:'b-red'};
}
 
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  APPLICANT BADGE (shown on every panel)
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
function renderApplicantBadges(){
  const panels=['score','portfolio','models','compliance','queue'];
  panels.forEach(p=>{
    const el=document.getElementById('applicant-badge-'+p);
    if(!el) return;
    if(!activeApplicant){el.style.display='none';el.innerHTML='';return;}
    const sc=activeApplicant.score;
    const{decision,badgeClass}=decisionFromScore(sc);
    const badgeHtml=`
      <div class="applicant-badge">
        <i class="ti ti-user-circle"></i>
        <span class="ab-name">${activeApplicant.name}</span>
        <span class="ab-id">${activeApplicant.lid}</span>
        <span class="badge ${badgeClass}" style="margin-left:8px">${decision}</span>
        <span style="font-size:12px;font-weight:700;margin-left:8px">${sc}</span>
        <span class="ab-clear" onclick="clearApplicant()">✕ Clear</span>
      </div>`;
    el.innerHTML=badgeHtml;
    el.style.display='block';
  });
}
 
function clearApplicant(){
  activeApplicant=null;
  // Reset Score inputs to defaults
  document.getElementById('income').value=85000;
  document.getElementById('loanamt').value=15000;
  document.getElementById('rate').value=10.5;
  document.getElementById('dti').value=2;
  document.getElementById('delinq').value=1;
  document.getElementById('credyrs').value=7;
  document.getElementById('grade').value=1;
  document.getElementById('purpose').value=2;
  document.getElementById('rate-out').textContent='10.5%';
  document.getElementById('dti-out').textContent='2%';
  document.getElementById('delinq-out').textContent='1';
  document.getElementById('credyrs-out').textContent='7';
  renderApplicantBadges();
  recalc();
}
 
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  TABS
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
const TAB_NAMES=['score','portfolio','models','compliance','queue'];
function switchTab(name){
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  document.querySelectorAll('.panel').forEach(p=>p.classList.remove('active'));
  const idx=TAB_NAMES.indexOf(name);
  document.querySelectorAll('.tab')[idx].classList.add('active');
  document.getElementById('panel-'+name).classList.add('active');
  if(name==='queue') renderQueue();
}
 
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  MODALS
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
function openModal(id){
  if(id==='report-modal') updateReport();
  document.getElementById(id).classList.add('open');
}
function closeModal(id){document.getElementById(id).classList.remove('open');}
document.querySelectorAll('.modal-overlay').forEach(el=>{
  el.addEventListener('click',e=>{if(e.target===el)el.classList.remove('open');});
});
 
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  SUBMIT NEW APPLICATION → drives ALL tabs
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
function submitNewApp(){
  const name   =document.getElementById('new-name').value.trim();
  const lid    =document.getElementById('new-lid').value.trim();
  const income =parseFloat(document.getElementById('new-income').value)||0;
  const loanamt=parseFloat(document.getElementById('new-loanamt').value)||0;
  const rate   =parseFloat(document.getElementById('new-rate').value)||10.5;
  const dti    =parseFloat(document.getElementById('new-dti').value)||0;
  const delinq =parseFloat(document.getElementById('new-delinq').value)||0;
  const credyrs=parseFloat(document.getElementById('new-credyrs').value)||5;
  const grade  =parseInt(document.getElementById('new-grade').value)||1;
  const purpose=parseInt(document.getElementById('new-purpose').value)||2;
 
  const errEl=document.getElementById('new-app-error');
 
  // Validate
  if(!name||!lid){errEl.style.display='block';errEl.textContent='Please enter applicant name and loan ID.';return;}
  if(income<=0){errEl.style.display='block';errEl.textContent='Please enter a valid annual income.';return;}
  if(loanamt<=0){errEl.style.display='block';errEl.textContent='Please enter a valid loan amount.';return;}
  errEl.style.display='none';
 
  // Score
  const result=scoreApplicant(income,loanamt,rate,dti,delinq,grade,credyrs,purpose);
  const{decision,badgeClass}=decisionFromScore(result.score);
 
  // Build applicant record
  activeApplicant={
    name,lid,income,loanamt,rate,dti,delinq,credyrs,grade,purpose,
    score:result.score,pDefault:result.pDefault,
    rateRisk:result.rateRisk,dtiRisk:result.dtiRisk,delinqRisk:result.delinqRisk,
    gradeRisk:result.gradeRisk,incomeBonus:result.incomeBonus,credBonus:result.credBonus,
    decision,badgeClass,isApplicant:true
  };
 
  // Inject into portfolio as slot 0
  portfolioData[0]={...activeApplicant,isApplicant:true};
 
  // Inject into queue as slot 0
  injectApplicantIntoQueue();
 
  // Sync Score tab inputs
  document.getElementById('income').value=income;
  document.getElementById('loanamt').value=loanamt;
  document.getElementById('rate').value=rate; document.getElementById('rate-out').textContent=rate+'%';
  document.getElementById('dti').value=dti; document.getElementById('dti-out').textContent=dti+'%';
  document.getElementById('delinq').value=delinq; document.getElementById('delinq-out').textContent=delinq;
  document.getElementById('credyrs').value=credyrs; document.getElementById('credyrs-out').textContent=credyrs;
  document.getElementById('grade').value=grade;
  document.getElementById('purpose').value=purpose;
 
  // Add to audit log
  addAuditEntry(`Application ${lid} (${name}) scored — ${decision} (${result.score})`);
 
  closeModal('new-app-modal');
 
  // Render badges on all panels
  renderApplicantBadges();
 
  // Update Models tab KV metrics
  updateModelsTab();
 
  // Update Compliance tab applicant summary
  updateComplianceApplicant();
 
  // Full recalc drives Score, Portfolio, SHAP charts
  recalc();
 
  // Navigate to Score tab so user sees the result
  switchTab('score');
}
 
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  MODELS TAB — update applicant section
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
function updateModelsTab(){
  const a=activeApplicant;
  document.getElementById('mdl-name').textContent    = a ? a.name  : '—';
  document.getElementById('mdl-id').textContent      = a ? a.lid   : '—';
  document.getElementById('mdl-score').textContent   = a ? a.score : document.getElementById('result-score').textContent;
  document.getElementById('mdl-pd').textContent      = a ? (a.pDefault*100).toFixed(1)+'%' : document.getElementById('result-prob').textContent.replace('P(Default): ','');
  document.getElementById('mdl-decision').textContent= a ? a.decision : document.getElementById('result-decision').textContent;
  document.getElementById('mdl-income').textContent  = a ? '$'+a.income.toLocaleString() : '$'+parseInt(document.getElementById('income').value).toLocaleString();
  document.getElementById('mdl-loanamt').textContent = a ? '$'+a.loanamt.toLocaleString() : '$'+parseInt(document.getElementById('loanamt').value).toLocaleString();
  document.getElementById('mdl-dti').textContent     = a ? a.dti+'%' : document.getElementById('dti').value+'%';
  document.getElementById('mdl-grade').textContent   = a ? GRADE_LABELS[a.grade] : GRADE_LABELS[parseInt(document.getElementById('grade').value)];
  document.getElementById('shap-applicant-note').textContent = a ? '— '+a.name : '';
}
 
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  COMPLIANCE TAB — applicant summary box
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
function updateComplianceApplicant(){
  const el=document.getElementById('compliance-applicant-summary');
  if(!activeApplicant){el.innerHTML='';return;}
  const a=activeApplicant;
  const{decision,bg,color}=decisionFromScore(a.score);
  const adverse = a.score < 650;
  el.innerHTML=`
    <div style="background:${bg};border-radius:var(--radius-sm);padding:10px 14px;font-size:12px;margin-bottom:8px">
      <div style="font-weight:600;color:${color};margin-bottom:4px">Current Decision: ${decision} — Score ${a.score}</div>
      <div style="color:${color}">Applicant: ${a.name} (${a.lid})</div>
      ${adverse ? `<div style="color:${color};margin-top:4px;font-size:11px">⚠ Adverse action notice required under ECOA Reg B</div>` : ''}
    </div>`;
}
 
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  AUDIT LOG
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
const auditLog=[
  {ts:'2025-06-14 09:12',msg:'Model v2.1.0 deployed to production'},
  {ts:'2025-06-01 14:30',msg:'Annual model validation completed — PASS'},
  {ts:'2025-05-15 10:00',msg:'Disparate impact analysis run — no violations'},
  {ts:'2025-03-01 08:45',msg:'HMDA annual report submitted'},
  {ts:'2025-01-20 11:00',msg:'CRA assessment area review — Satisfactory'},
];
function addAuditEntry(msg){
  const now=new Date();
  const ts=now.toISOString().replace('T',' ').slice(0,16);
  auditLog.unshift({ts,msg});
  renderAuditLog();
}
function renderAuditLog(){
  document.getElementById('audit-log-entries').innerHTML=auditLog.slice(0,8).map(e=>
    `<div class="kv-row"><span class="kv-key" style="font-family:monospace">${e.ts}</span><span class="kv-val" style="font-size:11px;text-align:right">${e.msg}</span></div>`
  ).join('');
}
 
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  QUEUE
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
const rng2=seededRandom(99);
let queueData=[];
for(let i=0;i<46;i++){
  const r2=5+rng2()*25,d2=rng2()*60,q2=rng2()>0.8?Math.floor(rng2()*3):0,
        g2=Math.floor(1+rng2()*5),inc2=30000+rng2()*120000,
        cy2=Math.floor(rng2()*20),la2=5000+rng2()*45000,pur2=Math.floor(1+rng2()*6);
  const res2=scoreApplicant(inc2,la2,r2,d2,q2,g2,cy2,pur2);
  const{decision:dec2,badgeClass:bc2}=decisionFromScore(res2.score);
  queueData.push({
    lid:`LN-2025-${String(1001+i).padStart(4,'0')}`,
    name:['Alex Johnson','Maria Garcia','Sam Lee','Pat Williams','Jordan Brown','Chris Davis','Taylor Wilson','Morgan Martinez','Casey Anderson','Riley Thomas','Jamie Jackson','Drew White','Avery Harris','Cameron Clark','Sydney Lewis'][i%15],
    score:res2.score,grade:GRADE_SHORT[g2],
    pDefault:(res2.pDefault*100).toFixed(1)+'%',
    decision:dec2,badgeClass:bc2,
    income:'$'+Math.round(inc2/1000)+'k',
    isApplicant:false
  });
}
 
function injectApplicantIntoQueue(){
  if(!activeApplicant) return;
  // Remove any previous applicant entry
  queueData=queueData.filter(r=>!r.isApplicant);
  // Add as first item
  queueData.unshift({
    lid:activeApplicant.lid,
    name:activeApplicant.name,
    score:activeApplicant.score,
    grade:GRADE_SHORT[activeApplicant.grade],
    pDefault:(activeApplicant.pDefault*100).toFixed(1)+'%',
    decision:activeApplicant.decision,
    badgeClass:activeApplicant.badgeClass,
    income:'$'+Math.round(activeApplicant.income/1000)+'k',
    isApplicant:true
  });
}
 
let queueFilter='';
function filterQueue(val){queueFilter=val;renderQueue();}
function renderQueue(){
  const filtered=queueFilter
    ? queueData.filter(r=>r.lid.toLowerCase().includes(queueFilter.toLowerCase())||r.name.toLowerCase().includes(queueFilter.toLowerCase())||r.decision.toLowerCase().includes(queueFilter.toLowerCase())||r.grade.toLowerCase().includes(queueFilter.toLowerCase()))
    : queueData;
  const shown=filtered.slice(0,15);
  let html='';
  shown.forEach(r=>{
    const rowCls=r.isApplicant?'highlight-row':'';
    const newTag=r.isApplicant?'<span style="font-size:9px;background:#dbeafe;color:#1d4ed8;padding:1px 5px;border-radius:10px;margin-left:4px;font-weight:600">NEW</span>':'';
    html+=`<tr class="${rowCls}">
      <td class="loan-id">${r.lid}${newTag}</td>
      <td>${r.name}</td>
      <td><b>${r.score}</b></td>
      <td class="hide-mobile">${r.grade}</td>
      <td class="hide-mobile">${r.pDefault}</td>
      <td><span class="badge ${r.badgeClass}">${r.decision}</span></td>
      <td class="hide-mobile">${r.income}</td>
      <td><button class="filter-btn" style="padding:4px 8px;font-size:11px" onclick="viewApp('${r.lid}','${r.name}')">View</button></td>
    </tr>`;
  });
  document.getElementById('queue-body').innerHTML=html;
  document.getElementById('queue-footer').textContent=`Showing ${shown.length} of ${filtered.length} applications`;
 
  // Processing summary counts
  const pending=queueData.filter(r=>r.decision==='MANUAL REVIEW').length;
  const approved=queueData.filter(r=>r.decision==='APPROVE').length;
  const declined=queueData.filter(r=>r.decision==='DECLINE').length;
  const review=queueData.filter(r=>r.decision==='MANUAL REVIEW').length;
  document.getElementById('q-pending').textContent=pending;
  document.getElementById('q-approved').textContent=approved;
  document.getElementById('q-declined').textContent=declined;
  document.getElementById('q-review').textContent=review;
 
  if(decisionChart){
    const approv=queueData.filter(r=>r.decision==='APPROVE').length;
    const cond=queueData.filter(r=>r.decision==='APPROVE WITH CONDITIONS').length;
    const rev=queueData.filter(r=>r.decision==='MANUAL REVIEW').length;
    const dec=queueData.filter(r=>r.decision==='DECLINE').length;
    decisionChart.data.datasets[0].data=[approv,cond,rev,dec];
    decisionChart.update('none');
  }
}
function viewApp(lid,name){
  // If it's the current applicant, navigate to score tab
  if(activeApplicant && activeApplicant.lid===lid){
    switchTab('score');
  } else {
    alert(`Opening application ${lid} for ${name}.\n\nIn production this would open the full application detail view.`);
  }
}
 
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  RISK MATRIX
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
function buildRiskMatrix(){
  const grades=['A','B','C','D','E'];
  const matrix=[[0,0,0,1],[0,0,1,1],[0,1,1,2],[1,1,2,2],[1,2,2,2]];
  const curDti=parseFloat(document.getElementById('dti').value);
  const curGrade=parseInt(document.getElementById('grade').value)-1;
  const dtiCol=curDti<15?0:curDti<30?1:curDti<45?2:3;
  let html='';
  for(let r=0;r<5;r++){
    html+=`<div style="display:flex;align-items:center;gap:3px;margin-bottom:3px"><span style="width:20px;font-size:9px;color:var(--muted);flex-shrink:0">${grades[r]}</span>`;
    for(let c=0;c<4;c++){
      const lvl=matrix[r][c];
      const cls=lvl===0?'rm-low':lvl===1?'rm-mod':'rm-high';
      const active=(r===curGrade&&c===dtiCol)?' rm-active':'';
      html+=`<div class="rm-cell ${cls}${active}" style="flex:1;min-height:22px">${lvl===0?'L':lvl===1?'M':'H'}</div>`;
    }
    html+='</div>';
  }
  document.getElementById('risk-matrix').innerHTML=html;
}
 
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  SHAP ROWS
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
function buildShapRows(rateRisk,dtiRisk,delinqRisk,gradeRisk,incomeBonus,credBonus){
  const features=[
    {name:'Delinquencies',neg:Math.round(delinqRisk),pos:0},
    {name:'Loan grade',   neg:Math.round(gradeRisk),pos:0},
    {name:'Interest rate',neg:Math.round(rateRisk),pos:0},
    {name:'DTI ratio',    neg:Math.round(dtiRisk),pos:0},
    {name:'Income',       neg:0,pos:Math.round(incomeBonus)},
    {name:'Credit history',neg:0,pos:Math.round(credBonus)},
  ].sort((a,b)=>(b.neg+b.pos)-(a.neg+a.pos));
  const maxVal=Math.max(...features.map(f=>f.neg+f.pos),1);
  document.getElementById('shap-rows').innerHTML=features.map(f=>{
    const negW=Math.round((f.neg/maxVal)*100);
    const posW=Math.round((f.pos/maxVal)*100);
    const val=f.neg>0?'+'+f.neg:'-'+f.pos;
    const valColor=f.neg>0?'#dc2626':'#2563eb';
    return `<div class="shap-row">
      <span class="shap-name">${f.name}</span>
      <div class="shap-bar-wrap">
        ${f.neg?`<div class="shap-neg" style="width:${negW}%"></div>`:''}
        <div class="shap-zero"></div>
        ${f.pos?`<div class="shap-pos" style="width:${posW}%"></div>`:''}
      </div>
      <span class="shap-val" style="color:${valColor}">${val}</span>
    </div>`;
  }).join('');
}
 
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  GOVERNANCE CHECKLIST
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
function buildGovernanceChecklist(){
  const items=[
    {label:'Model development documentation',done:true},
    {label:'Conceptual soundness review',done:true},
    {label:'Outcomes analysis (back-testing)',done:true},
    {label:'Independent validation completed',done:true},
    {label:'Disparate impact analysis',done:true},
    {label:'ECOA adverse action logic verified',done:true},
    {label:'FCRA permissible-purpose check',done:true},
    {label:'Annual model performance review',done:true},
    {label:'PSI monitoring active',done:true},
    {label:'Challenger model benchmarking',done:false},
    {label:'Stress test (recession scenario)',done:false},
    {label:'Basel III IRB full compliance',done:false},
  ];
  document.getElementById('governance-checklist').innerHTML=items.map(it=>{
    const icon=it.done?'ti-check':'ti-clock';
    const col=it.done?'#15803d':'#92400e';
    const bg=it.done?'#dcfce7':'#fef3c7';
    return `<div class="kv-row"><span class="kv-key">${it.label}</span>
      <span style="display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:50%;background:${bg};color:${col}">
        <i class="ti ${icon}" style="font-size:12px"></i>
      </span></div>`;
  }).join('');
}
 
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  CHARTS INIT
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
function initCharts(){
  barChart=new Chart(document.getElementById('barChart').getContext('2d'),{
    type:'bar',
    data:{labels:['Interest rate','DTI','Delinquencies','Loan grade','Income','Credit history'],
          datasets:[{data:[0,0,0,0,0,0],backgroundColor:['#dc2626','#f59e0b','#dc2626','#d97706','#16a34a','#16a34a'],borderRadius:4,label:'Risk contribution'}]},
    options:{responsive:true,maintainAspectRatio:false,indexAxis:'y',
      plugins:{legend:{display:false}},
      scales:{x:{beginAtZero:true,grid:{color:'#f1f5f9'},ticks:{font:{size:11}}},y:{ticks:{font:{size:11}},grid:{display:false}}}}
  });
 
  donutChart=new Chart(document.getElementById('donutChart').getContext('2d'),{
    type:'doughnut',
    data:{labels:['Low risk','Moderate risk','Elevated risk','High risk'],
          datasets:[{data:[0,0,0,0],backgroundColor:['#16a34a','#d97706','#ea580c','#dc2626'],borderWidth:3,borderColor:'#fff'}]},
    options:{responsive:true,maintainAspectRatio:false,cutout:'58%',
      plugins:{legend:{position:'bottom',labels:{font:{size:11},padding:12}}}}
  });
 
  const buckets=new Array(10).fill(0);
  portfolioData.forEach(l=>{const b=Math.min(9,Math.floor(l.score/100));buckets[b]++;});
  distChart=new Chart(document.getElementById('distChart').getContext('2d'),{
    type:'bar',
    data:{labels:['0–99','100–199','200–299','300–399','400–499','500–599','600–699','700–799','800–899','900–1000'],
          datasets:[{data:buckets,backgroundColor:buckets.map((_,i)=>i>=8?'#16a34a':i>=6?'#d97706':i>=5?'#ea580c':'#dc2626'),borderRadius:3}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},
      scales:{x:{ticks:{font:{size:9},maxRotation:45}},y:{grid:{color:'#f1f5f9'}}}}
  });
 
  const rocPts=[];
  for(let t=0;t<=1;t+=0.05){
    rocPts.push({x:t,y:Math.max(0,Math.min(1,t*1.64+Math.pow(t,2)*(-0.4)))});
  }
  rocChart=new Chart(document.getElementById('rocChart').getContext('2d'),{
    type:'scatter',
    data:{datasets:[
      {label:'Logistic Reg (AUC=0.640)',data:rocPts,showLine:true,fill:false,borderColor:'#1a56db',backgroundColor:'rgba(26,86,219,0.1)',pointRadius:0,borderWidth:2},
      {label:'Random (0.50)',data:[{x:0,y:0},{x:1,y:1}],showLine:true,fill:false,borderColor:'#9ca3af',borderDash:[5,5],pointRadius:0,borderWidth:1}
    ]},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{labels:{font:{size:10}}}},
      scales:{x:{min:0,max:1,title:{display:true,text:'FPR',font:{size:10}}},y:{min:0,max:1,title:{display:true,text:'TPR',font:{size:10}}}}}
  });
 
  decisionChart=new Chart(document.getElementById('decisionChart').getContext('2d'),{
    type:'bar',
    data:{labels:['Approved','Conditions','Review','Declined'],
          datasets:[{data:[0,0,0,0],backgroundColor:['#16a34a','#d97706','#ea580c','#dc2626'],borderRadius:4}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},
      scales:{x:{grid:{display:false}},y:{beginAtZero:true,grid:{color:'#f1f5f9'}}}}
  });
}
 
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  REPORT MODAL
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
function updateReport(){
  const a=activeApplicant;
  document.getElementById('rpt-name').textContent    = a?a.name:'—';
  document.getElementById('rpt-lid').textContent     = a?a.lid:'—';
  document.getElementById('rpt-score').textContent   = a?a.score:document.getElementById('result-score').textContent;
  document.getElementById('rpt-pd').textContent      = a?(a.pDefault*100).toFixed(1)+'%':document.getElementById('result-prob').textContent.replace('P(Default): ','');
  document.getElementById('rpt-decision').textContent= a?a.decision:document.getElementById('result-decision').textContent;
  document.getElementById('rpt-income').textContent  = '$'+(a?a.income:parseInt(document.getElementById('income').value)).toLocaleString();
  document.getElementById('rpt-loanamt').textContent = '$'+(a?a.loanamt:parseInt(document.getElementById('loanamt').value)).toLocaleString();
  document.getElementById('rpt-rate').textContent    = (a?a.rate:document.getElementById('rate').value)+'%';
  document.getElementById('rpt-dti').textContent     = (a?a.dti:document.getElementById('dti').value)+'%';
  document.getElementById('rpt-delinq').textContent  = a?a.delinq:document.getElementById('delinq').value;
  document.getElementById('rpt-credyrs').textContent = (a?a.credyrs:document.getElementById('credyrs').value)+' yrs';
  document.getElementById('rpt-grade').textContent   = GRADE_LABELS[a?a.grade:parseInt(document.getElementById('grade').value)];
  document.getElementById('rpt-purpose').textContent = PURPOSE_LABELS[a?a.purpose:parseInt(document.getElementById('purpose').value)];
  document.getElementById('report-date').textContent = new Date().toLocaleString();
}
 
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  MAIN RECALC — fires on every input change
//  and after new application is submitted
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
function recalc(){
  const income  =parseFloat(document.getElementById('income').value)||60000;
  const loanamt =parseFloat(document.getElementById('loanamt').value)||15000;
  const rate    =parseFloat(document.getElementById('rate').value);
  const dti     =parseFloat(document.getElementById('dti').value);
  const delinq  =parseFloat(document.getElementById('delinq').value);
  const grade   =parseFloat(document.getElementById('grade').value);
  const credyrs =parseFloat(document.getElementById('credyrs').value);
  const purpose =parseInt(document.getElementById('purpose').value);
 
  document.getElementById('rate-out').textContent   =rate+'%';
  document.getElementById('dti-out').textContent    =dti+'%';
  document.getElementById('delinq-out').textContent =delinq;
  document.getElementById('credyrs-out').textContent=credyrs;
 
  const res=scoreApplicant(income,loanamt,rate,dti,delinq,grade,credyrs,purpose);
  const{rateRisk,dtiRisk,delinqRisk,gradeRisk,incomeBonus,credBonus,pDefault,score}=res;
  const{decision,bg,color,badgeClass}=decisionFromScore(score);
 
  // Keep portfolio slot 0 in sync with Score tab inputs
  portfolioData[0]={rate,dti,delinq,grade,income,credyrs,loanamt,purpose,score,pDefault,
    name:activeApplicant?activeApplicant.name:'',
    lid:activeApplicant?activeApplicant.lid:'',
    isApplicant:!!activeApplicant};
 
  // If we have an active applicant, also sync their score with the slider
  if(activeApplicant){
    activeApplicant.score=score;
    activeApplicant.pDefault=pDefault;
    activeApplicant.decision=decision;
    activeApplicant.badgeClass=badgeClass;
    renderApplicantBadges();
    injectApplicantIntoQueue();
  }
 
  // Gauge
  document.getElementById('gauge-marker').style.left=Math.min(97,Math.max(1,score/10))+'%';
 
  // Score result box
  const ltv=((loanamt/Math.max(1,income))*100).toFixed(0);
  document.getElementById('result-box').style.background     =bg;
  document.getElementById('result-score').style.color        =color;
  document.getElementById('result-score').textContent        =score;
  document.getElementById('result-decision').style.color     =color;
  document.getElementById('result-decision').textContent     =decision;
  document.getElementById('result-prob').style.color         =color;
  document.getElementById('result-prob').textContent         ='P(Default): '+(pDefault*100).toFixed(1)+'%';
  document.getElementById('result-meta').textContent         =`LTV: ${ltv}% · Grade: ${GRADE_SHORT[grade]} · Purpose: ${PURPOSE_LABELS[purpose]}`;
 
  // Adverse action
  const advBox=document.getElementById('adverse-box');
  if(score<650){
    advBox.style.display='block';
    const reasons=[];
    if(delinq>0) reasons.push(`Delinquent accounts on record (${delinq} in past 2 years)`);
    if(grade>=4) reasons.push(`Loan grade classification (${GRADE_SHORT[grade]})`);
    if(dti>35)   reasons.push(`Debt-to-income ratio too high (${dti}%)`);
    if(rate>18)  reasons.push(`High interest rate indicative of credit risk (${rate}%)`);
    if(income<40000) reasons.push('Insufficient income to support requested loan amount');
    if(!reasons.length) reasons.push('Overall credit profile does not meet current lending criteria');
    document.getElementById('adverse-list').innerHTML=reasons.slice(0,4).map(r=>`<li>${r}</li>`).join('');
  } else { advBox.style.display='none'; }
 
  // Risk flags
  const items=[];
  if(rate>18)      items.push({text:`High interest rate (${rate}%)`,color:'#b91c1c',dot:'#dc2626'});
  if(dti>35)       items.push({text:`High debt-to-income (${dti}%)`,color:'#b91c1c',dot:'#dc2626'});
  if(delinq>0)     items.push({text:`${delinq} delinquenc${delinq>1?'ies':'y'} in last 2 years`,color:'#b91c1c',dot:'#dc2626'});
  if(grade>=4)     items.push({text:`Elevated loan grade (${GRADE_SHORT[grade]})`,color:'#92400e',dot:'#d97706'});
  if(loanamt>income*0.5) items.push({text:`Loan-to-income ratio elevated (${ltv}%)`,color:'#92400e',dot:'#d97706'});
  if(credyrs<3)    items.push({text:`Short credit history (${credyrs} yrs)`,color:'#92400e',dot:'#d97706'});
  if(delinq===0)   items.push({text:'No recent delinquencies ✓',color:'#15803d',dot:'#16a34a'});
  if(dti<20)       items.push({text:'Low debt-to-income ratio ✓',color:'#15803d',dot:'#16a34a'});
  if(income>80000) items.push({text:'Strong income profile ✓',color:'#15803d',dot:'#16a34a'});
  if(credyrs>=10)  items.push({text:`Long credit history (${credyrs} yrs) ✓`,color:'#15803d',dot:'#16a34a'});
  if(!items.length)items.push({text:'No significant risk flags',color:'#15803d',dot:'#16a34a'});
  document.getElementById('risk-flags').innerHTML=items.map(f=>
    `<div class="flag-item"><div class="flag-dot" style="background:${f.dot}"></div><span style="color:${f.color}">${f.text}</span></div>`
  ).join('');
 
  // Scorecard
  const factorDefs=[
    {name:'Interest Rate',pts:-Math.round(rateRisk),maxAbs:40},
    {name:'DTI Ratio',    pts:-Math.round(dtiRisk),maxAbs:30},
    {name:'Delinquencies',pts:-Math.round(delinqRisk),maxAbs:30},
    {name:'Loan Grade',   pts:-Math.round(gradeRisk),maxAbs:32},
    {name:'Income',       pts: Math.round(incomeBonus),maxAbs:15},
    {name:'Credit History',pts: Math.round(credBonus),maxAbs:5},
  ];
  document.getElementById('scorecard-total').textContent=score;
  document.getElementById('scorecard-rows').innerHTML=factorDefs.map(f=>{
    const pct=Math.min(100,Math.abs(f.pts)/f.maxAbs*100);
    const fillColor=f.pts<0?(Math.abs(f.pts)>f.maxAbs*0.5?'#dc2626':'#f59e0b'):'#16a34a';
    const sign=f.pts>=0?'+':'';
    return `<div class="factor-row">
      <span class="factor-name">${f.name}</span>
      <div class="factor-bar"><div class="factor-fill" style="width:${pct}%;background:${fillColor}"></div></div>
      <span class="factor-pts" style="color:${f.pts<0?'#dc2626':'#15803d'}">${sign}${f.pts}</span>
    </div>`;
  }).join('');
 
  // Workflow timeline
  let steps;
  if(score>=800){steps=[
    {label:'Application received',meta:'Completed',state:'done'},
    {label:'Automated credit scoring',meta:'Score: '+score,state:'done'},
    {label:'Auto-approval decision',meta:'APPROVED',state:'done'},
    {label:'Offer letter generation',meta:'Next step',state:'active'},
    {label:'Loan disbursement',meta:'Pending',state:'pending'},
  ];}else if(score>=650){steps=[
    {label:'Application received',meta:'Completed',state:'done'},
    {label:'Automated credit scoring',meta:'Score: '+score,state:'done'},
    {label:'Conditional approval',meta:'Awaiting docs',state:'active'},
    {label:'Document verification',meta:'Pending',state:'pending'},
    {label:'Final decision',meta:'Pending',state:'pending'},
  ];}else if(score>=500){steps=[
    {label:'Application received',meta:'Completed',state:'done'},
    {label:'Automated credit scoring',meta:'Score: '+score,state:'done'},
    {label:'Referred to underwriter',meta:'In queue',state:'active'},
    {label:'Manual review',meta:'Pending',state:'pending'},
    {label:'Final decision',meta:'Pending',state:'pending'},
  ];}else{steps=[
    {label:'Application received',meta:'Completed',state:'done'},
    {label:'Automated credit scoring',meta:'Score: '+score,state:'done'},
    {label:'Adverse action triggered',meta:'DECLINED',state:'done'},
    {label:'Adverse action notice',meta:'Generating…',state:'active'},
    {label:'Applicant notification',meta:'Pending',state:'pending'},
  ];}
  document.getElementById('workflow-timeline').innerHTML=steps.map(s=>
    `<div class="tl-item ${s.state}"><div class="tl-dot"></div><div class="tl-label">${s.label}</div><div class="tl-meta">${s.meta}</div></div>`
  ).join('');
 
  // Portfolio counts
  let low=0,mod=0,elev=0,high=0;
  portfolioData.forEach(l=>{
    if(l.score>=800)low++;
    else if(l.score>=650)mod++;
    else if(l.score>=500)elev++;
    else high++;
  });
  const total=portfolioData.length;
  document.getElementById('low-count-val').textContent =low;
  document.getElementById('mod-count-val').textContent =mod;
  document.getElementById('elev-count-val').textContent=elev;
  document.getElementById('high-count-val').textContent=high;
  document.getElementById('low-count-lbl').textContent =low+' loans';
  document.getElementById('mod-count-lbl').textContent =mod+' loans';
  document.getElementById('elev-count-lbl').textContent=elev+' loans';
  document.getElementById('high-count-lbl').textContent=high+' loans';
  document.getElementById('port-total-scored').textContent=total.toLocaleString();
 
  // Portfolio KPIs
  const defCount=Math.round(total*0.0178);
  const totalLoanVal=portfolioData.reduce((s,l)=>s+(l.loanamt||15000),0);
  const el=totalLoanVal*0.0178*0.45;
  document.getElementById('port-default-rate').textContent=((defCount/total)*100).toFixed(2)+'%';
  document.getElementById('port-defaults-abs').textContent=defCount+' expected defaults';
  document.getElementById('port-el').textContent='$'+(el/1000).toFixed(0)+'K';
  const approved2=low+mod;
  document.getElementById('port-approval-rate').textContent=((approved2/total)*100).toFixed(1)+'%';
  document.getElementById('port-approved-abs').textContent=approved2+' approved';
 
  // Concentration flags
  const flags=[];
  if(high/total>0.45) flags.push({text:`High-risk loans ${(high/total*100).toFixed(0)}% of portfolio — above 40% threshold`,color:'#b91c1c',dot:'#dc2626'});
  if((elev+high)/total>0.65) flags.push({text:`Elevated+High combined at ${((elev+high)/total*100).toFixed(0)}% — concentration risk`,color:'#c2410c',dot:'#ea580c'});
  if(low/total<0.15) flags.push({text:'Low-risk share below 15% — portfolio quality concern',color:'#92400e',dot:'#d97706'});
  if(!flags.length) flags.push({text:'No concentration risk flags at current levels',color:'#15803d',dot:'#16a34a'});
  document.getElementById('concentration-flags').innerHTML=flags.map(f=>
    `<div class="flag-item"><div class="flag-dot" style="background:${f.dot}"></div><span style="color:${f.color};font-size:12px">${f.text}</span></div>`
  ).join('');
 
  // Alert
  if((elev+high)/total>0.6){
    document.getElementById('alert-banner').classList.add('show');
    document.getElementById('alert-text').textContent=`Portfolio concentration alert: ${((high/total)*100).toFixed(0)}% high-risk loans detected. Consider tightening credit policy.`;
  }
 
  // Bar chart update
  if(barChart){
    barChart.data.datasets[0].data=[Math.round(rateRisk),Math.round(dtiRisk),Math.round(delinqRisk),Math.round(gradeRisk),Math.round(incomeBonus),Math.round(credBonus)];
    barChart.data.datasets[0].backgroundColor=[
      rateRisk>15?'#dc2626':'#16a34a',
      dtiRisk>15?'#dc2626':'#16a34a',
      delinqRisk>0?'#dc2626':'#16a34a',
      gradeRisk>20?'#dc2626':'#16a34a',
      '#16a34a','#16a34a'
    ];
    barChart.update('none');
  }
 
  // Donut update
  if(donutChart){donutChart.data.datasets[0].data=[low,mod,elev,high];donutChart.update('none');}
 
  // SHAP
  buildShapRows(rateRisk,dtiRisk,delinqRisk,gradeRisk,incomeBonus,credBonus);
 
  // Risk matrix
  buildRiskMatrix();
 
  // Models tab live sync
  updateModelsTab();
 
  // Compliance applicant summary
  updateComplianceApplicant();
}
 
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  BOOT
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
buildGovernanceChecklist();
renderAuditLog();
initCharts();
recalc();
renderQueue();
</script>
</body>
</html>
"""
 
components.html(html_code, height=1000, scrolling=True)
