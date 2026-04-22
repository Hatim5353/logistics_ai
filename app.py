"""
app.py  —  Streamlit UI for the Autonomous Logistics Researcher Agent
Run with:  streamlit run app.py
"""

import os
import re
import glob
import time
import streamlit as st

from datetime import datetime
from dotenv import load_dotenv

# Disable ChromaDB telemetry as it can cause indefinite hanging on Windows loops
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY_IMPL_OOTB"] = "false"

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LogisticsAI · Intelligence Agent",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

/* ── Root ── */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background-color: #f0fdf9;
    color: #134e4a;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer { visibility: hidden; }
header { background: transparent !important; }
.block-container {
    padding: 2.5rem 3rem;
    max-width: 1180px;
    background: transparent;
}

/* ══════════════════════════════════════
   SIDEBAR
══════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #134e4a 0%, #0f3d39 100%) !important;
    border-right: none;
    min-width: 260px !important;
}
[data-testid="stSidebar"] > div { padding: 1.5rem 1rem; }
[data-testid="stSidebar"] * { color: #ccfbf1 !important; }


[data-testid="stSidebar"] .stRadio > label {
    display: none;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
    gap: 6px;
    display: flex;
    flex-direction: column;
}
[data-testid="stSidebar"] .stRadio label {
    display: flex !important;
    align-items: center;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    color: #99f6e4 !important;
    padding: 0.65rem 1rem !important;
    border-radius: 10px !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    border: 1px solid transparent !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(153, 246, 228, 0.12) !important;
    color: #ffffff !important;
    border-color: rgba(153, 246, 228, 0.2) !important;
}
[data-testid="stSidebar"] [data-baseweb="radio"] input:checked ~ div {
    background: rgba(13, 148, 136, 0.4) !important;
}

/* ══════════════════════════════════════
   HERO BANNER
══════════════════════════════════════ */
.hero-wrap {
    background: linear-gradient(135deg, #0d9488 0%, #0f766e 50%, #115e59 100%);
    border-radius: 20px;
    padding: 2.5rem 2.75rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-wrap::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 220px; height: 220px;
    background: rgba(255,255,255,0.05);
    border-radius: 50%;
}
.hero-wrap::after {
    content: '';
    position: absolute;
    bottom: -60px; left: 30%;
    width: 300px; height: 300px;
    background: rgba(255,255,255,0.04);
    border-radius: 50%;
}
.hero-eyebrow {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #5eead4;
    margin-bottom: 0.5rem;
}
.hero-title {
    font-size: 2.1rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.2;
    margin-bottom: 0.5rem;
    letter-spacing: -0.03em;
}
.hero-sub {
    font-size: 0.925rem;
    color: #99f6e4;
    font-weight: 400;
    margin-bottom: 0;
}

/* ══════════════════════════════════════
   STAT CARDS
══════════════════════════════════════ */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}
.stat-card {
    background: #ffffff;
    border: 1px solid #d1fae5;
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    box-shadow: 0 2px 8px rgba(13, 148, 136, 0.06);
    transition: all 0.25s ease;
}
.stat-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(13, 148, 136, 0.12);
    border-color: #6ee7b7;
}
.stat-icon { font-size: 1.5rem; margin-bottom: 0.5rem; }
.stat-label {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #6b7280;
    margin-bottom: 0.35rem;
}
.stat-value {
    font-size: 1.65rem;
    font-weight: 800;
    color: #134e4a;
    line-height: 1;
}
.stat-sub {
    font-size: 0.75rem;
    color: #6b7280;
    margin-top: 0.2rem;
}

/* ══════════════════════════════════════
   SECTION HEADER
══════════════════════════════════════ */
.section-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: #134e4a;
    margin-bottom: 1.25rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 2px;
    background: linear-gradient(to right, #d1fae5, transparent);
    border-radius: 2px;
    margin-left: 0.75rem;
}

/* ══════════════════════════════════════
   QUERY INPUT + BUTTONS
══════════════════════════════════════ */
.stTextArea textarea {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.95rem !important;
    border: 2px solid #d1fae5 !important;
    border-radius: 12px !important;
    background: #ffffff !important;
    color: #134e4a !important;
    padding: 1rem 1.1rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 6px rgba(13, 148, 136, 0.05) !important;
    line-height: 1.6 !important;
}
.stTextArea textarea:focus {
    border-color: #0d9488 !important;
    box-shadow: 0 0 0 4px rgba(13, 148, 136, 0.1) !important;
    outline: none !important;
}

/* ── All buttons base ── */
.stButton > button {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    background: #ffffff !important;
    color: #0d9488 !important;
    border: 1.5px solid #d1fae5 !important;
    border-radius: 10px !important;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: #f0fdf9 !important;
    border-color: #6ee7b7 !important;
}

/* ── Primary button — Streamlit renders type=primary as data-testid or p tag inside ── */
[data-testid="baseButton-primary"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.92rem !important;
    font-weight: 700 !important;
    background: linear-gradient(135deg, #0d9488 0%, #0f766e 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.6rem !important;
    box-shadow: 0 4px 14px rgba(13, 148, 136, 0.35) !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.02em !important;
}
[data-testid="baseButton-primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 22px rgba(13, 148, 136, 0.45) !important;
    background: linear-gradient(135deg, #0f766e 0%, #115e59 100%) !important;
    color: #ffffff !important;
}
[data-testid="baseButton-primary"]:active {
    transform: translateY(0px) !important;
}

/* ── Example query chips ── */
.example-chip {
    display: inline-block;
    background: #f0fdf9;
    border: 1.5px solid #99f6e4;
    border-radius: 20px;
    padding: 0.35rem 0.85rem;
    font-size: 0.8rem;
    font-weight: 500;
    color: #0f766e;
    cursor: pointer;
    transition: all 0.2s ease;
    margin: 0.25rem;
}
.example-chip:hover {
    background: #0d9488;
    color: white;
    border-color: #0d9488;
}

/* ══════════════════════════════════════
   LOG / OUTPUT BOX
══════════════════════════════════════ */
.log-box {
    background: #022c22;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    font-family: 'Courier New', Courier, monospace;
    font-size: 0.82rem;
    color: #6ee7b7;
    line-height: 1.85;
    white-space: pre-wrap;
    max-height: 340px;
    overflow-y: auto;
    border: 1px solid #064e3b;
    box-shadow: inset 0 2px 6px rgba(0,0,0,0.3);
}
.log-pending { color: #6ee7b7; }
.log-done    { color: #34d399; }
.log-err     { color: #f87171; }

/* ══════════════════════════════════════
   BADGES / CHIPS
══════════════════════════════════════ */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    padding: 0.22rem 0.7rem;
    border-radius: 20px;
}
.badge-running { background: #fef3c7; color: #92400e; border: 1px solid #fcd34d; }
.badge-done    { background: #d1fae5; color: #065f46; border: 1px solid #6ee7b7; }
.badge-kb      { background: #ede9fe; color: #4c1d95; border: 1px solid #c4b5fd; }
.badge-error   { background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; }

/* ══════════════════════════════════════
   REPORT CARDS
══════════════════════════════════════ */
.report-card {
    background: #ffffff;
    border: 1px solid #d1fae5;
    border-left: 4px solid #0d9488;
    border-radius: 12px;
    padding: 1rem 1.4rem;
    margin-bottom: 0.75rem;
    box-shadow: 0 2px 8px rgba(13, 148, 136, 0.05);
    transition: all 0.2s ease;
}
.report-card:hover {
    box-shadow: 0 6px 20px rgba(13, 148, 136, 0.12);
    border-left-color: #0f766e;
    transform: translateX(2px);
}
.report-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: #134e4a;
    margin-bottom: 0.2rem;
}
.report-meta {
    font-size: 0.75rem;
    color: #9ca3af;
    display: flex;
    gap: 0.5rem;
    align-items: center;
}

/* ══════════════════════════════════════
   ANSWER / OUTPUT CARD
══════════════════════════════════════ */
.answer-box {
    background: #ffffff;
    border: 1px solid #d1fae5;
    border-radius: 14px;
    padding: 1.5rem 1.75rem;
    font-size: 0.95rem;
    color: #1f2937;
    line-height: 1.75;
    box-shadow: 0 4px 16px rgba(13, 148, 136, 0.07);
}

/* ══════════════════════════════════════
   ALERT BOXES
══════════════════════════════════════ */
.alert-info {
    background: #ecfdf5;
    border: 1px solid #a7f3d0;
    border-radius: 10px;
    padding: 0.85rem 1.2rem;
    font-size: 0.875rem;
    color: #065f46;
    margin-bottom: 1rem;
}
.alert-warn {
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-radius: 10px;
    padding: 0.85rem 1.2rem;
    font-size: 0.875rem;
    color: #78350f;
    margin-bottom: 1rem;
}

/* ══════════════════════════════════════
   SIDEBAR BRAND
══════════════════════════════════════ */
.sidebar-brand {
    padding: 0.5rem 0.5rem 1.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 1.5rem;
}
.sidebar-logo {
    font-size: 1.35rem;
    font-weight: 800;
    color: #ffffff !important;
    letter-spacing: -0.02em;
}
.sidebar-tagline {
    font-size: 0.7rem;
    font-weight: 600;
    color: #5eead4 !important;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 2px;
}
.sidebar-stat-row {
    background: rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 0.75rem 1rem;
    margin-top: 1.5rem;
    border: 1px solid rgba(255,255,255,0.08);
}
.sidebar-stat-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.3rem 0;
    font-size: 0.775rem;
    font-weight: 500;
    color: #99f6e4 !important;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}
.sidebar-stat-item:last-child { border-bottom: none; }
.sidebar-stat-val {
    font-weight: 700;
    color: #ffffff !important;
}

/* ══════════════════════════════════════
   TEXT INPUT
══════════════════════════════════════ */
.stTextInput input {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    border: 2px solid #d1fae5 !important;
    border-radius: 10px !important;
    background: #ffffff !important;
    color: #134e4a !important;
    padding: 0.6rem 1rem !important;
    font-size: 0.9rem !important;
}
.stTextInput input:focus {
    border-color: #0d9488 !important;
    box-shadow: 0 0 0 4px rgba(13, 148, 136, 0.1) !important;
}

/* ══════════════════════════════════════
   SLIDER
══════════════════════════════════════ */
.stSlider > div > div > div { background: #0d9488 !important; }

/* ══════════════════════════════════════
   EXPANDER
══════════════════════════════════════ */
.streamlit-expanderHeader {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    color: #0f766e !important;
    background: #f0fdf9 !important;
    border: 1px solid #d1fae5 !important;
    border-radius: 10px !important;
}
.streamlit-expanderContent {
    border: 1px solid #d1fae5 !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
    background: #ffffff !important;
}

/* thin divider */
.divider {
    border: none;
    border-top: 1.5px solid #d1fae5;
    margin: 1.75rem 0;
}

/* ══════════════════════════════════════
   CHECKBOX
══════════════════════════════════════ */
.stCheckbox label {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    color: #0f766e !important;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ──────────────────────────────────────────────────────────────────

def clean_markdown(text: str) -> str:
    text = text.strip()
    if text.startswith("```markdown"):
        text = text[11:]
    elif text.startswith("```md"):
        text = text[5:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()

def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()[:60]).strip("-")

def get_reports() -> list[dict]:
    files = sorted(glob.glob("knowledge_repo/*.md"), reverse=True)
    reports = []
    for f in files:
        name  = os.path.basename(f)
        size  = os.path.getsize(f)
        mtime = datetime.fromtimestamp(os.path.getmtime(f)).strftime("%Y-%m-%d %H:%M")
        reports.append({"name": name, "path": f, "size": size, "modified": mtime})
    return reports

def knowledge_base_exists() -> bool:
    chroma_dir = "./chroma_db"
    return os.path.isdir(chroma_dir) and bool(os.listdir(chroma_dir))

# Cache ChromaDB connection and embedding model to optimize performance
@st.cache_data(ttl=60)
def count_chunks() -> int:
    try:
        from langchain_chroma import Chroma
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        emb = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
        )
        db = Chroma(persist_directory="./chroma_db", embedding_function=emb)
        collection_count = db._collection.count()
        db = None # release the database lock
        return collection_count
    except Exception:
        return 0


# ═══════════════════════════════════════════════════════════════════════════
# AUTO-INDEX: If reports exist but ChromaDB is empty/broken, index once per session
# ═══════════════════════════════════════════════════════════════════════════
if "auto_indexed" not in st.session_state:
    st.session_state["auto_indexed"] = False

_reports_on_disk = get_reports()
_kb_chunk_count  = count_chunks() if knowledge_base_exists() else 0
_needs_indexing  = _reports_on_disk and _kb_chunk_count == 0 and not st.session_state["auto_indexed"]

if _needs_indexing:
    with st.spinner("📚 Indexing existing reports into knowledge base for the first time..."):
        try:
            from src.rag.indexer import index_knowledge_repo
            index_knowledge_repo()
            count_chunks.clear()
            st.session_state["auto_indexed"] = True
        except Exception as _e:
            st.warning(f"Auto-index failed (you can retry in Settings): {_e}")
            st.session_state["auto_indexed"] = True  # don't retry on every reload
    st.rerun()
else:
    st.session_state["auto_indexed"] = True

# ═══════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════
with st.sidebar:
    reports = get_reports()
    kb_ok   = knowledge_base_exists()
    chunks  = count_chunks() if kb_ok else 0
    serper_active = bool(os.getenv("SERPER_API_KEY"))
    gemini_ok     = bool(os.getenv("GOOGLE_API_KEY"))

    st.markdown(f"""
    <div class='sidebar-brand'>
        <div class='sidebar-logo'>🌊 LogisticsAI</div>
        <div class='sidebar-tagline'>Intelligence Agent</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["🔬 Live Research", "💬 Query Knowledge Base", "📚 Report Library", "⚙️ Settings"],
        label_visibility="collapsed",
    )

    st.markdown(f"""
    <div class='sidebar-stat-row'>
        <div class='sidebar-stat-item'>
            <span>📄 Reports</span>
            <span class='sidebar-stat-val'>{len(reports)}</span>
        </div>
        <div class='sidebar-stat-item'>
            <span>🧠 KB Chunks</span>
            <span class='sidebar-stat-val'>{chunks}</span>
        </div>
        <div class='sidebar-stat-item'>
            <span>🔌 KB Status</span>
            <span class='sidebar-stat-val' style='color:{"#34d399" if kb_ok else "#f87171"} !important'>
                {"Ready" if kb_ok else "Empty"}
            </span>
        </div>
        <div class='sidebar-stat-item'>
            <span>🔍 Search</span>
            <span class='sidebar-stat-val' style='color:{"#34d399" if serper_active else "#fbbf24"} !important'>
                {"Serper.dev" if serper_active else "DuckDuckGo"}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# HERO BANNER (shown on all pages)
# ═══════════════════════════════════════════════════════════════════════════
page_info = {
    "🔬 Live Research":        ("🔬 Live Research",          "Run AI agents to search the web and generate a structured logistics intelligence report."),
    "💬 Query Knowledge Base": ("💬 Query Knowledge Base",   "Instantly answer questions from your saved research reports — no web calls needed."),
    "📚 Report Library":       ("📚 Report Library",         "Browse, search, and download all previously generated research reports."),
    "⚙️ Settings":             ("⚙️ Settings & Tools",       "Manage your API keys, knowledge base index, and project configuration."),
}
page_title, page_desc = page_info.get(page, ("LogisticsAI", ""))

st.markdown(f"""
<div class='hero-wrap'>
    <div class='hero-eyebrow'>Autonomous Research · Powered by Gemini + CrewAI</div>
    <div class='hero-title'>{page_title}</div>
    <div class='hero-sub'>{page_desc}</div>
</div>
""", unsafe_allow_html=True)

# ── Stat bar ─────────────────────────────────────────────────────────────────
total_size_kb = sum(r["size"] for r in reports) // 1024

st.markdown(f"""
<div class='stat-grid'>
    <div class='stat-card'>
        <div class='stat-icon'>📄</div>
        <div class='stat-label'>Reports Generated</div>
        <div class='stat-value'>{len(reports)}</div>
        <div class='stat-sub'>in knowledge_repo/</div>
    </div>
    <div class='stat-card'>
        <div class='stat-icon'>🧠</div>
        <div class='stat-label'>KB Chunks Indexed</div>
        <div class='stat-value'>{chunks}</div>
        <div class='stat-sub'>vector embeddings</div>
    </div>
    <div class='stat-card'>
        <div class='stat-icon'>💾</div>
        <div class='stat-label'>Repo Size</div>
        <div class='stat-value'>{total_size_kb}<span style='font-size:1rem;color:#6b7280'> KB</span></div>
        <div class='stat-sub'>total stored data</div>
    </div>
    <div class='stat-card'>
        <div class='stat-icon'>{"🟢" if serper_active else "🟡"}</div>
        <div class='stat-label'>Search Engine</div>
        <div class='stat-value' style='font-size:1rem;margin-top:4px'>{"Serper.dev" if serper_active else "DuckDuckGo"}</div>
        <div class='stat-sub'>{"premium search" if serper_active else "free fallback"}</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 1 — Live Research
# ═══════════════════════════════════════════════════════════════════════════
if "Live Research" in page:

    # ── Example queries ──────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>💡 Quick Start with an Example Query</div>", unsafe_allow_html=True)
    examples = [
        "Analyze Red Sea shipping disruptions and impact on Europe-Asia freight rates",
        "Current Panama Canal drought impact on transit times",
        "Global container port congestion levels in 2025",
        "Air freight vs ocean freight rate trends for Asia-US routes",
    ]
    cols = st.columns(2)
    for i, ex in enumerate(examples):
        with cols[i % 2]:
            label = ex[:58] + ("..." if len(ex) > 58 else "")
            if st.button(f"↗ {label}", key=f"ex_{i}"):
                st.session_state["query_input"] = ex

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # ── Query input ──────────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>✏️ Your Research Query</div>", unsafe_allow_html=True)
    query = st.text_area(
        "Research Query",
        value=st.session_state.get("query_input", ""),
        height=110,
        placeholder="e.g. Analyze the impact of current Red Sea disruptions on European container shipping rates and expected rate changes over Q3 2025...",
        label_visibility="collapsed",
    )

    col1, col2, col3 = st.columns([1.2, 1.8, 4])
    with col1:
        run_btn = st.button("🚀 Run Agent", key="run_agent_btn", type="primary")
    with col2:
        force_fresh = st.checkbox("⚡ Force Fresh Research", help="Bypass local knowledge base and run new live web research.")

    if run_btn:
        if not query.strip():
            st.markdown("<div class='alert-warn'>⚠️ Please enter a research query before running.</div>", unsafe_allow_html=True)
        else:
            proceed_with_agent = True

            # ── 1. Auto-check Knowledge Base ─────────────────────────────────
            if not force_fresh and kb_ok:
                with st.spinner("🔍 Checking local knowledge base for existing insights..."):
                    try:
                        from src.rag.retriever import query_local
                        kb_check = query_local(query)

                        if "Insufficient data" not in kb_check:
                            st.markdown("<span class='badge badge-kb'>📖 From Knowledge Base</span>", unsafe_allow_html=True)
                            st.success("✨ Found relevant information in your saved reports! Showing results below:")
                            st.markdown(f"<div class='answer-box'>{kb_check}</div>", unsafe_allow_html=True)
                            st.markdown("""
                            <div class='alert-info'>
                                💡 <strong>Tip:</strong> This answer came from your local knowledge base — no API calls were made.
                                Check <em>"Force Fresh Research"</em> if you need the absolute latest web data.
                            </div>
                            """, unsafe_allow_html=True)
                            proceed_with_agent = False
                        else:
                            st.markdown("<div class='alert-info'>🔎 No sufficient data in local reports. Starting live research...</div>", unsafe_allow_html=True)
                    except Exception as e:
                        if "429" in str(e) or "quota" in str(e).lower() or "RESOURCE_EXHAUSTED" in str(e):
                            st.error(f"🚨 **Gemini API Rate Limit Exceeded!** Please wait a minute before querying again.\n\nError details: {e}")
                            st.stop()
                        else:
                            st.error(f"⚠️ Knowledge Base error: {e}")
                            st.stop()

            # ── 2. Live Agent Research ────────────────────────────────────────
            if proceed_with_agent:
                timestamp   = datetime.now().strftime("%Y%m%d_%H%M")
                output_file = f"{timestamp}_{slugify(query)}.md"

                st.markdown(f"""
                <div style='margin:1rem 0 0.75rem;display:flex;align-items:center;gap:0.5rem;'>
                    <span class='badge badge-running'>⏳ Running</span>
                    <span style='font-size:0.8rem;color:#92400e;font-weight:500;'>
                        → knowledge_repo/{output_file}
                    </span>
                </div>
                """, unsafe_allow_html=True)

                log_placeholder    = st.empty()
                result_placeholder = st.empty()

                log_lines = [
                    "[ ANALYST ] Initialising Logistics Analyst agent...",
                    "[ ANALYST ] Connecting to search tools...",
                    "[ ANALYST ] Running web search pass 1...",
                    "[ ANALYST ] Extracting data points and sources...",
                    "[ ANALYST ] Running web search pass 2 (refinement)...",
                    "[ ANALYST ] Verifying cross-references...",
                    "[ WRITER  ] Technical Writer receiving research payload...",
                    "[ WRITER  ] Synthesising into structured Markdown report...",
                    "[ WRITER  ] Applying schema: Summary → Findings → Data → Sources...",
                    f"[ SYSTEM  ] Saving report → knowledge_repo/{output_file}",
                ]

                shown = []
                for line in log_lines:
                    shown.append(line)
                    log_placeholder.markdown(
                        "<div class='log-box'>" +
                        "\n".join(f"<span class='log-pending'>{l}</span>" for l in shown) +
                        "</div>",
                        unsafe_allow_html=True,
                    )
                    time.sleep(0.35)

                try:
                    from src.agents.logistics_crew import run_research
                    result = run_research(query, output_file)

                    try:
                        from src.rag.indexer import index_knowledge_repo
                        index_knowledge_repo()
                        shown.append("[ INDEXER ] New report indexed into ChromaDB ✓")
                        count_chunks.clear()
                    except Exception:
                        pass

                    shown.append("[ DONE    ] Research complete ✓")
                    log_placeholder.markdown(
                        "<div class='log-box'>" +
                        "\n".join(
                            f"<span class='{'log-done' if '✓' in l else 'log-pending'}'>{l}</span>"
                            for l in shown
                        ) + "</div>",
                        unsafe_allow_html=True,
                    )

                    st.markdown(f"""
                    <div style='margin:1rem 0;display:flex;align-items:center;gap:0.5rem;'>
                        <span class='badge badge-done'>✓ Complete</span>
                        <span style='font-size:0.85rem;color:#065f46;font-weight:600;'>
                            Report saved to knowledge_repo/{output_file}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("<div class='section-title'>📋 Report Output</div>", unsafe_allow_html=True)
                    with st.container():
                        st.markdown(f"<div class='answer-box'>{clean_markdown(result)}</div>", unsafe_allow_html=True)

                    st.download_button(
                        label="⬇️ Download Report",
                        data=result,
                        file_name=output_file,
                        mime="text/markdown",
                    )

                except Exception as e:
                    shown.append(f"[ ERROR ] {e}")
                    log_placeholder.markdown(
                        "<div class='log-box'>" +
                        "\n".join(
                            f"<span class='{'log-err' if 'ERROR' in l else 'log-pending'}'>{l}</span>"
                            for l in shown
                        ) + "</div>",
                        unsafe_allow_html=True,
                    )
                    st.error(f"❌ Agent run failed: {e}")


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 2 — Query Knowledge Base
# ═══════════════════════════════════════════════════════════════════════════
elif "Query Knowledge Base" in page:

    if not kb_ok:
        st.markdown("""
        <div class='alert-warn'>
            <strong>⚠️ Knowledge base is empty.</strong><br>
            Run at least one <em>Live Research</em> session first. Once a report is saved,
            it will be indexed here so you can query it instantly — no web calls, no API cost.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='alert-info'>
            🧠 <strong>{chunks} chunks</strong> indexed from <strong>{len(reports)} report{"s" if len(reports) != 1 else ""}</strong>
            — ready for instant semantic retrieval.
        </div>
        """, unsafe_allow_html=True)

        col_k, _ = st.columns([1, 3])
        with col_k:
            k = st.slider("Chunks to retrieve (k)", min_value=2, max_value=10, value=4,
                          help="More chunks = broader context but slightly slower answer.")

        st.markdown("<div class='section-title'>💬 Ask a Question</div>", unsafe_allow_html=True)
        question = st.text_area(
            "Question",
            height=100,
            placeholder="e.g. What were the main freight rate findings across all my reports?",
            label_visibility="collapsed",
        )

        if st.button("🔍 Search Knowledge Base", type="primary"):
            if not question.strip():
                st.markdown("<div class='alert-warn'>Please enter a question.</div>", unsafe_allow_html=True)
            else:
                with st.spinner("🧠 Retrieving from local knowledge base..."):
                    try:
                        from src.rag.retriever import query_local
                        answer = query_local(question, k=k)

                        st.markdown("<div class='section-title'>📖 Answer</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='answer-box'>{clean_markdown(answer)}</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"❌ Query failed: {e}")


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 3 — Report Library
# ═══════════════════════════════════════════════════════════════════════════
elif "Report Library" in page:

    if not reports:
        st.markdown("""
        <div class='alert-info'>
            📭 No reports yet. Run a <em>Live Research</em> session to generate your first report.
        </div>
        """, unsafe_allow_html=True)
    else:
        search = st.text_input("🔎 Filter reports", placeholder="Search by filename or topic...",
                               label_visibility="collapsed")
        filtered = [r for r in reports if search.lower() in r["name"].lower()] if search else reports

        st.markdown(f"""
        <div style='font-size:0.82rem;font-weight:600;color:#6b7280;margin-bottom:1.25rem;'>
            Showing {len(filtered)} of {len(reports)} report{"s" if len(reports) != 1 else ""}
        </div>
        """, unsafe_allow_html=True)

        for r in filtered:
            size_kb = r["size"] // 1024 or 1
            slug    = r["name"].replace(".md", "").replace("_", " ")

            st.markdown(f"""
            <div class='report-card'>
                <div class='report-title'>📄 {slug}</div>
                <div class='report-meta'>
                    🕐 {r['modified']} &nbsp;·&nbsp; 💾 {size_kb} KB
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander(f"View — {r['name']}"):
                try:
                    with open(r["path"], "r", encoding="utf-8") as f:
                        content = f.read()
                    st.markdown(clean_markdown(content))
                    st.download_button(
                        label="⬇️ Download",
                        data=content,
                        file_name=r["name"],
                        mime="text/markdown",
                        key=f"dl_{r['name']}",
                    )
                except Exception as e:
                    st.error(f"Could not read file: {e}")


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 4 — Settings
# ═══════════════════════════════════════════════════════════════════════════
elif "Settings" in page:

    serper_ok = bool(os.getenv("SERPER_API_KEY"))

    # API Key Status
    st.markdown("<div class='section-title'>🔑 API Key Status</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-icon'>{"✅" if gemini_ok else "❌"}</div>
            <div class='stat-label'>Google Gemini API Key</div>
            <div class='stat-value' style='font-size:1.1rem;color:{"#065f46" if gemini_ok else "#991b1b"}'>
                {"● SET & ACTIVE" if gemini_ok else "● NOT SET"}
            </div>
            <div class='stat-sub'>Required for all AI operations</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-icon'>{"✅" if serper_ok else "🟡"}</div>
            <div class='stat-label'>Serper.dev Search API</div>
            <div class='stat-value' style='font-size:1.1rem;color:{"#065f46" if serper_ok else "#92400e"}'>
                {"● ACTIVE" if serper_ok else "● USING DUCKDUCKGO"}
            </div>
            <div class='stat-sub'>{"Premium Google Search" if serper_ok else "Free fallback search"}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # Knowledge Base Management
    st.markdown("<div class='section-title'>🗄️ Knowledge Base Management</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔄 Re-index Knowledge Repo", type="primary"):
            with st.spinner("Indexing all reports..."):
                try:
                    from src.rag.indexer import index_knowledge_repo
                    n = index_knowledge_repo()
                    count_chunks.clear()
                    st.success(f"✅ Indexed {n} chunks from {len(reports)} reports.")
                except Exception as e:
                    st.error(f"Indexing failed: {e}")

    with col2:
        if st.button("🗑️ Clear Knowledge Base"):
            import shutil
            if os.path.isdir("./chroma_db"):
                shutil.rmtree("./chroma_db")
                count_chunks.clear()
                st.success("🧹 ChromaDB cleared. Re-index to rebuild.")
            else:
                st.info("No knowledge base found.")

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # Project Info
    st.markdown("<div class='section-title'>ℹ️ Project Info</div>", unsafe_allow_html=True)
    info = {
        "Framework":   "CrewAI + LangChain",
        "LLM":         "Gemini 1.5 Flash",
        "Vector DB":   "ChromaDB (local)",
        "Embeddings":  "Google Embedding-001",
        "Reports Dir": "./knowledge_repo/",
        "Chroma Dir":  "./chroma_db/",
    }
    for label, val in info.items():
        st.markdown(f"""
        <div style='display:flex;align-items:center;padding:0.5rem 0;border-bottom:1px solid #d1fae5;'>
            <span style='font-size:0.78rem;font-weight:700;color:#6b7280;width:120px;letter-spacing:0.04em;text-transform:uppercase;'>{label}</span>
            <span style='font-size:0.9rem;font-weight:500;color:#134e4a;'>{val}</span>
        </div>
        """, unsafe_allow_html=True)
