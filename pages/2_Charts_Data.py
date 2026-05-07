import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Charts & Visualizations | Mess Feedback",
    page_icon="📈",
    layout="wide"
)

# ── Load Data ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("Updated PVGCOET Mess Feedback.csv")
    df.rename(columns={
        "MEAL TYPE(Choose the meal you just had)": "Meal",
        "Food Temperature": "Temperature",
        "Your Experience": "Experience",
        "Taste  ": "Taste"
    }, inplace=True)
    if 'Timestamp' in df.columns:
        df.drop(columns=['Timestamp'], inplace=True)
    return df

df          = load_data()
ALL_PARAMS  = ["Taste", "Temperature", "Quantity", "Hygiene", "Experience"]
PARAMS      = [c for c in ALL_PARAMS if c in df.columns]
MEALS       = sorted(df["Meal"].unique().tolist()) if "Meal" in df.columns else []

# ── Chart helpers ──────────────────────────────────────────────────────────────
DARK_BASE = dict(
    paper_bgcolor="#0f172a",
    plot_bgcolor="#1e293b",
    font=dict(family="Inter, sans-serif", color="#94a3b8", size=12),
    title_font=dict(family="Inter, sans-serif", color="#f1f5f9", size=15),
)
GRID = dict(gridcolor="#334155", linecolor="#334155", zerolinecolor="#334155")

def layout(**kw):
    base = dict(DARK_BASE)
    base["xaxis"] = dict(GRID)
    base["yaxis"] = dict(GRID)
    base["legend"] = dict(bgcolor="#1e293b", bordercolor="#334155", borderwidth=1)
    base["margin"] = dict(l=0, r=0, t=44, b=0)
    base.update(kw)
    return base

PARAM_COLORS = {
    "Taste":       "#f59e0b",
    "Temperature": "#ef4444",
    "Quantity":    "#22c55e",
    "Hygiene":     "#3b82f6",
    "Experience":  "#a855f7",
}
MEAL_COLORS = ["#3b82f6", "#22c55e", "#f59e0b", "#a855f7", "#ef4444"]

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.block-container { padding-top: 1rem !important; padding-bottom: 2rem !important; }

.page-header {
    background: linear-gradient(135deg, #0f172a 0%, #1a2744 45%, #0f4c81 100%);
    border-radius: 20px; padding: 48px 48px 42px;
    margin-bottom: 28px; position: relative; overflow: hidden;
    box-shadow: 0 20px 60px rgba(0,0,0,.45);
}
.page-header::before {
    content:''; position:absolute; inset:0;
    background:
        radial-gradient(circle at 10% 50%, rgba(59,130,246,.15) 0%, transparent 55%),
        radial-gradient(circle at 90% 20%, rgba(99,102,241,.10) 0%, transparent 50%);
    pointer-events:none;
}
.page-header-inner { position:relative; max-width:720px; }
.page-badge {
    display:inline-flex; align-items:center; gap:6px;
    background:rgba(59,130,246,.15); border:1px solid rgba(59,130,246,.4);
    color:#93c5fd; font-size:11px; font-weight:600;
    letter-spacing:1.8px; text-transform:uppercase;
    padding:6px 16px; border-radius:50px; margin-bottom:20px;
}
.page-title {
    font-size:clamp(1.8rem,4vw,2.8rem); font-weight:800;
    color:#fff; line-height:1.15; margin:0 0 12px; letter-spacing:-.4px;
}
.page-title span {
    background:linear-gradient(90deg,#60a5fa,#818cf8);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
}
.page-subtitle { font-size:.97rem; color:#94a3b8; line-height:1.65; margin:0; max-width:560px; }

.sec-head { display:flex; align-items:center; gap:12px; margin:36px 0 8px; }
.sec-icon {
    width:38px; height:38px; border-radius:10px;
    display:flex; align-items:center; justify-content:center;
    font-size:1.1rem; flex-shrink:0;
}
.sec-icon.blue   { background:rgba(59,130,246,.15); }
.sec-icon.amber  { background:rgba(245,158,11,.15); }
.sec-icon.green  { background:rgba(34,197,94,.15); }
.sec-icon.purple { background:rgba(168,85,247,.15); }
.sec-text h3 { font-size:1.05rem; font-weight:700; color:#f1f5f9; margin:0 0 2px; }
.sec-text p  { font-size:.82rem; color:#64748b; margin:0; }
.sec-rule { height:1px; background:linear-gradient(90deg,#334155 0%,transparent 100%); margin:8px 0 16px; border:none; }

.chart-card {
    background:#1e293b; border:1px solid #334155;
    border-radius:16px; padding:20px 20px 14px; margin-bottom:0;
}
.insight-strip {
    background:rgba(59,130,246,.06); border:1px solid rgba(59,130,246,.18);
    border-left:3px solid #3b82f6; border-radius:0 8px 8px 0;
    padding:10px 16px; margin-top:10px;
    font-size:.82rem; color:#94a3b8; line-height:1.55;
}
.insight-strip strong { color:#60a5fa; }

.insights-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:14px; margin-bottom:4px; }
.insight-card {
    background:#1e293b; border:1px solid #334155; border-radius:14px;
    padding:20px 18px; display:flex; align-items:flex-start; gap:14px;
    transition:transform .2s, border-color .2s;
}
.insight-card:hover { transform:translateY(-3px); border-color:#3b82f6; }
.insight-icon-box {
    width:44px; height:44px; border-radius:12px;
    display:flex; align-items:center; justify-content:center;
    font-size:1.3rem; flex-shrink:0;
}
.insight-body h4 { font-size:.78rem; font-weight:600; color:#64748b; margin:0 0 4px; text-transform:uppercase; letter-spacing:.8px; }
.insight-body .val { font-size:1.15rem; font-weight:800; color:#f1f5f9; margin:0 0 2px; }
.insight-body .sub { font-size:.76rem; color:#475569; margin:0; }

@media(max-width:768px) {
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
    <div class="page-badge">📈 Visual Analytics</div>
    <h1 class="page-title">Charts &amp; <span>Trend Analysis</span></h1>
    <p class="page-subtitle">
      Visual exploration of mess feedback — meal distribution, parameter
      performance, quality heatmap, and satisfaction radar.
    </p>
  </div>
</div>
""", unsafe_allow_html=True)


# ── Filters ────────────────────────────────────────────────────────────────────
st.markdown("### 🎛️ Filters")
fc1, fc2 = st.columns([2, 2])
with fc1:
    sel_meals = st.multiselect("Meal Type", MEALS, default=MEALS)
with fc2:
    sel_params = st.multiselect("Parameters", PARAMS, default=PARAMS)

dff           = df[df["Meal"].isin(sel_meals)] if sel_meals else df.copy()
active_params = sel_params if sel_params else PARAMS

st.markdown("---")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION A — MEAL OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec-head">
  <div class="sec-icon amber">🍽️</div>
  <div class="sec-text">
    <h3>Meal Overview</h3>
    <p>Parameter scores per meal type and meal-wise response share</p>
  </div>
</div>
<hr class="sec-rule">
""", unsafe_allow_html=True)

col_a1, col_a2 = st.columns([3, 2], gap="medium")

with col_a1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    meal_param_avg = dff.groupby("Meal")[active_params].mean().reset_index()
    fig_grp = go.Figure()
    for p in active_params:
        fig_grp.add_trace(go.Bar(
            name=p, x=meal_param_avg["Meal"], y=meal_param_avg[p],
            marker_color=PARAM_COLORS.get(p, "#3b82f6"),
            marker_line_color="#0f172a", marker_line_width=1,
        ))
    fig_grp.update_layout(**layout(
        barmode="group", height=300,
        title="Parameter Scores by Meal Type",
        legend=dict(orientation="h", y=-0.22, bgcolor="#1e293b", bordercolor="#334155", borderwidth=1),
        yaxis=dict(range=[0, 5.4], **GRID),
    ))
    st.plotly_chart(fig_grp, use_container_width=True)
    st.markdown("""<div class="insight-strip">💡 <strong>Insight:</strong>
        Each colour represents a different quality parameter. Taller bars are better.
        Look for meals where multiple bars dip — that meal needs overall improvement.
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_a2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    meal_counts = dff["Meal"].value_counts().reset_index()
    meal_counts.columns = ["Meal", "Count"]
    fig_donut = go.Figure(go.Pie(
        labels=meal_counts["Meal"], values=meal_counts["Count"],
        hole=0.58, marker=dict(colors=MEAL_COLORS),
        textinfo="percent+label",
        textfont=dict(size=11, color="#f1f5f9"),
        hovertemplate="<b>%{label}</b><br>Responses: %{value}<br>%{percent}<extra></extra>"
    ))
    fig_donut.add_annotation(
        text=f"<b>{dff.shape[0]}</b><br>Responses",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=13, color="#f1f5f9")
    )
    fig_donut.update_layout(**layout(
        height=300, title="Meal Response Share",
        showlegend=False,
    ))
    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown("""<div class="insight-strip">💡 <strong>Insight:</strong>
        A larger slice = more students responded for that meal.
        Higher response counts make the data more reliable for that meal type.
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION B — PARAMETER COMPARISON
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec-head">
  <div class="sec-icon blue">📐</div>
  <div class="sec-text">
    <h3>Parameter Comparison</h3>
    <p>Quality radar profile and ranked horizontal bar view of all parameters</p>
  </div>
</div>
<hr class="sec-rule">
""", unsafe_allow_html=True)

col_b1, col_b2 = st.columns([2, 3], gap="medium")

with col_b1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    avgs        = dff[active_params].mean().tolist()
    avgs_closed = avgs + [avgs[0]]
    cats_closed = active_params + [active_params[0]]
    fig_radar = go.Figure(go.Scatterpolar(
        r=avgs_closed, theta=cats_closed, fill="toself",
        fillcolor="rgba(59,130,246,0.15)",
        line=dict(color="#3b82f6", width=2),
        marker=dict(color="#3b82f6", size=6),
    ))
    fig_radar.update_layout(**layout(
        height=300, title="Quality Radar Profile",
        polar=dict(
            bgcolor="#1e293b",
            radialaxis=dict(visible=True, range=[0, 5], color="#475569", gridcolor="#334155"),
            angularaxis=dict(color="#94a3b8", gridcolor="#334155"),
        ),
        margin=dict(l=20, r=20, t=44, b=10),
    ))
    st.plotly_chart(fig_radar, use_container_width=True)
    st.markdown("""<div class="insight-strip">💡 <strong>Insight:</strong>
        A perfect pentagon = all parameters equal. Any dip on an axis
        pinpoints the exact quality area that needs improvement.
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_b2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    param_avg_df = dff[active_params].mean().sort_values(ascending=True).reset_index()
    param_avg_df.columns = ["Parameter", "Score"]
    bar_colors = [PARAM_COLORS.get(p, "#3b82f6") for p in param_avg_df["Parameter"]]
    fig_hbar = go.Figure(go.Bar(
        x=param_avg_df["Score"], y=param_avg_df["Parameter"],
        orientation="h",
        marker=dict(color=bar_colors, line=dict(color="#0f172a", width=1)),
        text=[f"  {v:.2f}" for v in param_avg_df["Score"]],
        textposition="outside",
        textfont=dict(color="#f1f5f9", size=12),
        hovertemplate="<b>%{y}</b><br>Score: %{x:.2f} / 5.0<extra></extra>"
    ))
    fig_hbar.add_vline(
        x=3.0, line_dash="dash", line_color="#475569",
        annotation_text="Min. Threshold 3.0",
        annotation_font_color="#64748b"
    )
    fig_hbar.update_layout(**layout(
        height=300, title="Parameter Score Ranking",
        xaxis=dict(range=[0, 6.0], **GRID),
        margin=dict(l=0, r=70, t=44, b=0),
    ))
    st.plotly_chart(fig_hbar, use_container_width=True)
    st.markdown("""<div class="insight-strip">💡 <strong>Insight:</strong>
        Parameters <strong>left of the dashed line</strong> fall below the
        acceptable threshold — these require priority management attention.
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION C — PERFORMANCE HEATMAP
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec-head">
  <div class="sec-icon purple">🗺️</div>
  <div class="sec-text">
    <h3>Performance Heatmap</h3>
    <p>Full meal × parameter score matrix — spot strengths and gaps at a glance</p>
  </div>
</div>
<hr class="sec-rule">
""", unsafe_allow_html=True)

st.markdown('<div class="chart-card">', unsafe_allow_html=True)
heat_df = dff.groupby("Meal")[active_params].mean()
fig_heat = go.Figure(go.Heatmap(
    z=heat_df.values.tolist(),
    x=heat_df.columns.tolist(),
    y=heat_df.index.tolist(),
    colorscale=[
        [0.0, "#3a1a1a"], [0.3, "#7f1d1d"],
        [0.5, "#1e3a5f"], [0.7, "#1d4ed8"],
        [1.0, "#22c55e"]
    ],
    zmin=1, zmax=5,
    text=[[f"{v:.2f}" for v in row] for row in heat_df.values],
    texttemplate="%{text}",
    textfont=dict(color="#ffffff", size=14, family="Inter"),
    hovertemplate="<b>%{y} — %{x}</b><br>Score: %{z:.2f} / 5<extra></extra>",
))
fig_heat.update_layout(**layout(
    height=260, title="Meal × Parameter Performance Heatmap",
    xaxis=dict(side="bottom", **GRID),
    margin=dict(l=0, r=0, t=44, b=0),
))
st.plotly_chart(fig_heat, use_container_width=True)
st.markdown("""<div class="insight-strip">💡 <strong>Insight:</strong>
    <strong>Green cells</strong> = high satisfaction. <strong>Red/dark cells</strong> = poor performance.
    Scan each column to spot parameters that consistently underperform across all meal types.
</div>""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION D — QUICK INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec-head">
  <div class="sec-icon green">💡</div>
  <div class="sec-text">
    <h3>Quick Insights</h3>
    <p>Key takeaways automatically derived from the filtered feedback data</p>
  </div>
</div>
<hr class="sec-rule">
""", unsafe_allow_html=True)

col_avgs    = dff[active_params].mean()
overall_avg = col_avgs.mean()
best_param  = col_avgs.idxmax()
worst_param = col_avgs.idxmin()

meal_scores = dff.groupby("Meal")[active_params].mean().mean(axis=1)
best_meal   = meal_scores.idxmax() if len(meal_scores) else "N/A"
worst_meal  = meal_scores.idxmin() if len(meal_scores) else "N/A"
best_meal_score  = f"{meal_scores[best_meal]:.2f}/5.0"  if len(meal_scores) else "N/A"
worst_meal_score = f"{meal_scores[worst_meal]:.2f}/5.0" if len(meal_scores) else "N/A"

def sat_label(s):
    if s >= 4.0: return "Excellent 🟢"
    if s >= 3.5: return "Good 🔵"
    if s >= 3.0: return "Average 🟡"
    if s >= 2.0: return "Poor 🟠"
    return "Critical 🔴"

st.markdown(f"""
<div class="insights-grid">
  <div class="insight-card">
    <div class="insight-icon-box" style="background:rgba(34,197,94,.12);">🏆</div>
    <div class="insight-body">
      <h4>Best Meal</h4>
      <div class="val">{best_meal}</div>
      <div class="sub">Avg score {best_meal_score} — highest overall student satisfaction</div>
    </div>
  </div>
  <div class="insight-card">
    <div class="insight-icon-box" style="background:rgba(239,68,68,.12);">📉</div>
    <div class="insight-body">
      <h4>Needs Most Improvement</h4>
      <div class="val">{worst_meal}</div>
      <div class="sub">Avg score {worst_meal_score} — lowest rated meal across all parameters</div>
    </div>
  </div>
  <div class="insight-card">
    <div class="insight-icon-box" style="background:rgba(59,130,246,.12);">⭐</div>
    <div class="insight-body">
      <h4>Strongest Parameter</h4>
      <div class="val">{best_param}</div>
      <div class="sub">Rated {col_avgs[best_param]:.2f}/5.0 — the best performing quality area</div>
    </div>
  </div>
  <div class="insight-card">
    <div class="insight-icon-box" style="background:rgba(245,158,11,.12);">⚠️</div>
    <div class="insight-body">
      <h4>Overall Satisfaction</h4>
      <div class="val">{overall_avg:.2f} / 5.0</div>
      <div class="sub">Status: {sat_label(overall_avg)} — based on {dff.shape[0]} responses</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
