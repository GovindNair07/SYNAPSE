import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Synapse · AI Research Intelligence",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@300;400;500&display=swap');

/* ─── Reset & base ─── */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    color: #e8e4dc;
}

.stApp {
    background: #0a0a0f;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(255,140,50,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(255,80,30,0.08) 0%, transparent 55%);
}

/* ─── Scrollbar ─── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,140,50,0.25); border-radius: 4px; }

/* ─── Hide default streamlit chrome ─── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 3.5rem 5rem; max-width: 1300px; }

/* ─── Top nav bar ─── */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.4rem 0 1.2rem;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    margin-bottom: 0;
}
.logo {
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.logo-hex {
    width: 30px;
    height: 30px;
    background: linear-gradient(135deg, #ff8c32, #ff5a1a);
    clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
    flex-shrink: 0;
}
.logo-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: #f0ebe0;
}
.logo-name span {
    background: linear-gradient(90deg, #ff8c32, #ff5a1a);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.nav-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: rgba(255,140,50,0.75);
    background: rgba(255,140,50,0.08);
    border: 1px solid rgba(255,140,50,0.18);
    padding: 0.3rem 0.8rem;
    border-radius: 100px;
}

/* ─── Hero ─── */
.hero {
    padding: 5rem 0 3.5rem;
    max-width: 780px;
}
.hero-kicker {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    font-weight: 400;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #ff8c32;
    margin-bottom: 1.4rem;
}
.hero-kicker::before {
    content: '';
    display: inline-block;
    width: 20px;
    height: 1px;
    background: #ff8c32;
}
.hero h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(2.6rem, 5.5vw, 4.4rem);
    font-weight: 700;
    line-height: 1.05;
    letter-spacing: -0.03em;
    color: #f0ebe0;
    margin: 0 0 1.4rem;
}
.hero h1 em {
    font-family: 'Instrument Serif', serif;
    font-style: italic;
    font-weight: 400;
    background: linear-gradient(135deg, #ff8c32 0%, #ff5a1a 60%, #ffb347 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-desc {
    font-size: 1.05rem;
    font-weight: 300;
    color: rgba(232,228,220,0.5);
    line-height: 1.75;
    max-width: 560px;
}

/* ─── Two-col layout ─── */
.main-grid {
    display: grid;
    grid-template-columns: 1fr 380px;
    gap: 2.5rem;
    align-items: start;
    margin-top: 0;
}

/* ─── Glass card base ─── */
.glass {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    backdrop-filter: blur(12px);
}

/* ─── Input section ─── */
.input-wrapper {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 2rem 2rem 1.5rem;
    margin-bottom: 1.2rem;
}

/* ─── Streamlit widget overrides ─── */
.stTextInput > div > div > input,
.stTextInput input,
input[type="text"],
input[type="search"],
input[type="email"],
input[type="url"] {
    background: #ffffff !important;
    border: 1px solid rgba(255,140,50,0.3) !important;
    border-radius: 12px !important;
    color: #1a1208 !important;
    caret-color: #ff8c32 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.8rem 1.1rem !important;
    transition: all 0.2s ease !important;
    -webkit-text-fill-color: #1a1208 !important;
}
.stTextInput > div > div > input::placeholder,
.stTextInput input::placeholder { color: rgba(30,20,10,0.38) !important; -webkit-text-fill-color: rgba(30,20,10,0.38) !important; }
.stTextInput > div > div > input:focus,
.stTextInput input:focus {
    border-color: rgba(255,140,50,0.55) !important;
    background: #ffffff !important;
    box-shadow: 0 0 0 3px rgba(255,140,50,0.12) !important;
    outline: none !important;
    -webkit-text-fill-color: #1a1208 !important;
}
.stTextInput > label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    color: rgba(255,140,50,0.75) !important;
    font-weight: 400 !important;
    margin-bottom: 0.5rem !important;
}

/* ─── Button ─── */
.stButton > button {
    background: linear-gradient(135deg, #ff8c32 0%, #ff5a1a 100%) !important;
    color: #0a0a0f !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 1.8rem !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    width: 100%;
    box-shadow: 0 4px 20px rgba(255,140,50,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(255,140,50,0.45) !important;
    opacity: 0.95 !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ─── Pipeline sidebar cards ─── */
.pipeline-header {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: rgba(232,228,220,0.35);
    margin-bottom: 1.2rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}

.step-card {
    position: relative;
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    padding: 1.1rem 1.2rem;
    margin-bottom: 0.6rem;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.06);
    background: rgba(255,255,255,0.02);
    transition: all 0.3s ease;
    overflow: hidden;
}
.step-card.active  { border-color: rgba(255,140,50,0.35); background: rgba(255,140,50,0.05); }
.step-card.done    { border-color: rgba(80,200,120,0.25); background: rgba(80,200,120,0.04); }

/* left accent bar */
.step-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    border-radius: 14px 0 0 14px;
    background: rgba(255,255,255,0.04);
    transition: background 0.3s;
}
.step-card.active::before { background: #ff8c32; }
.step-card.done::before   { background: #50c878; }

/* per-step icon colors (idle state) */
.step-icon {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    font-size: 1rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    transition: all 0.3s;
}
/* Search — amber/orange */
.step-icon.icon-search { background: rgba(255,140,50,0.12); border: 1px solid rgba(255,140,50,0.2); color: #ff8c32; }
/* Reader — sky blue */
.step-icon.icon-reader { background: rgba(56,189,248,0.1);  border: 1px solid rgba(56,189,248,0.18); color: #38bdf8; }
/* Writer — violet */
.step-icon.icon-writer { background: rgba(167,139,250,0.1); border: 1px solid rgba(167,139,250,0.18); color: #a78bfa; }
/* Critic — emerald */
.step-icon.icon-critic { background: rgba(80,200,120,0.1);  border: 1px solid rgba(80,200,120,0.18); color: #50c878; }

.step-card.active .step-icon { box-shadow: 0 0 0 0 rgba(255,140,50,0.4); animation: pulse-ring 1.8s ease-out infinite; }
.step-card.done .step-icon   { background: rgba(80,200,120,0.12) !important; border-color: rgba(80,200,120,0.22) !important; color: #50c878 !important; }

.step-body { flex: 1; min-width: 0; }
.step-title-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.25rem;
}
.step-name {
    font-size: 0.85rem;
    font-weight: 600;
    color: #e8e4dc;
    letter-spacing: -0.01em;
}
.step-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.15rem 0.5rem;
    border-radius: 100px;
}
.badge-wait { color: rgba(232,228,220,0.25); background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); }
.badge-run  { color: #ff8c32; background: rgba(255,140,50,0.1); border: 1px solid rgba(255,140,50,0.22); }
.badge-done { color: #50c878; background: rgba(80,200,120,0.1); border: 1px solid rgba(80,200,120,0.2); }

.step-desc {
    font-size: 0.76rem;
    color: rgba(232,228,220,0.42);
    line-height: 1.45;
    font-weight: 300;
}

/* ─── Example chips ─── */
.chips-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.8rem;
}
.chip {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.73rem;
    color: rgba(232,228,220,0.45);
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 8px;
    padding: 0.3rem 0.75rem;
    cursor: default;
    transition: all 0.15s;
}
.chip:hover {
    color: rgba(232,228,220,0.75);
    background: rgba(255,140,50,0.06);
    border-color: rgba(255,140,50,0.2);
}
.chips-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: rgba(232,228,220,0.22);
    align-self: center;
}

/* ─── Divider ─── */
.thin-rule {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,140,50,0.2), transparent);
    margin: 2.5rem 0;
}

/* ─── Results section ─── */
.results-heading {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: rgba(232,228,220,0.3);
    margin-bottom: 1.5rem;
}

/* ─── Raw output panels ─── */
.raw-panel {
    background: rgba(0,0,0,0.3);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
}
.raw-panel-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: rgba(255,140,50,0.55);
    margin-bottom: 0.9rem;
    padding-bottom: 0.7rem;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.raw-panel-content {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    line-height: 1.75;
    color: rgba(232,228,220,0.55);
    white-space: pre-wrap;
    word-break: break-word;
}

/* ─── Report panel ─── */
.report-wrap {
    background: rgba(255,140,50,0.03);
    border: 1px solid rgba(255,140,50,0.18);
    border-radius: 20px;
    padding: 2.2rem 2.5rem;
    margin-bottom: 1.2rem;
}
.report-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: rgba(255,140,50,0.7);
    margin-bottom: 1.4rem;
    padding-bottom: 0.9rem;
    border-bottom: 1px solid rgba(255,140,50,0.12);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ─── Critic panel ─── */
.critic-wrap {
    background: rgba(80,200,120,0.03);
    border: 1px solid rgba(80,200,120,0.15);
    border-radius: 20px;
    padding: 2.2rem 2.5rem;
    margin-bottom: 1.2rem;
}
.critic-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: rgba(80,200,120,0.7);
    margin-bottom: 1.4rem;
    padding-bottom: 0.9rem;
    border-bottom: 1px solid rgba(80,200,120,0.12);
}

/* ─── Streamlit expander overrides ─── */
details {
    background: rgba(0,0,0,0.2) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 12px !important;
    margin-bottom: 0.8rem !important;
}
details summary {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem !important;
    color: rgba(232,228,220,0.35) !important;
    letter-spacing: 0.12em !important;
    padding: 0.9rem 1.2rem !important;
}

/* ─── Download button ─── */
.stDownloadButton > button {
    background: transparent !important;
    color: rgba(255,140,50,0.75) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.1em !important;
    border: 1px solid rgba(255,140,50,0.22) !important;
    border-radius: 9px !important;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
    background: rgba(255,140,50,0.08) !important;
    border-color: rgba(255,140,50,0.45) !important;
    color: #ff8c32 !important;
}

/* ─── Spinner ─── */
.stSpinner > div { color: #ff8c32 !important; }

/* ─── Warning / info msgs ─── */
.stAlert { border-radius: 12px !important; }

/* ─── Footer ─── */
.footer {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    color: rgba(232,228,220,0.15);
    text-align: center;
    margin-top: 4rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}

/* ─── Markdown inside panels ─── */
.report-wrap p, .critic-wrap p,
.report-wrap li, .critic-wrap li,
.report-wrap span, .critic-wrap span,
.report-wrap div, .critic-wrap div {
    color: #d4cfc7 !important;
    line-height: 1.85 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.97rem !important;
}
.report-wrap h1, .report-wrap h2, .report-wrap h3,
.report-wrap h4, .report-wrap h5, .report-wrap h6,
.critic-wrap h1, .critic-wrap h2, .critic-wrap h3 {
    color: #f5f0e8 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
    margin-top: 1.6rem !important;
    margin-bottom: 0.5rem !important;
}
.report-wrap h1 { font-size: 1.6rem !important; }
.report-wrap h2 { font-size: 1.25rem !important; color: #f0ebe0 !important; }
.report-wrap h3 { font-size: 1.05rem !important; color: #e8a060 !important; }
.report-wrap strong, .critic-wrap strong,
.report-wrap b, .critic-wrap b {
    color: #f0ebe0 !important;
    font-weight: 700 !important;
}
.report-wrap em, .critic-wrap em,
.report-wrap i, .critic-wrap i {
    color: #c8b89a !important;
}
.report-wrap a, .critic-wrap a {
    color: #ff8c32 !important;
    text-decoration: underline !important;
    text-underline-offset: 3px !important;
}
.report-wrap code, .critic-wrap code {
    background: rgba(255,140,50,0.1) !important;
    color: #ff8c32 !important;
    border-radius: 5px !important;
    padding: 0.1em 0.45em !important;
    font-size: 0.85em !important;
    font-family: 'JetBrains Mono', monospace !important;
}
.report-wrap ul, .report-wrap ol,
.critic-wrap ul, .critic-wrap ol {
    padding-left: 1.4rem !important;
    margin: 0.6rem 0 !important;
}
.report-wrap li, .critic-wrap li {
    margin-bottom: 0.35rem !important;
    color: #cdc8bf !important;
}
.report-wrap li::marker { color: #ff8c32 !important; }
.critic-wrap li::marker  { color: #50c878 !important; }
.report-wrap blockquote, .critic-wrap blockquote {
    border-left: 3px solid rgba(255,140,50,0.4) !important;
    padding-left: 1rem !important;
    margin: 1rem 0 !important;
    color: #a09080 !important;
    font-style: italic !important;
}
.report-wrap hr, .critic-wrap hr {
    border: none !important;
    border-top: 1px solid rgba(255,255,255,0.08) !important;
    margin: 1.5rem 0 !important;
}

/* Override Streamlit's default stMarkdown color inside panels */
.report-wrap .stMarkdown p,
.report-wrap .stMarkdown li,
.critic-wrap .stMarkdown p,
.critic-wrap .stMarkdown li {
    color: #d4cfc7 !important;
}
.report-wrap .stMarkdown h1,
.report-wrap .stMarkdown h2,
.report-wrap .stMarkdown h3,
.critic-wrap .stMarkdown h1,
.critic-wrap .stMarkdown h2,
.critic-wrap .stMarkdown h3 {
    color: #f5f0e8 !important;
}

/* ─── Animated pulse for active step icon ─── */
@keyframes pulse-ring {
    0%   { box-shadow: 0 0 0 0   rgba(255,140,50,0.4); }
    70%  { box-shadow: 0 0 0 8px rgba(255,140,50,0); }
    100% { box-shadow: 0 0 0 0   rgba(255,140,50,0); }
}

/* ─── Global markdown text brightness fix ─── */
.stMarkdown p, .stMarkdown li, .stMarkdown span,
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] span,
[data-testid="stMarkdownContainer"] ol,
[data-testid="stMarkdownContainer"] ul {
    color: #cdc8bf !important;
    font-family: 'Space Grotesk', sans-serif !important;
    line-height: 1.8 !important;
}
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4 {
    color: #f5f0e8 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
[data-testid="stMarkdownContainer"] strong,
[data-testid="stMarkdownContainer"] b {
    color: #f0ebe0 !important;
}
[data-testid="stMarkdownContainer"] a {
    color: #ff8c32 !important;
}
[data-testid="stMarkdownContainer"] li::marker {
    color: #ff8c32 !important;
}

</style>
""", unsafe_allow_html=True)


# ── Helper: render a pipeline step card ──────────────────────────────────────
STEP_ICONS = {
    "search": ("⌖", "icon-search"),
    "reader": ("◈", "icon-reader"),
    "writer": ("◇", "icon-writer"),
    "critic": ("◉", "icon-critic"),
}

def step_card(key: str, num: str, title: str, state: str, desc: str = ""):
    badge_map = {
        "waiting": ("idle", "badge-wait"),
        "running": ("live", "badge-run"),
        "done":    ("done",  "badge-done"),
    }
    badge_text, badge_cls = badge_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    icon, icon_cls = STEP_ICONS.get(key, ("○", ""))
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-icon {icon_cls}">{icon}</div>
        <div class="step-body">
            <div class="step-title-row">
                <span class="step-name">{title}</span>
                <span class="step-badge {badge_cls}">{badge_text}</span>
            </div>
            <div class="step-desc">{desc}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Top navigation bar ────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <div class="logo">
        <div class="logo-hex"></div>
        <span class="logo-name">Syn<span>apse</span></span>
    </div>
    <span class="nav-tag">Research Intelligence</span>
</div>
""", unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-kicker">Multi-Agent AI Pipeline</div>
    <h1>Research that<br/><em>thinks deeper.</em></h1>
    <p class="hero-desc">
        Four specialized AI agents — search, read, write, critique —
        working in sequence to surface insights you'd otherwise miss.
    </p>
</div>
""", unsafe_allow_html=True)


# ── Main two-column layout ────────────────────────────────────────────────────
col_left, col_right = st.columns([3, 1.4])

with col_left:
    # Input card
    st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
    topic = st.text_input(
        "Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        key="topic_input",
        label_visibility="visible",
    )
    run_btn = st.button("⬡  Run Synapse Pipeline", use_container_width=True)

    # Example chips
    st.markdown("""
    <div class="chips-row">
        <span class="chips-label">Try →</span>
        <span class="chip">LLM agents 2025</span>
        <span class="chip">CRISPR gene editing</span>
        <span class="chip">Fusion energy progress</span>
        <span class="chip">Dark matter theories</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    # Pipeline status panel
    st.markdown('<div class="pipeline-header">Pipeline · 4 agents</div>', unsafe_allow_html=True)

    r = st.session_state.results

    def get_state(step):
        steps = ["search", "reader", "writer", "critic"]
        if step in r:
            return "done"
        if st.session_state.running:
            for k in steps:
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    step_card("search", "01", "Search Agent",  get_state("search"), "Gathers live web intelligence")
    step_card("reader", "02", "Reader Agent",  get_state("reader"), "Scrapes & extracts deep content")
    step_card("writer", "03", "Writer Chain",  get_state("writer"), "Synthesizes a research report")
    step_card("critic", "04", "Critic Chain",  get_state("critic"), "Scores & refines the output")


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Enter a research topic to begin.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    with st.spinner("⌖  Search agent scanning the web…"):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)

    with st.spinner("◈  Reader agent extracting deep content…"):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    with st.spinner("◇  Writer crafting the report…"):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })
        st.session_state.results = dict(results)

    with st.spinner("◉  Critic evaluating quality…"):
        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="thin-rule"></div>', unsafe_allow_html=True)
    st.markdown('<div class="results-heading">Output</div>', unsafe_allow_html=True)

    if "search" in r:
        with st.expander("⌖  Search agent — raw output", expanded=False):
            st.markdown(
                f'<div class="raw-panel">'
                f'<div class="raw-panel-label">Search Agent Output</div>'
                f'<div class="raw-panel-content">{r["search"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    if "reader" in r:
        with st.expander("◈  Reader agent — raw output", expanded=False):
            st.markdown(
                f'<div class="raw-panel">'
                f'<div class="raw-panel-label">Reader Agent Output</div>'
                f'<div class="raw-panel-content">{r["reader"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    if "writer" in r:
        st.markdown('<div class="report-wrap"><div class="report-label">◇ Research Report</div>', unsafe_allow_html=True)
        st.markdown(r["writer"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.download_button(
            label="↓  Download report (.md)",
            data=r["writer"],
            file_name=f"synapse_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    if "critic" in r:
        st.markdown('<div class="critic-wrap"><div class="critic-label">◉ Critic Analysis</div>', unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Synapse · Multi-Agent Research Intelligence · Powered by LangChain &amp; Streamlit
</div>
""", unsafe_allow_html=True)