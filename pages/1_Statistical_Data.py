import streamlit as st
import pandas as pd
from config import DATA_FILE   # ← single source of truth

st.set_page_config(
    page_title="Statistical Data | Mess Feedback",
    page_icon="📊",
    layout="wide"
)

# ── Load Data ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)
    df.rename(columns={
        "MEAL TYPE(Choose the meal you just had)": "Meal",
        "Food Temperature": "Temperature",
        "Your Experience": "Experience",
        "Taste  ": "Taste"
    }, inplace=True)
    if 'Timestamp' in df.columns:
        df.drop(columns=['Timestamp'], inplace=True)
    return df

df           = load_data()
numeric_cols = df.select_dtypes(include='number').columns.tolist()
col_avgs     = df[numeric_cols].mean()
overall_avg  = col_avgs.mean()
total_resp   = len(df)
best_param   = col_avgs.idxmax()
worst_param  = col_avgs.idxmin()

meal_scores  = df.groupby("Meal")[numeric_cols].mean().mean(axis=1).sort_values(ascending=False) \
               if "Meal" in df.columns else pd.Series()
best_meal    = meal_scores.idxmax() if len(meal_scores) else "N/A"
worst_meal   = meal_scores.idxmin() if len(meal_scores) else "N/A"

# Satisfaction label
def satisfaction_label(score):
    if score >= 4.0: return ("Excellent", "#22c55e")
    if score >= 3.5: return ("Good",      "#3b82f6")
    if score >= 3.0: return ("Average",   "#f59e0b")
    if score >= 2.0: return ("Poor",      "#f97316")
    return ("Critical", "#ef4444")

sat_label, sat_color = satisfaction_label(overall_avg)

# Parameter config
PARAM_META = {
    "Taste":       ("😋", "#f59e0b", "amber"),
    "Temperature": ("🌡️", "#ef4444", "red"),
    "Quantity":    ("🍽️", "#22c55e", "green"),
    "Hygiene":     ("🧹", "#3b82f6", "blue"),
    "Experience":  ("⭐", "#a855f7", "purple"),
}

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.block-container { padding-top: 1rem !important; padding-bottom: 2rem !important; }

/* ── Page Header ───────────────────────── */
.page-header {
    background: linear-gradient(135deg, #0f172a 0%, #1a2744 45%, #0f4c81 100%);
    border-radius: 20px;
    padding: 48px 48px 42px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(0,0,0,0.45);
}
.page-header::before {
    content: '';
    position: absolute; inset: 0;
    background:
        radial-gradient(circle at 10% 50%, rgba(59,130,246,0.15) 0%, transparent 55%),
        radial-gradient(circle at 90% 20%, rgba(99,102,241,0.10) 0%, transparent 50%);
    pointer-events: none;
}
.page-header-inner { position: relative; max-width: 720px; }
.page-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(59,130,246,0.15);
    border: 1px solid rgba(59,130,246,0.4);
    color: #93c5fd; font-size: 11px; font-weight: 600;
    letter-spacing: 1.8px; text-transform: uppercase;
    padding: 6px 16px; border-radius: 50px; margin-bottom: 20px;
}
.page-title {
    font-size: clamp(1.8rem, 4vw, 2.8rem); font-weight: 800;
    color: #fff; line-height: 1.15; margin: 0 0 12px; letter-spacing: -0.4px;
}
.page-title span {
    background: linear-gradient(90deg, #60a5fa, #818cf8);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.page-subtitle { font-size: 0.97rem; color: #94a3b8; line-height: 1.65; margin: 0; max-width: 540px; }

/* ── Summary Metric Row ────────────────── */
.metric-row {
    display: grid; grid-template-columns: repeat(4,1fr);
    gap: 14px; margin-bottom: 28px;
}
.metric-card {
    background: #1e293b; border: 1px solid #334155;
    border-radius: 14px; padding: 20px 16px;
    text-align: center; position: relative; overflow: hidden;
    transition: transform .2s, box-shadow .2s, border-color .2s;
}
.metric-card::after {
    content:''; position:absolute; bottom:0; left:0; right:0;
    height:2px; background: linear-gradient(90deg,#3b82f6,#6366f1);
    transform: scaleX(0); transition: transform .3s ease;
}
.metric-card:hover { transform: translateY(-4px); box-shadow: 0 12px 32px rgba(0,0,0,.3); border-color:#3b82f6; }
.metric-card:hover::after { transform: scaleX(1); }
.metric-icon  { font-size: 1.6rem; margin-bottom: 6px; }
.metric-value { font-size: 1.8rem; font-weight: 800; color: #60a5fa; line-height: 1; margin-bottom: 4px; }
.metric-label { font-size: 11px; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: .8px; }

/* ── Section Header ────────────────────── */
.sec-head { display:flex; align-items:center; gap:12px; margin: 32px 0 6px; }
.sec-icon {
    width:38px; height:38px; border-radius:10px;
    display:flex; align-items:center; justify-content:center;
    font-size:1.1rem; flex-shrink:0;
}
.sec-icon.blue   { background: rgba(59,130,246,.15); }
.sec-icon.indigo { background: rgba(99,102,241,.15); }
.sec-icon.amber  { background: rgba(245,158,11,.15); }
.sec-icon.green  { background: rgba(34,197,94,.15); }
.sec-text h3 { font-size:1.1rem; font-weight:700; color:#f1f5f9; margin:0 0 2px; }
.sec-text p  { font-size:.82rem; color:#64748b; margin:0; }
.sec-rule {
    height:1px; background: linear-gradient(90deg,#334155 0%,transparent 100%);
    margin:10px 0 18px; border:none;
}

/* ── Parameter Cards ───────────────────── */
.param-grid {
    display: grid; grid-template-columns: repeat(5,1fr);
    gap: 14px; margin-bottom: 28px;
}
.param-card {
    background: #1e293b; border: 1px solid #334155;
    border-radius: 14px; padding: 22px 14px 18px;
    text-align: center; position: relative; overflow: hidden;
    transition: transform .22s, box-shadow .22s, border-color .22s;
}
.param-card:hover { transform: translateY(-5px); box-shadow: 0 14px 36px rgba(0,0,0,.3); }
.param-top-bar {
    position: absolute; top:0; left:0; right:0; height:3px; border-radius:14px 14px 0 0;
}
.param-emoji { font-size:1.8rem; margin-bottom:8px; }
.param-name  { font-size:.75rem; font-weight:700; color:#94a3b8; text-transform:uppercase; letter-spacing:1px; margin-bottom:10px; }
.param-score { font-size:2.1rem; font-weight:800; line-height:1; margin-bottom:4px; }
.param-out   { font-size:.72rem; color:#475569; margin-bottom:12px; }
.param-bar-wrap { background:#0f172a; border-radius:50px; height:6px; overflow:hidden; }
.param-bar-fill { height:6px; border-radius:50px; transition: width .6s ease; }
.param-tag {
    display:inline-block; margin-top:10px;
    font-size:.68rem; font-weight:700; letter-spacing:.6px;
    padding:3px 10px; border-radius:50px;
}

/* ── Meal comparison ────────────────────── */
.meal-card {
    background: #1e293b; border: 1px solid #334155;
    border-radius: 14px; padding: 20px 18px;
    margin-bottom: 12px;
    transition: border-color .2s;
}
.meal-card:hover { border-color: #3b82f6; }
.meal-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; }
.meal-name { font-size:.95rem; font-weight:700; color:#f1f5f9; }
.meal-score-badge {
    font-size:.85rem; font-weight:800;
    padding:4px 14px; border-radius:50px;
    background: rgba(59,130,246,.12); border:1px solid rgba(59,130,246,.25); color:#60a5fa;
}
.meal-bar-wrap { background:#0f172a; border-radius:50px; height:8px; overflow:hidden; }
.meal-bar-fill { height:8px; border-radius:50px; }
.meal-sub-grid { display:grid; grid-template-columns:repeat(5,1fr); gap:8px; margin-top:12px; }
.meal-sub-item { text-align:center; }
.meal-sub-val  { font-size:.85rem; font-weight:700; color:#e2e8f0; }
.meal-sub-lbl  { font-size:.65rem; color:#475569; font-weight:600; text-transform:uppercase; letter-spacing:.6px; }

/* ── Quick Insights ─────────────────────── */
.insights-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:14px; margin-bottom:28px; }
.insight-card {
    background: #1e293b; border: 1px solid #334155;
    border-radius:14px; padding:22px 20px;
    display:flex; align-items:flex-start; gap:16px;
    transition: transform .2s, border-color .2s;
}
.insight-card:hover { transform:translateY(-3px); border-color:#3b82f6; }
.insight-icon-box {
    width:46px; height:46px; border-radius:12px;
    display:flex; align-items:center; justify-content:center;
    font-size:1.4rem; flex-shrink:0;
}
.insight-body h4 { font-size:.85rem; font-weight:600; color:#64748b; margin:0 0 4px; text-transform:uppercase; letter-spacing:.8px; }
.insight-body .val { font-size:1.2rem; font-weight:800; color:#f1f5f9; margin:0 0 3px; }
.insight-body .sub { font-size:.78rem; color:#475569; margin:0; }

@media(max-width:768px) {
    .metric-row, .param-grid { grid-template-columns:repeat(2,1fr); }
    .insights-grid { grid-template-columns:1fr; }
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="page-header">
  <div class="page-header-inner">
    <div class="page-badge">📊 Mess Feedback Dashboard</div>
    <h1 class="page-title">Statistical <span>Analytics</span></h1>
    <p class="page-subtitle">
      Live metrics, parameter ratings, and meal-wise performance breakdown
      from all collected student feedback responses.
    </p>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TOP SUMMARY CARDS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="metric-row">
  <div class="metric-card">
    <div class="metric-icon">📋</div>
    <div class="metric-value">{total_resp}</div>
    <div class="metric-label">Total Responses</div>
  </div>
  <div class="metric-card">
    <div class="metric-icon">⭐</div>
    <div class="metric-value">{overall_avg:.2f}</div>
    <div class="metric-label">Overall Avg / 5.0</div>
  </div>
  <div class="metric-card">
    <div class="metric-icon">🏆</div>
    <div class="metric-value">{best_param}</div>
    <div class="metric-label">Best Parameter</div>
  </div>
  <div class="metric-card">
    <div class="metric-icon" style="color:{sat_color};">●</div>
    <div class="metric-value" style="color:{sat_color};">{sat_label}</div>
    <div class="metric-label">Satisfaction Level</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — PARAMETER RATING CARDS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec-head">
  <div class="sec-icon indigo">📐</div>
  <div class="sec-text">
    <h3>Parameter Ratings</h3>
    <p>Average student rating for each mess quality parameter (out of 5)</p>
  </div>
</div>
<hr class="sec-rule">
""", unsafe_allow_html=True)

cards_html = '<div class="param-grid">'
for param in numeric_cols:
    score = col_avgs.get(param, 0)
    pct   = (score / 5) * 100
    meta  = PARAM_META.get(param, ("📊", "#3b82f6", "blue"))
    emoji, color, _ = meta
    lbl, _ = satisfaction_label(score)
    cards_html += f"""
    <div class="param-card" style="border-top-color:{color}">
      <div class="param-top-bar" style="background:{color};"></div>
      <div class="param-emoji">{emoji}</div>
      <div class="param-name">{param}</div>
      <div class="param-score" style="color:{color};">{score:.2f}</div>
      <div class="param-out">out of 5.0</div>
      <div class="param-bar-wrap">
        <div class="param-bar-fill" style="width:{pct:.1f}%; background:{color};"></div>
      </div>
      <div class="param-tag" style="background:{color}22; color:{color}; border:1px solid {color}55;">{lbl}</div>
    </div>"""
cards_html += '</div>'
st.markdown(cards_html, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — QUICK INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec-head">
  <div class="sec-icon green">💡</div>
  <div class="sec-text">
    <h3>Quick Insights</h3>
    <p>Automatically derived highlights from the feedback data</p>
  </div>
</div>
<hr class="sec-rule">
""", unsafe_allow_html=True)

best_meal_score  = f"{meal_scores[best_meal]:.2f}/5.0"  if len(meal_scores) else "N/A"
worst_meal_score = f"{meal_scores[worst_meal]:.2f}/5.0" if len(meal_scores) else "N/A"
best_val  = f"{col_avgs[best_param]:.2f}/5.0"
worst_val = f"{col_avgs[worst_param]:.2f}/5.0"

st.markdown(f"""
<div class="insights-grid">
  <div class="insight-card">
    <div class="insight-icon-box" style="background:rgba(34,197,94,.12);">🏆</div>
    <div class="insight-body">
      <h4>Highest Rated Meal</h4>
      <div class="val">{best_meal}</div>
      <div class="sub">Avg score: {best_meal_score} — best overall experience reported</div>
    </div>
  </div>
  <div class="insight-card">
    <div class="insight-icon-box" style="background:rgba(239,68,68,.12);">⚠️</div>
    <div class="insight-body">
      <h4>Lowest Rated Meal</h4>
      <div class="val">{worst_meal}</div>
      <div class="sub">Avg score: {worst_meal_score} — needs improvement in quality</div>
    </div>
  </div>
  <div class="insight-card">
    <div class="insight-icon-box" style="background:rgba(59,130,246,.12);">⭐</div>
    <div class="insight-body">
      <h4>Best Performing Parameter</h4>
      <div class="val">{best_param}</div>
      <div class="sub">Rated {best_val} — strongest area of the mess</div>
    </div>
  </div>
  <div class="insight-card">
    <div class="insight-icon-box" style="background:rgba(245,158,11,.12);">🔻</div>
    <div class="insight-body">
      <h4>Lowest Rated Parameter</h4>
      <div class="val">{worst_param}</div>
      <div class="sub">Rated {worst_val} — priority area for management attention</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — MEAL-WISE BREAKDOWN
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec-head">
  <div class="sec-icon amber">🍽️</div>
  <div class="sec-text">
    <h3>Meal-wise Breakdown</h3>
    <p>Per-meal rating comparison with individual parameter scores</p>
  </div>
</div>
<hr class="sec-rule">
""", unsafe_allow_html=True)

if "Meal" in df.columns:
    meal_avg_df = df.groupby("Meal")[numeric_cols].mean()
    meal_colors = ["#22c55e", "#3b82f6", "#f59e0b", "#a855f7", "#ef4444"]

    for i, (meal_name, row) in enumerate(meal_avg_df.iterrows()):
        score   = row.mean()
        pct     = (score / 5) * 100
        mcolor  = meal_colors[i % len(meal_colors)]
        sub_items = "".join([
            f'<div class="meal-sub-item"><div class="meal-sub-val">{row[p]:.1f}</div>'
            f'<div class="meal-sub-lbl">{p}</div></div>'
            for p in numeric_cols if p in row
        ])
        st.markdown(f"""
        <div class="meal-card">
          <div class="meal-header">
            <span class="meal-name">🍛 {meal_name}</span>
            <span class="meal-score-badge" style="color:{mcolor}; border-color:{mcolor}44;">{score:.2f} / 5.0</span>
          </div>
          <div class="meal-bar-wrap">
            <div class="meal-bar-fill" style="width:{pct:.1f}%; background:linear-gradient(90deg,{mcolor},{mcolor}99);"></div>
          </div>
          <div class="meal-sub-grid">{sub_items}</div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — RAW DATASET (Collapsible)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec-head">
  <div class="sec-icon blue">🗂️</div>
  <div class="sec-text">
    <h3>Raw Dataset</h3>
    <p>Preview the collected feedback records — expand to browse the full dataset</p>
  </div>
</div>
<hr class="sec-rule">
""", unsafe_allow_html=True)

# Compact preview: first 5 rows
styled_preview = (
    df.head(5).style
    .format("{:.2f}", subset=numeric_cols)
    .background_gradient(cmap="Blues", subset=numeric_cols, axis=0)
    .set_properties(**{"font-size": "13px", "border": "1px solid #334155"})
)
st.dataframe(styled_preview, use_container_width=True)

# Full dataset in expander
with st.expander(f"📂 View Full Dataset ({total_resp} rows)", expanded=False):
    styled_full = (
        df.style
        .format("{:.2f}", subset=numeric_cols)
        .background_gradient(cmap="Blues", subset=numeric_cols, axis=0)
        .highlight_max(subset=numeric_cols, color="#1a3a2a", axis=0)
        .set_properties(**{"font-size": "13px", "border": "1px solid #334155"})
    )
    st.dataframe(styled_full, use_container_width=True, height=350)
