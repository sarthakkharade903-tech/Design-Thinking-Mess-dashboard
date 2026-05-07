import streamlit as st
import pandas as pd
import os
import re
import requests
from dotenv import load_dotenv

# ── Config & API ───────────────────────────────────────────────────────────────
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

st.set_page_config(
    page_title="AI Insights | Mess Feedback",
    page_icon="🤖",
    layout="wide"
)

# ── Load Data ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
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
    except Exception:
        return None

df = load_data()

# Pre-compute stats for summary cards
if df is not None and not df.empty:
    numeric_cols  = df.select_dtypes(include='number').columns.tolist()
    col_avgs      = df[numeric_cols].mean()
    overall_avg   = col_avgs.mean()
    best_param    = col_avgs.idxmax()
    worst_param   = col_avgs.idxmin()

    def sat_label(s):
        if s >= 4.0: return ("Excellent", "#22c55e")
        if s >= 3.5: return ("Good",      "#3b82f6")
        if s >= 3.0: return ("Average",   "#f59e0b")
        if s >= 2.0: return ("Poor",      "#f97316")
        return ("Critical", "#ef4444")

    sat_text, sat_color = sat_label(overall_avg)
else:
    overall_avg  = 0
    best_param   = "N/A"
    worst_param  = "N/A"
    sat_text     = "N/A"
    sat_color    = "#64748b"

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.block-container { padding-top: 1rem !important; padding-bottom: 2rem !important; }

/* ── Page Header ───────────────────── */
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
        radial-gradient(circle at 90% 20%, rgba(168,85,247,.10) 0%, transparent 50%);
    pointer-events:none;
}
.page-header-inner { position:relative; max-width:720px; }
.page-badge {
    display:inline-flex; align-items:center; gap:6px;
    background:rgba(168,85,247,.15); border:1px solid rgba(168,85,247,.4);
    color:#d8b4fe; font-size:11px; font-weight:600;
    letter-spacing:1.8px; text-transform:uppercase;
    padding:6px 16px; border-radius:50px; margin-bottom:20px;
}
.page-title {
    font-size:clamp(1.8rem,4vw,2.8rem); font-weight:800;
    color:#fff; line-height:1.15; margin:0 0 12px; letter-spacing:-.4px;
}
.page-title span {
    background:linear-gradient(90deg,#a78bfa,#818cf8);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
}
.page-subtitle { font-size:.97rem; color:#94a3b8; line-height:1.65; margin:0; max-width:560px; }

/* ── Summary Cards ─────────────────── */
.summary-row {
    display:grid; grid-template-columns:repeat(4,1fr);
    gap:14px; margin-bottom:28px;
}
.summary-card {
    background:#1e293b; border:1px solid #334155;
    border-radius:14px; padding:18px 16px;
    text-align:center; position:relative; overflow:hidden;
    transition:transform .2s, box-shadow .2s, border-color .2s;
}
.summary-card::after {
    content:''; position:absolute; bottom:0; left:0; right:0;
    height:2px; background:linear-gradient(90deg,#a78bfa,#6366f1);
    transform:scaleX(0); transition:transform .3s ease;
}
.summary-card:hover { transform:translateY(-4px); box-shadow:0 12px 32px rgba(0,0,0,.3); border-color:#6366f1; }
.summary-card:hover::after { transform:scaleX(1); }
.s-icon  { font-size:1.6rem; margin-bottom:6px; }
.s-value { font-size:1.5rem; font-weight:800; color:#a78bfa; line-height:1; margin-bottom:4px; }
.s-label { font-size:11px; color:#64748b; font-weight:600; text-transform:uppercase; letter-spacing:.8px; }

/* ── Generate Area ───────────────── */
.gen-area {
    background:#1e293b; border:1px solid #334155;
    border-radius:14px; padding:20px 22px;
    margin-bottom:20px;
}

/* ── Generate Button Override ────────── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #a78bfa) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 36px !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.3px !important;
    width: 100% !important;
    transition: all .25s ease !important;
    box-shadow: 0 4px 20px rgba(99,102,241,.35) !important;
}
.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 28px rgba(167,139,250,.45) !important;
}

/* ── Empty State ───────────────── */
.empty-state {
    text-align:center; padding:36px 24px;
    background:#1e293b; border:1px dashed #334155;
    border-radius:14px; margin-bottom:16px;
}
.empty-state .es-icon { font-size:3rem; margin-bottom:12px; opacity:.65; }
.empty-state h3 { font-size:1rem; font-weight:700; color:#e2e8f0; margin:0 0 6px; }
.empty-state p  { font-size:.84rem; color:#64748b; max-width:400px; margin:0 auto; line-height:1.6; }

/* ── AI Output Cards ───────────────── */
.ai-card {
    border-radius:14px; padding:22px 22px 18px;
    margin-bottom:16px; border:1px solid;
}
.ai-card.summary  { background:rgba(99,102,241,.07);  border-color:rgba(99,102,241,.25); box-shadow:0 4px 20px rgba(99,102,241,.08); }
.ai-card.positive { background:rgba(34,197,94,.06);   border-color:rgba(34,197,94,.22); box-shadow:0 4px 20px rgba(34,197,94,.08); }
.ai-card.negative { background:rgba(245,158,11,.06);  border-color:rgba(245,158,11,.22); box-shadow:0 4px 20px rgba(245,158,11,.08); }
.ai-card.suggest  { background:rgba(59,130,246,.06);  border-color:rgba(59,130,246,.22); box-shadow:0 4px 20px rgba(59,130,246,.08); }
.ai-card-head {
    display:flex; align-items:center; gap:10px;
    margin-bottom:14px; padding-bottom:12px;
    border-bottom:1px solid rgba(255,255,255,.06);
}
.ai-card-head .head-icon {
    width:36px; height:36px; border-radius:10px;
    display:flex; align-items:center; justify-content:center; font-size:1.1rem; flex-shrink:0;
}
.ai-card-head h4 { font-size:1rem; font-weight:700; color:#f1f5f9; margin:0; }
.ai-card-body  { font-size:.95rem; color:#cbd5e1; line-height:1.8; white-space:pre-wrap; }
.ai-card-body strong, .ai-card-body b { color:#fff; }

/* ── Sec head ──────────────────── */
.sec-head { display:flex; align-items:center; gap:12px; margin:24px 0 4px; }
.sec-icon { width:36px; height:36px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:1rem; flex-shrink:0; }
.sec-icon.purple { background:rgba(168,85,247,.15); }
.sec-text h3 { font-size:1rem; font-weight:700; color:#f1f5f9; margin:0 0 1px; }
.sec-text p  { font-size:.8rem; color:#64748b; margin:0; }
.sec-rule { height:1px; background:linear-gradient(90deg,#334155 0%,transparent 100%); margin:6px 0 14px; border:none; }

@media(max-width:768px) { .summary-row { grid-template-columns:repeat(2,1fr); } }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="page-header">
  <div class="page-header-inner">
    <div class="page-badge">🤖 Generative AI</div>
    <h1 class="page-title">AI-Powered <span>Insights</span></h1>
    <p class="page-subtitle">
      Automated analysis of student mess feedback using large language models.
      Get actionable summaries, positives, concerns, and improvement suggestions
      — generated directly from your dataset.
    </p>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SUMMARY CARDS
# ══════════════════════════════════════════════════════════════════════════════
api_status_icon  = "🟢" if API_KEY else "🔴"
api_status_label = "Connected" if API_KEY else "Key Missing"
api_status_color = "#22c55e" if API_KEY else "#ef4444"

st.markdown(f"""
<div class="summary-row">
  <div class="summary-card">
    <div class="s-icon">⭐</div>
    <div class="s-value">{overall_avg:.2f}</div>
    <div class="s-label">Overall Satisfaction</div>
  </div>
  <div class="summary-card">
    <div class="s-icon">🏆</div>
    <div class="s-value" style="font-size:1.1rem;">{best_param}</div>
    <div class="s-label">Most Praised Area</div>
  </div>
  <div class="summary-card">
    <div class="s-icon">⚠️</div>
    <div class="s-value" style="font-size:1.1rem;">{worst_param}</div>
    <div class="s-label">Biggest Concern</div>
  </div>
  <div class="summary-card">
    <div class="s-icon">{api_status_icon}</div>
    <div class="s-value" style="color:{api_status_color}; font-size:1.1rem;">{api_status_label}</div>
    <div class="s-label">AI API Status</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── Guard rails ────────────────────────────────────────────────────────────────
if not API_KEY:
    st.error("**API Key Missing** — Add `OPENROUTER_API_KEY` to your `.env` file to enable AI Insights.", icon="🔑")
    st.stop()

if df is None or df.empty:
    st.error("**Dataset Error** — Could not load `Updated PVGCOET Mess Feedback.csv`. Check the file path.", icon="📂")
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
# GENERATE SECTION
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec-head">
  <div class="sec-icon purple">🚀</div>
  <div class="sec-text">
    <h3>Generate Analysis</h3>
    <p>Click below to send the dataset to the AI model and receive structured insights</p>
  </div>
</div>
<hr class="sec-rule">
""", unsafe_allow_html=True)

st.markdown('<div class="gen-area">', unsafe_allow_html=True)

info_col, btn_col = st.columns([3, 1], gap="large")
with info_col:
    st.markdown(f"""
    <div style="padding: 4px 0;">
        <div style="font-size:.88rem; color:#64748b; margin-bottom:4px; font-weight:600; text-transform:uppercase; letter-spacing:.8px;">Model</div>
        <div style="font-size:.95rem; color:#e2e8f0; font-weight:600;">google/gemma-4-31b-it:free &nbsp;·&nbsp; OpenRouter API</div>
        <div style="font-size:.8rem; color:#475569; margin-top:6px;">
            Dataset: <strong style="color:#94a3b8;">{len(df)} responses</strong> &nbsp;·&nbsp;
            Parameters: <strong style="color:#94a3b8;">Taste, Temperature, Quantity, Hygiene, Experience</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)
with btn_col:
    generate = st.button("✨ Generate AI Insights")

st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# EMPTY STATE (shown before generation)
# ══════════════════════════════════════════════════════════════════════════════
if not generate:
    st.markdown("""
    <div class="empty-state">
        <div class="es-icon">🧠</div>
        <h3>AI Insights Not Yet Generated</h3>
        <p>
            Click <strong>✨ Generate AI Insights</strong> above to analyse the full student
            feedback dataset and receive structured, AI-powered recommendations for the mess management team.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
# AI GENERATION & OUTPUT
# ══════════════════════════════════════════════════════════════════════════════
summary_stats = df.describe().to_csv()
raw_data_csv  = df.to_csv(index=False)

prompt = f"""You are an expert data analyst. I am providing student feedback data for a mess/cafeteria.
Scores are out of 5 for Taste, Temperature, Quantity, Hygiene, and Experience.

Summary statistics:
{summary_stats}

Raw data:
{raw_data_csv}

Analyze this data and provide insights structured EXACTLY with these markdown headings:
### Overall Summary
### Positive Insights
### Negative Insights
### Suggestions

Keep insights concise, actionable, and data-specific."""

# Loading state with styled spinner message
loading_placeholder = st.empty()
loading_placeholder.markdown("""
<div style="
    background:#1e293b; border:1px solid #334155; border-radius:14px;
    padding:32px 24px; text-align:center; margin-bottom:16px;
">
    <div style="font-size:2.2rem; margin-bottom:12px;">⚙️</div>
    <div style="font-size:1rem; font-weight:700; color:#e2e8f0; margin-bottom:6px;">AI is analysing student feedback…</div>
    <div style="font-size:.85rem; color:#64748b;">Sending data to the model · Please wait a moment</div>
</div>
""", unsafe_allow_html=True)

try:
    with st.spinner("Contacting OpenRouter API…"):
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type":  "application/json"
        }
        full_prompt = "You are a helpful AI assistant analysing mess feedback data.\n\n" + prompt
        payload = {
            "model":    "google/gemma-4-31b-it:free",
            "messages": [{"role": "user", "content": full_prompt}],
            "temperature": 0.3,
            "max_tokens":  1000
        }
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )

    # Clear loading card
    loading_placeholder.empty()

    if response.status_code != 200:
        st.error(f"**API Error {response.status_code}:** {response.text}", icon="🚫")
        st.stop()

    ai_content = response.json()["choices"][0]["message"]["content"]

    # ── Success banner ──────────────────────────────────────────────────────
    st.markdown("""
    <div style="
        background:rgba(34,197,94,.07); border:1px solid rgba(34,197,94,.22);
        border-radius:10px; padding:10px 16px; margin-bottom:16px;
        display:flex; align-items:center; gap:10px;
    ">
        <span style="font-size:1.1rem;">✅</span>
        <div style="font-size:.86rem; font-weight:600; color:#86efac;">
            Analysis complete &nbsp;<span style="color:#4ade80; font-weight:400; opacity:.85;">— AI insights generated successfully</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Section heading ─────────────────────────────────────────────────────
    st.markdown("""
    <div class="sec-head">
      <div class="sec-icon purple">📋</div>
      <div class="sec-text">
        <h3>AI Generated Report</h3>
        <p>Structured analysis across 4 insight dimensions</p>
      </div>
    </div>
    <hr class="sec-rule">
    """, unsafe_allow_html=True)

    # ── Parse & render sections ─────────────────────────────────────────────
    CARD_CONFIG = {
        "Overall Summary":   ("summary",  "📊", "rgba(99,102,241,.18)",  "#818cf8", "Overall Summary"),
        "Positive Insights": ("positive", "✅", "rgba(34,197,94,.18)",   "#4ade80", "Positive Insights"),
        "Negative Insights": ("negative", "⚠️", "rgba(245,158,11,.18)", "#fbbf24", "Negative Insights"),
        "Suggestions":       ("suggest",  "💡", "rgba(59,130,246,.18)",  "#60a5fa", "Suggestions"),
    }

    sections = re.split(r'(?i)###\s*', ai_content)
    rendered = 0

    for section in sections:
        if not section.strip():
            continue
        parts   = section.split('\n', 1)
        heading = parts[0].strip()
        content = parts[1].strip() if len(parts) > 1 else ""

        matched = None
        for key, cfg in CARD_CONFIG.items():
            if key.lower() in heading.lower():
                matched = cfg
                break

        if matched:
            css_cls, icon, icon_bg, icon_color, label = matched
            st.markdown(f"""
            <div class="ai-card {css_cls}">
              <div class="ai-card-head">
                <div class="head-icon" style="background:{icon_bg};">
                  <span style="color:{icon_color};">{icon}</span>
                </div>
                <h4>{label}</h4>
              </div>
              <div class="ai-card-body">{content}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            if heading:
                st.markdown(f"""
                <div class="ai-card summary">
                  <div class="ai-card-head">
                    <div class="head-icon" style="background:rgba(99,102,241,.18);">🔍</div>
                    <h4>{heading}</h4>
                  </div>
                  <div class="ai-card-body">{content}</div>
                </div>
                """, unsafe_allow_html=True)
        rendered += 1

    # Fallback if no sections parsed
    if rendered == 0:
        st.markdown(f"""
        <div class="ai-card summary">
          <div class="ai-card-head">
            <div class="head-icon" style="background:rgba(99,102,241,.18);">📋</div>
            <h4>AI Analysis</h4>
          </div>
          <div class="ai-card-body">{ai_content}</div>
        </div>
        """, unsafe_allow_html=True)

except requests.exceptions.Timeout:
    loading_placeholder.empty()
    st.error("**Request Timed Out** — The AI model took too long to respond. Please try again.", icon="⏱️")
except Exception as e:
    loading_placeholder.empty()
    st.error(f"**Unexpected Error:** {str(e)}", icon="🚫")
