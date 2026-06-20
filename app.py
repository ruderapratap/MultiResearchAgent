import sys
import os

# ── Fix import path so pipeline.py is always found next to app.py ──────────────
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
if _THIS_DIR not in sys.path:
    sys.path.insert(0, _THIS_DIR)

import streamlit as st
import time
from datetime import datetime

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchAI — Multi-Agent Pipeline",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@700&display=swap');

/* Root palette */
:root {
    --burnt:   #E97451;
    --gold:    #DAA06D;
    --tan:     #C19A6B;
    --umber:   #AF6E4D;
    --earth:   #81613E;
    --cream:   #F5F5DC;
    --wheat:   #EFDFBB;
    --text:    #1A1108;
    --subtext: #4A3728;
    --muted:   #7A5C46;
    --card-bg: #FAF6EE;
    --border:  #DDCFB8;
}

/* Global */
html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }
.stApp { background: linear-gradient(145deg, #F5F5DC 0%, #EFDFBB 100%); }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1A1108 0%, #2E1E0F 50%, #3D2A14 100%);
    border-right: 2px solid var(--umber);
}
section[data-testid="stSidebar"] * { color: var(--cream) !important; }
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 { color: var(--gold) !important; }

/* Brand title */
.brand-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 700;
    background: linear-gradient(135deg, #DAA06D, #E97451);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    padding: 0.5rem 0 0.2rem;
    letter-spacing: 0.5px;
}
.brand-sub {
    text-align: center;
    font-size: 0.7rem;
    color: var(--muted) !important;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}

/* Cards */
.res-card {
    background: var(--card-bg);
    border: 1.5px solid var(--border);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 4px 20px rgba(100,60,20,0.08);
    transition: transform 0.2s, box-shadow 0.2s;
}
.res-card:hover { transform: translateY(-2px); box-shadow: 0 8px 30px rgba(100,60,20,0.13); }

/* Card header row */
.card-header {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    margin-bottom: 0.9rem;
}
.card-icon-wrap {
    width: 44px; height: 44px;
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem;
    flex-shrink: 0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15), inset 0 1px 0 rgba(255,255,255,0.25);
}
.icon-search  { background: linear-gradient(145deg,#E97451,#C0522E); }
.icon-reader  { background: linear-gradient(145deg,#DAA06D,#B07A3A); }
.icon-writer  { background: linear-gradient(145deg,#C19A6B,#8A5E35); }
.icon-critic  { background: linear-gradient(145deg,#AF6E4D,#7A3F22); }

.card-title { font-weight: 700; font-size: 1.05rem; color: var(--text); }
.card-step  { font-size: 0.7rem; letter-spacing: 2px; text-transform: uppercase; color: var(--muted); margin-top: 1px; }

/* Output text box */
.output-box {
    background: #FFFEF9;
    border: 1px solid #DDD0B8;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    font-size: 0.88rem;
    color: var(--text);
    line-height: 1.75;
    max-height: 320px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-word;
}
.output-box::-webkit-scrollbar { width: 5px; }
.output-box::-webkit-scrollbar-thumb { background: var(--wheat); border-radius: 4px; }

/* Score badge */
.score-badge {
    display: inline-block;
    background: linear-gradient(135deg, #E97451, #DAA06D);
    color: #fff;
    font-weight: 700;
    font-size: 0.85rem;
    padding: 3px 14px;
    border-radius: 20px;
    margin-bottom: 0.6rem;
    box-shadow: 0 3px 10px rgba(233,116,81,0.35);
}

/* Input area */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #FFFEF9 !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--burnt) !important;
    box-shadow: 0 0 0 3px rgba(233,116,81,0.15) !important;
}

/* Primary button */
.stButton > button {
    background: linear-gradient(135deg, #E97451 0%, #C0522E 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.6rem 1.4rem !important;
    box-shadow: 0 4px 16px rgba(233,116,81,0.35) !important;
    transition: all 0.2s !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 22px rgba(233,116,81,0.45) !important;
}

/* Progress steps */
.step-pill {
    display: inline-flex; align-items: center; gap: 0.4rem;
    background: var(--card-bg);
    border: 1.5px solid var(--border);
    border-radius: 50px;
    padding: 0.35rem 0.9rem;
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--subtext);
    margin: 0.25rem;
}
.step-pill.active { background: linear-gradient(135deg,#E97451,#DAA06D); color:#fff; border-color: transparent; }
.step-pill.done   { background: #81613E; color: #F5F5DC; border-color: transparent; }

/* History item */
.hist-item {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.7rem;
    cursor: pointer;
    transition: all 0.18s;
}
.hist-item:hover { border-color: var(--burnt); background: #FFF8F2; }
.hist-topic { font-weight: 600; font-size: 0.88rem; color: var(--text); }
.hist-meta  { font-size: 0.73rem; color: var(--muted); margin-top: 2px; }

/* Page header */
.page-header {
    background: linear-gradient(135deg, #1A1108 0%, #3D2A14 100%);
    border-radius: 16px;
    padding: 2rem 2.4rem;
    margin-bottom: 1.8rem;
    border: 1px solid #5A3A20;
    position: relative;
    overflow: hidden;
}
.page-header::before {
    content: '';
    position: absolute; top: -40px; right: -40px;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(233,116,81,0.25) 0%, transparent 70%);
    border-radius: 50%;
}
.page-header h1 {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    color: var(--cream);
    margin: 0 0 0.3rem;
}
.page-header p { color: #C9B49A; margin: 0; font-size: 0.92rem; }

/* Section label */
.section-label {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.6rem;
}

/* Divider */
hr.styled { border: none; border-top: 1.5px solid var(--border); margin: 1.5rem 0; }

/* Alert override */
.stAlert { border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# ─── Session State ───────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []          # list of dicts
if "current" not in st.session_state:
    st.session_state.current = None        # currently displayed result
if "running" not in st.session_state:
    st.session_state.running = False

# ─── Sidebar ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="brand-title">🔬 ResearchAI</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">Multi-Agent Pipeline</div>', unsafe_allow_html=True)

    st.markdown("### 🕰️ Research History")

    if not st.session_state.history:
        st.markdown('<p style="font-size:0.8rem;color:#8a7060;text-align:center;padding:1rem 0;">No research yet.<br>Run your first query!</p>', unsafe_allow_html=True)
    else:
        for i, item in enumerate(reversed(st.session_state.history)):
            idx = len(st.session_state.history) - 1 - i
            ts  = item.get("timestamp", "")
            sc  = item.get("score", "—")
            topic_short = item["topic"][:32] + ("…" if len(item["topic"]) > 32 else "")
            clicked = st.button(
                f"📄 {topic_short}\n{ts}  ·  Score {sc}",
                key=f"hist_{idx}",
                use_container_width=True,
            )
            if clicked:
                st.session_state.current = item

    st.markdown('<hr style="border:1px solid #3D2A14;margin:1.2rem 0;">', unsafe_allow_html=True)
    if st.session_state.history:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.history = []
            st.session_state.current = None
            st.rerun()

    st.markdown("""
    <div style='margin-top:2rem;font-size:0.73rem;color:#7A5C46;line-height:1.7;'>
    <b style='color:#DAA06D;'>Pipeline Agents</b><br>
    🌐 <b>Search Agent</b> — Tavily web search<br>
    📖 <b>Reader Agent</b> — URL scraper<br>
    ✍️ <b>Writer Chain</b> — Report drafting<br>
    🧐 <b>Critic Chain</b> — Quality scoring
    </div>
    """, unsafe_allow_html=True)

# ─── Main ─────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <h1>🔬 ResearchAI Pipeline</h1>
    <p>Enter a topic — four AI agents collaborate to search, scrape, write, and critique a full research report.</p>
</div>
""", unsafe_allow_html=True)

# ── Input Row ──
col_in, col_btn = st.columns([4, 1], gap="medium")
with col_in:
    topic = st.text_input(
        "",
        placeholder="e.g.  Quantum computing breakthroughs in 2025",
        label_visibility="collapsed",
    )
with col_btn:
    st.markdown("<div style='margin-top:0.25rem;'>", unsafe_allow_html=True)
    run_btn = st.button("▶ Run Research")
    st.markdown("</div>", unsafe_allow_html=True)

# ── Pipeline progress tracker ──
def show_progress(active_step: int):
    steps = [
        ("🌐", "Searching"),
        ("📖", "Scraping"),
        ("✍️", "Writing"),
        ("🧐", "Critiquing"),
    ]
    pills = ""
    for i, (icon, label) in enumerate(steps):
        cls = "done" if i < active_step else ("active" if i == active_step else "step-pill")
        if i < active_step:
            cls = "step-pill done"
        elif i == active_step:
            cls = "step-pill active"
        else:
            cls = "step-pill"
        pills += f'<span class="{cls}">{icon} {label}</span>'
    st.markdown(f'<div style="margin:0.8rem 0 1.4rem;">{pills}</div>', unsafe_allow_html=True)

# ── Result display helper ──
def display_result(item: dict):
    col1, col2 = st.columns(2, gap="large")

    with col1:
        # Search results card
        st.markdown(f"""
        <div class="res-card">
            <div class="card-header">
                <div class="card-icon-wrap icon-search">🌐</div>
                <div><div class="card-title">Web Search Results</div><div class="card-step">Step 01 — Search Agent</div></div>
            </div>
            <div class="output-box">{item.get('search_results','No data')}</div>
        </div>
        """, unsafe_allow_html=True)

        # Writer card
        st.markdown(f"""
        <div class="res-card">
            <div class="card-header">
                <div class="card-icon-wrap icon-writer">✍️</div>
                <div><div class="card-title">Research Report</div><div class="card-step">Step 03 — Writer Chain</div></div>
            </div>
            <div class="output-box">{item.get('report','No data')}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Scraper card
        st.markdown(f"""
        <div class="res-card">
            <div class="card-header">
                <div class="card-icon-wrap icon-reader">📖</div>
                <div><div class="card-title">Scraped Content</div><div class="card-step">Step 02 — Reader Agent</div></div>
            </div>
            <div class="output-box">{item.get('scraped_content','No data')}</div>
        </div>
        """, unsafe_allow_html=True)

        # Critic card
        score_html = ""
        feedback = item.get('feedback', '')
        if feedback and "Score:" in feedback:
            score_line = [l for l in feedback.split('\n') if "Score:" in l]
            if score_line:
                score_html = f'<div class="score-badge">⭐ {score_line[0].strip()}</div><br>'

        st.markdown(f"""
        <div class="res-card">
            <div class="card-header">
                <div class="card-icon-wrap icon-critic">🧐</div>
                <div><div class="card-title">Critic Review</div><div class="card-step">Step 04 — Critic Chain</div></div>
            </div>
            {score_html}
            <div class="output-box">{feedback or 'No data'}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Run the pipeline ──
if run_btn and topic.strip():
    st.session_state.running = True
    st.session_state.current = None

    prog_placeholder = st.empty()
    status_placeholder = st.empty()

    try:
        try:
            from pipeline import run_research_pipeline
        except Exception as import_err:
            prog_placeholder.empty()
            status_placeholder.empty()
            st.session_state.running = False
            st.error(f"❌ Import error — make sure `pipeline.py`, `agents.py`, and `tools.py` are in the **same folder** as `app.py`.\n\n**Details:** `{import_err}`")
            st.stop()

        with prog_placeholder.container():
            show_progress(0)
        with status_placeholder.container():
            st.info("🌐 **Search Agent** is scanning the web…")
        time.sleep(0.4)

        # Monkey-patch to capture step progress via a wrapper
        # We'll run the full pipeline; progress updates are cosmetic
        with st.spinner("Running multi-agent research pipeline…"):
            result = run_research_pipeline(topic.strip())

        # Show progress completing
        for step in range(1, 5):
            with prog_placeholder.container():
                show_progress(step if step < 4 else 5)
            time.sleep(0.25)

        prog_placeholder.empty()
        status_placeholder.empty()

        # Extract score for history
        score_str = "—"
        fb = result.get("feedback", "")
        if fb:
            for line in fb.split('\n'):
                if "Score:" in line:
                    score_str = line.replace("Score:", "").strip()
                    break

        entry = {
            "topic":           topic.strip(),
            "timestamp":       datetime.now().strftime("%d %b %Y, %H:%M"),
            "score":           score_str,
            "search_results":  result.get("search_results", ""),
            "scraped_content": result.get("scraped_content", ""),
            "report":          result.get("report", ""),
            "feedback":        result.get("feedback", ""),
        }
        st.session_state.history.append(entry)
        st.session_state.current = entry
        st.session_state.running = False
        st.rerun()

    except Exception as e:
        prog_placeholder.empty()
        status_placeholder.empty()
        st.session_state.running = False
        st.error(f"❌ Pipeline error: `{type(e).__name__}: {e}`")

elif run_btn and not topic.strip():
    st.warning("Please enter a research topic first.")

# ── Display current result ──
if st.session_state.current:
    item = st.session_state.current
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:0.8rem;margin-bottom:1rem;">
        <div style="flex:1;">
            <div class="section-label">Research Output</div>
            <div style="font-family:'Playfair Display',serif;font-size:1.4rem;color:#1A1108;font-weight:700;">{item['topic']}</div>
            <div style="font-size:0.78rem;color:#7A5C46;margin-top:2px;">🕰️ {item.get('timestamp','')} &nbsp;·&nbsp; ⭐ Score {item.get('score','—')}</div>
        </div>
    </div>
    <hr class="styled">
    """, unsafe_allow_html=True)

    display_result(item)

else:
    # Empty state
    st.markdown("""
    <div style="text-align:center;padding:4rem 2rem;opacity:0.7;">
        <div style="font-size:4rem;margin-bottom:1rem;filter:drop-shadow(0 4px 8px rgba(0,0,0,0.15));">🔬</div>
        <div style="font-family:'Playfair Display',serif;font-size:1.4rem;color:#4A3728;margin-bottom:0.5rem;">Ready to Research</div>
        <div style="color:#7A5C46;font-size:0.9rem;max-width:380px;margin:0 auto;line-height:1.6;">
            Enter any topic above and the four-agent pipeline will search, scrape, write, and critique a full report for you.
        </div>
    </div>
    """, unsafe_allow_html=True)