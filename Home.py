# streamlit run "Home.py"
import streamlit as st
import pandas as pd
import base64

st.set_page_config(
    page_title="Mess Feedback Dashboard",
    page_icon="🍔",
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

df = load_data()

numeric_cols  = df.select_dtypes(include='number').columns
total_resp    = len(df)
overall_avg   = df[numeric_cols].mean().mean()
best_category = df[numeric_cols].mean().idxmax()
best_meal     = df.groupby("Meal")[numeric_cols].mean().mean(axis=1).idxmax() if "Meal" in df.columns else "N/A"

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* Reset & base */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.block-container { padding-top: 1rem !important; padding-bottom: 2rem !important; }

/* ── Hero ─────────────────────────────────────────────── */
.hero-section {
    background: linear-gradient(135deg, #0f172a 0%, #1a2744 45%, #0f4c81 100%);
    border-radius: 24px;
    padding: 72px 48px 64px 48px;
    text-align: center;
    margin-bottom: 40px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 24px 80px rgba(0,0,0,0.5);
}
.hero-section::before {
    content: '';
    position: absolute; inset: 0;
    background:
        radial-gradient(circle at 15% 50%, rgba(59,130,246,0.18) 0%, transparent 55%),
        radial-gradient(circle at 85% 15%, rgba(99,102,241,0.12) 0%, transparent 50%),
        radial-gradient(circle at 50% 100%, rgba(15,76,129,0.25) 0%, transparent 60%);
    pointer-events: none;
}
.hero-inner {
    position: relative;
    max-width: 760px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(59,130,246,0.15);
    border: 1px solid rgba(59,130,246,0.4);
    color: #93c5fd;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    padding: 7px 20px;
    border-radius: 50px;
    margin-bottom: 28px;
}
.hero-title {
    font-size: clamp(2.4rem, 5vw, 3.8rem);
    font-weight: 800;
    color: #ffffff;
    line-height: 1.12;
    margin: 0 0 20px 0;
    position: relative;
    letter-spacing: -0.5px;
}
.hero-title span {
    color: #60a5fa;
    background: linear-gradient(90deg, #60a5fa, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-subtitle {
    font-size: 1.05rem;
    color: #94a3b8;
    max-width: 560px;
    margin: 0 auto 36px auto;
    line-height: 1.75;
    position: relative;
    font-weight: 400;
}
.hero-divider {
    width: 48px;
    height: 3px;
    background: linear-gradient(90deg, #3b82f6, #6366f1);
    border-radius: 4px;
    margin: 0 auto 32px auto;
}
.hero-tags {
    display: flex;
    gap: 10px;
    justify-content: center;
    flex-wrap: wrap;
    position: relative;
}
.hero-tag {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    color: #cbd5e1;
    padding: 8px 20px;
    border-radius: 50px;
    font-size: 13px;
    font-weight: 500;
    letter-spacing: 0.2px;
    transition: background 0.2s, border-color 0.2s;
}
.hero-tag:hover {
    background: rgba(59,130,246,0.12);
    border-color: rgba(59,130,246,0.35);
}

/* ── Stat Cards ───────────────────────────────────────── */
.stats-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 40px;
}
.stat-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 24px 20px;
    text-align: center;
    transition: transform 0.2s, box-shadow 0.2s;
}
.stat-card:hover { transform: translateY(-4px); box-shadow: 0 12px 32px rgba(0,0,0,0.3); }
.stat-emoji { font-size: 2rem; margin-bottom: 8px; }
.stat-value {
    font-size: 2rem;
    font-weight: 800;
    color: #60a5fa;
    line-height: 1;
    margin-bottom: 6px;
}
.stat-label { font-size: 13px; color: #94a3b8; font-weight: 500; }

/* ── Section Heading ──────────────────────────────────── */
.section-head {
    text-align: center;
    margin: 48px 0 28px 0;
}
.section-head h2 {
    font-size: 1.9rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 8px 0;
}
.section-head p {
    color: #94a3b8;
    font-size: 1rem;
    margin: 0;
}
.section-divider {
    width: 56px; height: 4px;
    background: linear-gradient(90deg, #3b82f6, #6366f1);
    border-radius: 4px;
    margin: 10px auto 0 auto;
}

/* ── Problem / Solution ───────────────────────────────── */
.two-col-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 40px;
}
.ps-card {
    border-radius: 16px;
    padding: 32px 28px;
}
.ps-card.problem {
    background: linear-gradient(135deg, #1e1a2e, #2d1f3d);
    border: 1px solid #4c1d95;
}
.ps-card.solution {
    background: linear-gradient(135deg, #0f2818, #14532d);
    border: 1px solid #166534;
}
.ps-card h3 {
    font-size: 1.2rem;
    font-weight: 700;
    margin: 0 0 14px 0;
}
.ps-card.problem h3 { color: #c4b5fd; }
.ps-card.solution h3 { color: #86efac; }
.ps-card ul { padding-left: 18px; margin: 0; }
.ps-card ul li {
    color: #cbd5e1;
    font-size: 0.95rem;
    line-height: 1.7;
    margin-bottom: 4px;
}

/* ── How It Works Steps ───────────────────────────────── */
.steps-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 40px;
    position: relative;
}
.step-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 28px 20px;
    text-align: center;
    position: relative;
}
.step-number {
    width: 36px; height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, #3b82f6, #6366f1);
    color: white;
    font-size: 14px;
    font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 12px auto;
}
.step-icon { font-size: 2rem; margin-bottom: 10px; }
.step-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 6px;
}
.step-desc { font-size: 0.85rem; color: #94a3b8; line-height: 1.5; }

/* ── Feature Cards ────────────────────────────────────── */
.features-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 18px;
    margin-bottom: 40px;
}
.feature-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 28px 24px;
    display: flex;
    gap: 20px;
    align-items: flex-start;
    transition: transform 0.2s, border-color 0.2s;
}
.feature-card:hover {
    transform: translateY(-3px);
    border-color: #3b82f6;
}
.feature-icon-box {
    width: 52px; height: 52px;
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.6rem;
    flex-shrink: 0;
}
.feature-icon-box.blue  { background: rgba(59,130,246,0.15); }
.feature-icon-box.green { background: rgba(34,197,94,0.15); }
.feature-icon-box.purple{ background: rgba(139,92,246,0.15); }
.feature-icon-box.amber { background: rgba(245,158,11,0.15); }
.feature-body {}
.feature-body h4 {
    font-size: 1rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 6px 0;
}
.feature-body p {
    font-size: 0.88rem;
    color: #94a3b8;
    line-height: 1.6;
    margin: 0;
}

/* ── QR Process ───────────────────────────────────────── */
.qr-banner {
    background: linear-gradient(135deg, #0f172a, #1e3a5f);
    border: 1px solid #1e40af;
    border-radius: 18px;
    padding: 40px 36px;
    margin-bottom: 40px;
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 32px;
    align-items: center;
}
.qr-content h3 {
    font-size: 1.5rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 10px 0;
}
.qr-content p {
    color: #94a3b8;
    font-size: 0.95rem;
    line-height: 1.65;
    margin: 0 0 20px 0;
}
.qr-steps {
    display: flex;
    flex-direction: column;
    gap: 10px;
}
.qr-step {
    display: flex; align-items: center; gap: 12px;
    color: #cbd5e1; font-size: 0.9rem;
}
.qr-step-num {
    width: 26px; height: 26px;
    border-radius: 50%;
    background: #1d4ed8;
    color: white;
    font-size: 12px;
    font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.qr-box {
    background: white;
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    min-width: 130px;
}
.qr-placeholder { font-size: 4.5rem; }
.qr-label {
    font-size: 11px;
    color: #475569;
    font-weight: 600;
    margin-top: 8px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* ── Footer CTA ───────────────────────────────────────── */
.footer-cta {
    text-align: center;
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 36px 24px;
    margin-bottom: 24px;
}
.footer-cta p {
    color: #94a3b8;
    font-size: 0.95rem;
    margin: 8px 0 0 0;
}
.nav-hint {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(59,130,246,0.15);
    border: 1px solid rgba(59,130,246,0.4);
    color: #93c5fd;
    padding: 10px 24px;
    border-radius: 50px;
    font-size: 0.9rem;
    font-weight: 600;
    margin-top: 16px;
}

/* ── QR Card ──────────────────────────────────────── */
.qr-card {
    background: linear-gradient(135deg, #1e293b 0%, #162032 100%);
    border: 1px solid #334155;
    border-radius: 20px;
    padding: 28px 32px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    gap: 32px;
    box-shadow: 0 8px 40px rgba(59,130,246,0.10), 0 2px 12px rgba(0,0,0,0.35);
    position: relative;
    overflow: hidden;
}
.qr-card::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(circle at 5% 50%, rgba(99,102,241,0.08) 0%, transparent 60%);
    pointer-events: none;
}
.qr-img-wrap {
    flex-shrink: 0;
    width: 130px; height: 130px;
    border-radius: 14px;
    border: 2px solid #334155;
    overflow: hidden;
    box-shadow: 0 0 24px rgba(59,130,246,0.18);
    background: #fff;
    display: flex; align-items: center; justify-content: center;
}
.qr-img-wrap img { width: 100%; height: 100%; object-fit: cover; display: block; }
.qr-text { flex: 1; position: relative; }
.qr-eyebrow {
    font-size: 11px; font-weight: 700; letter-spacing: 1.6px;
    text-transform: uppercase; color: #64748b; margin-bottom: 8px;
}
.qr-title {
    font-size: 1.25rem; font-weight: 800; color: #f1f5f9;
    margin: 0 0 6px; line-height: 1.2;
}
.qr-title span {
    background: linear-gradient(90deg, #60a5fa, #818cf8);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.qr-desc { font-size: .85rem; color: #64748b; line-height: 1.6; margin: 0 0 16px; max-width: 380px; }
.qr-btn {
    display: inline-flex; align-items: center; gap: 8px;
    background: linear-gradient(135deg, #3b82f6, #6366f1);
    color: #fff !important; text-decoration: none !important;
    font-size: .85rem; font-weight: 700;
    padding: 9px 22px; border-radius: 50px;
    box-shadow: 0 4px 18px rgba(59,130,246,0.30);
    transition: transform .2s, box-shadow .2s;
    letter-spacing: .3px;
}
.qr-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(99,102,241,0.40);
}
.qr-accent {
    position: absolute; right: -20px; top: -20px;
    width: 120px; height: 120px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(99,102,241,0.10) 0%, transparent 70%);
}

/* Responsive tweaks */
@media (max-width: 768px) {
    .stats-row, .steps-grid { grid-template-columns: repeat(2, 1fr); }
    .two-col-grid, .features-grid { grid-template-columns: 1fr; }
    .qr-banner { grid-template-columns: 1fr; }
    .qr-card { flex-direction: column; text-align: center; padding: 24px 20px; gap: 20px; }
    .qr-img-wrap { margin: 0 auto; }
    .qr-desc { max-width: 100%; }
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HERO SECTION
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="hero-section">
    <div class="hero-inner">
        <div class="hero-badge">🏫 PVGCOET &nbsp;·&nbsp; Design Thinking Project</div>
        <h1 class="hero-title">
            Mess Feedback<br>
            <span>Intelligence Dashboard</span>
        </h1>
        <div class="hero-divider"></div>
        <p class="hero-subtitle">
            A data-driven platform that transforms anonymous student mess
            feedback into actionable insights — powered by statistical
            analysis and generative AI.
        </p>
        <div class="hero-tags">
            <span class="hero-tag">📊 Statistical Analysis</span>
            <span class="hero-tag">🤖 AI Insights</span>
            <span class="hero-tag">📱 QR Feedback</span>
            <span class="hero-tag">📈 Visualizations</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# QR FEEDBACK CARD
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""

qr_b64 = get_base64_image("assets/feedback_qr.jpeg")
qr_img_html = f'<img src="data:image/jpeg;base64,{qr_b64}" alt="QR Code">' if qr_b64 else ''

st.markdown(f"""
<div class="qr-card">
    <div class="qr-accent"></div>
    <div class="qr-img-wrap">
        {qr_img_html}
    </div>
    <div class="qr-text">
        <div class="qr-eyebrow">📱 Student Feedback Portal</div>
        <div class="qr-title">Scan to Submit <span>Feedback</span></div>
        <p class="qr-desc">
            Students can instantly rate their mess experience — Taste, Hygiene,
            Temperature, Quantity &amp; more — by scanning the QR code or clicking the link below.
        </p>
        <a class="qr-btn"
           href="https://docs.google.com/forms/d/e/1FAIpQLSfKgqcU2eikaDqUqWw1zlQEQUZ1063rqEMwu9uGawT5sJEe7w/viewform?usp=dialog"
           target="_blank" rel="noopener noreferrer">
            📋 Open Feedback Form
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# LIVE STATS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="stats-row">
    <div class="stat-card">
        <div class="stat-emoji">📋</div>
        <div class="stat-value">{total_resp}</div>
        <div class="stat-label">Total Responses</div>
    </div>
    <div class="stat-card">
        <div class="stat-emoji">⭐</div>
        <div class="stat-value">{overall_avg:.2f}</div>
        <div class="stat-label">Avg. Rating / 5.0</div>
    </div>
    <div class="stat-card">
        <div class="stat-emoji">🏆</div>
        <div class="stat-value">{best_category}</div>
        <div class="stat-label">Best Rated Category</div>
    </div>
    <div class="stat-card">
        <div class="stat-emoji">🍽️</div>
        <div class="stat-value">{best_meal}</div>
        <div class="stat-label">Best Rated Meal</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SMART ALERTS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="section-head">
    <h2>🔔 Smart Alerts</h2>
    <p>Automatic flags raised from the latest feedback data</p>
    <div class="section-divider"></div>
</div>
""", unsafe_allow_html=True)

# ── Compute per-category and per-meal averages ─────────────────────────────
col_avgs     = df[numeric_cols].mean()
WARN_LOW     = 3.0   # below this → warning
CRIT_LOW     = 2.5   # below this → error

alerts_shown = 0

# 1. Overall satisfaction check
if overall_avg < CRIT_LOW:
    st.error(f"🚨 **Critical: Overall Satisfaction is Very Low** — Average rating is only **{overall_avg:.2f}/5.0**. Immediate attention required across all mess parameters.")
    alerts_shown += 1
elif overall_avg < WARN_LOW:
    st.warning(f"⚠️ **Low Overall Satisfaction** — Average rating is **{overall_avg:.2f}/5.0**, which is below the acceptable threshold of 3.0. Review all parameters.")
    alerts_shown += 1
else:
    st.success(f"✅ **Overall Satisfaction is Good** — Students rate the mess **{overall_avg:.2f}/5.0** on average. Keep maintaining quality!")
    alerts_shown += 1

# 2. Hygiene check
if "Hygiene" in col_avgs:
    hyg = col_avgs["Hygiene"]
    if hyg < CRIT_LOW:
        st.error(f"🦠 **Critical Hygiene Alert** — Hygiene is rated at **{hyg:.2f}/5.0**. This is a health risk. Immediate deep cleaning and inspection required.")
        alerts_shown += 1
    elif hyg < WARN_LOW:
        st.warning(f"🧹 **Hygiene Needs Improvement** — Hygiene score is **{hyg:.2f}/5.0**. Students have flagged cleanliness concerns. Review sanitation protocols.")
        alerts_shown += 1

# 3. Food Temperature check
if "Temperature" in col_avgs:
    temp = col_avgs["Temperature"]
    if temp < CRIT_LOW:
        st.error(f"🌡️ **Food Temperature Critical** — Temperature score is **{temp:.2f}/5.0**. Students are consistently receiving cold food. Review heating processes.")
        alerts_shown += 1
    elif temp < WARN_LOW:
        st.warning(f"🌡️ **Food Temperature Warning** — Temperature score is **{temp:.2f}/5.0**. Food may not be served at optimal temperature. Check meal serving timings.")
        alerts_shown += 1

# 4. Taste check
if "Taste" in col_avgs:
    taste = col_avgs["Taste"]
    if taste < CRIT_LOW:
        st.error(f"😣 **Taste Rated Very Poorly** — Taste score is **{taste:.2f}/5.0**. A major driver of dissatisfaction. Engage with the kitchen team immediately.")
        alerts_shown += 1
    elif taste < WARN_LOW:
        st.warning(f"😕 **Taste Needs Attention** — Taste score is **{taste:.2f}/5.0**. Students find the food below expectations. Consider menu variety or recipe adjustments.")
        alerts_shown += 1

# 5. Quantity check
if "Quantity" in col_avgs:
    qty = col_avgs["Quantity"]
    if qty < CRIT_LOW:
        st.error(f"📉 **Quantity Severely Insufficient** — Quantity score is **{qty:.2f}/5.0**. Students are not getting adequate portions. Increase serving quantities.")
        alerts_shown += 1
    elif qty < WARN_LOW:
        st.warning(f"🍽️ **Quantity Below Expected** — Quantity score is **{qty:.2f}/5.0**. Consider reviewing portion sizes, especially for high-demand meals.")
        alerts_shown += 1

# 6. Best & Worst rated category
best_cat  = col_avgs.idxmax()
worst_cat = col_avgs.idxmin()
st.info(f"🏆 **Top Rated Parameter: {best_cat}** — Rated **{col_avgs[best_cat]:.2f}/5.0**. This is the strongest area of the mess. Maintain and highlight this quality.")
if col_avgs[worst_cat] < WARN_LOW:
    st.warning(f"🔻 **Lowest Rated Parameter: {worst_cat}** — Rated only **{col_avgs[worst_cat]:.2f}/5.0**. This needs priority attention for improving student satisfaction.")
else:
    st.info(f"📌 **Lowest Rated Parameter: {worst_cat}** — Rated **{col_avgs[worst_cat]:.2f}/5.0**. Still acceptable, but monitor for any downward trends.")

# 7. Meal-wise alerts
if "Meal" in df.columns:
    meal_avgs = df.groupby("Meal")[numeric_cols].mean().mean(axis=1)
    worst_meal = meal_avgs.idxmin()
    best_meal_name  = meal_avgs.idxmax()
    if meal_avgs[worst_meal] < WARN_LOW:
        st.warning(f"🍛 **Meal Alert: '{worst_meal}'** is the lowest-rated meal at **{meal_avgs[worst_meal]:.2f}/5.0**. Focus improvement efforts on this meal's quality and presentation.")
    st.success(f"⭐ **Best Meal: '{best_meal_name}'** scores **{meal_avgs[best_meal_name]:.2f}/5.0** — the most popular and well-received meal among students.")


# ══════════════════════════════════════════════════════════════════════════════
# PROBLEM & SOLUTION
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="section-head">
    <h2>🎯 Problem Statement & Solution</h2>
    <p>Why this dashboard exists — and what it solves</p>
    <div class="section-divider"></div>
</div>

<div class="two-col-grid">
    <div class="ps-card problem">
        <h3>❌ The Problem</h3>
        <ul>
            <li>Mess feedback was collected on paper — hard to analyze</li>
            <li>No structured way to identify recurring complaints</li>
            <li>Management had no real-time view of student satisfaction</li>
            <li>Positive aspects were never recognized or reinforced</li>
            <li>Suggestions from students went unheard and untracked</li>
        </ul>
    </div>
    <div class="ps-card solution">
        <h3>✅ Our Solution</h3>
        <ul>
            <li>QR-code based digital feedback collection at mess entry/exit</li>
            <li>Centralized dataset with structured rating parameters</li>
            <li>Live statistical dashboard for meal-wise & parameter analysis</li>
            <li>Interactive visualizations for trend identification</li>
            <li>AI-generated summaries with actionable recommendations</li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HOW IT WORKS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="section-head">
    <h2>⚙️ How It Works</h2>
    <p>From feedback to insight in four simple steps</p>
    <div class="section-divider"></div>
</div>

<div class="steps-grid">
    <div class="step-card">
        <div class="step-number">1</div>
        <div class="step-icon">📱</div>
        <div class="step-title">QR Code Scan</div>
        <div class="step-desc">Students scan a QR code displayed in the mess to access a Google Form.</div>
    </div>
    <div class="step-card">
        <div class="step-number">2</div>
        <div class="step-icon">📝</div>
        <div class="step-title">Submit Feedback</div>
        <div class="step-desc">Rate Taste, Temperature, Quantity, Hygiene & Overall Experience on a 1–5 scale.</div>
    </div>
    <div class="step-card">
        <div class="step-number">3</div>
        <div class="step-icon">🗄️</div>
        <div class="step-title">Data Aggregation</div>
        <div class="step-desc">Responses are collected in a CSV dataset and processed for analysis.</div>
    </div>
    <div class="step-card">
        <div class="step-number">4</div>
        <div class="step-icon">📊</div>
        <div class="step-title">Dashboard Insights</div>
        <div class="step-desc">Stats, charts, and AI summaries surface actionable insights for management.</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# FEATURE HIGHLIGHTS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="section-head">
    <h2>✨ Feature Highlights</h2>
    <p>Everything packed inside this dashboard</p>
    <div class="section-divider"></div>
</div>

<div class="features-grid">
    <div class="feature-card">
        <div class="feature-icon-box blue">📱</div>
        <div class="feature-body">
            <h4>QR-Based Feedback Collection</h4>
            <p>Students scan a QR code to instantly submit structured feedback after every meal — no paper, no manual entry, no friction.</p>
        </div>
    </div>
    <div class="feature-card">
        <div class="feature-icon-box green">📊</div>
        <div class="feature-body">
            <h4>Statistical Analysis</h4>
            <p>Explore raw data, meal-wise averages, and parameter breakdowns through beautifully styled tables with gradient highlighting.</p>
        </div>
    </div>
    <div class="feature-card">
        <div class="feature-icon-box purple">🤖</div>
        <div class="feature-body">
            <h4>AI-Generated Insights</h4>
            <p>Gemma 4 AI analyzes the full dataset and returns structured summaries — positives, negatives, and improvement suggestions.</p>
        </div>
    </div>
    <div class="feature-card">
        <div class="feature-icon-box amber">📈</div>
        <div class="feature-body">
            <h4>Visualization Dashboard</h4>
            <p>Interactive bar charts, pie charts, and rating distributions let management spot trends and compare meals at a glance.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# QR PROCESS BANNER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="qr-banner">
    <div class="qr-content">
        <h3>📱 QR-Based Feedback Process</h3>
        <p>
            We replaced paper feedback slips with a seamless QR code system.
            A printed QR code placed at the mess counter links directly to a Google Form,
            making it effortless for students to rate their meal in under 30 seconds.
        </p>
        <div class="qr-steps">
            <div class="qr-step">
                <div class="qr-step-num">1</div>
                <span>📷 Student scans QR code at the mess counter</span>
            </div>
            <div class="qr-step">
                <div class="qr-step-num">2</div>
                <span>📋 Google Form opens with rating fields</span>
            </div>
            <div class="qr-step">
                <div class="qr-step-num">3</div>
                <span>✅ Response saved to shared Google Sheet / CSV</span>
            </div>
            <div class="qr-step">
                <div class="qr-step-num">4</div>
                <span>📊 Dashboard auto-refreshes with new data</span>
            </div>
        </div>
    </div>
    <div class="qr-box">
        <div class="qr-placeholder">⬛</div>
        <div style="font-size:3rem; margin-top:-30px;">📱</div>
        <div class="qr-label">Scan to Rate</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# FOOTER CTA
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer-cta">
    <h3 style="color:#f1f5f9; font-size:1.2rem; margin:0;">
        🚀 Ready to explore the data?
    </h3>
    <p>Use the sidebar on the left to navigate between pages.</p>
    <div class="nav-hint">👈 Statistical Data &nbsp;·&nbsp; 📈 Charts &nbsp;·&nbsp; 🤖 AI Insights</div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PROJECT TEAM
# ══════════════════════════════════════════════════════════════════════════════

# CSS only — separate call so Streamlit doesn't confuse style with content
st.markdown("""
<style>
.team-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 28px 16px 24px 16px;
    text-align: center;
    transition: transform 0.22s ease, border-color 0.22s ease, box-shadow 0.22s ease;
    position: relative;
    overflow: hidden;
    height: 100%;
}
.team-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #3b82f6, #6366f1, #8b5cf6);
    border-radius: 16px 16px 0 0;
}
.team-card:hover {
    transform: translateY(-5px);
    border-color: #3b82f6;
    box-shadow: 0 16px 40px rgba(59,130,246,0.15);
}
.team-avatar {
    width: 60px; height: 60px;
    border-radius: 50%;
    background: linear-gradient(135deg, #1d4ed8, #6366f1);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.6rem;
    margin: 0 auto 14px auto;
    border: 2px solid #334155;
}
.team-name {
    font-size: 0.95rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 6px;
    line-height: 1.3;
}
.team-role {
    font-size: 0.78rem;
    color: #64748b;
    line-height: 1.5;
    font-weight: 500;
}
.team-role-badge {
    display: block;
    width: 72px;
    background: rgba(59,130,246,0.12);
    border: 1px solid rgba(59,130,246,0.25);
    color: #93c5fd;
    font-size: 0.72rem;
    font-weight: 700;
    padding: 4px 0;
    border-radius: 50px;
    margin: 12px auto 0 auto;
    text-align: center;
    letter-spacing: 0.4px;
}
.site-footer {
    text-align: center;
    padding: 24px 0 8px 0;
    border-top: 1px solid #1e293b;
    margin-top: 24px;
}
.site-footer p {
    color: #475569;
    font-size: 0.82rem;
    margin: 0;
    letter-spacing: 0.5px;
}
.site-footer span { color: #3b82f6; font-weight: 600; }
.guide-block {
    text-align: center;
    margin: 28px auto 0 auto;
    padding: 18px 32px;
    background: rgba(59,130,246,0.06);
    border: 1px solid rgba(59,130,246,0.18);
    border-radius: 12px;
    max-width: 380px;
}
.guide-label {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 6px;
}
.guide-name {
    font-size: 1rem;
    font-weight: 700;
    color: #e2e8f0;
}
.guide-sub {
    font-size: 0.78rem;
    color: #64748b;
    margin-top: 3px;
    font-weight: 400;
}
</style>
""", unsafe_allow_html=True)

# Section heading
st.markdown("""
<div class="section-head">
    <h2>👨‍💻 Project Team</h2>
    <p>The minds behind the Mess Feedback Intelligence Dashboard</p>
    <div class="section-divider"></div>
</div>
""", unsafe_allow_html=True)

# Team members using native st.columns — renders reliably
team = [
    ("🧠", "Sarthak Kharade",  "AI Integration & Dashboard", "Tech"),
    ("🎨", "Samir Myanawar",   "UI & Visualization",         "Design"),
    ("📋", "Soham Jawalkar",   "Data Collection",            "Data"),
    ("📊", "Ayush Janunkar",   "Analysis & Testing",         "Testing"),
    ("📝", "Atharva Nale",     "Research & Documentation",   "Research"),
]

cols = st.columns(5)
for col, (emoji, name, role, badge) in zip(cols, team):
    with col:
        st.markdown(f"""
        <div class="team-card">
            <div class="team-avatar">{emoji}</div>
            <div class="team-name">{name}</div>
            <div class="team-role">{role}</div>
            <div class="team-role-badge">{badge}</div>
        </div>
        """, unsafe_allow_html=True)

# Guide / Faculty Mentor
st.markdown("""
<div class="guide-block">
    <div class="guide-label">🎓 Guided By</div>
    <div class="guide-name">Prof. Dr. P. V. Rishbud</div>
    <div class="guide-sub">Faculty Mentor &nbsp;&middot;&nbsp; PVGCOET</div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="site-footer">
    <p><span>PVGCOET</span> &nbsp;|&nbsp; Digital Feedback Management System &nbsp;|&nbsp; <span>2026</span></p>
</div>
""", unsafe_allow_html=True)


