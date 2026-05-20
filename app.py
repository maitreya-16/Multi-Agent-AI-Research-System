import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain
from langchain_core.messages import ToolMessage

st.set_page_config(
    page_title="ResearchMind",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:ital,wght@0,300;0,400;1,300&display=swap');

  /* Global reset */
  html, body, [class*="css"] {
    font-family: 'DM Mono', monospace;
  }

  /* Dark background */
  .stApp {
    background-color: #0a0a0f;
    color: #e8e8f0;
  }

  /* Hide default streamlit chrome */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 2rem; padding-bottom: 4rem; }

  /* ── Hero title ── */
  .hero-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 3.4rem;
    letter-spacing: -0.03em;
    line-height: 1;
    background: linear-gradient(135deg, #e8e8f0 30%, #7b6ef6 70%, #f06292 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem;
  }
  .hero-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    font-weight: 300;
    color: #555570;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 2.5rem;
  }

  /* ── Input box ── */
  .stTextInput > div > div > input {
    background: #111120 !important;
    border: 1px solid #2a2a40 !important;
    border-radius: 4px !important;
    color: #e8e8f0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s;
  }
  .stTextInput > div > div > input:focus {
    border-color: #7b6ef6 !important;
    box-shadow: 0 0 0 2px rgba(123,110,246,0.15) !important;
  }

  /* ── Run button ── */
  .stButton > button {
    background: linear-gradient(135deg, #7b6ef6, #f06292) !important;
    border: none !important;
    border-radius: 4px !important;
    color: #fff !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.08em !important;
    padding: 0.65rem 2rem !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.1s !important;
  }
  .stButton > button:hover { opacity: 0.85 !important; transform: translateY(-1px) !important; }
  .stButton > button:active { transform: translateY(0) !important; }

  /* ── Step card ── */
  .step-card {
    background: #111120;
    border: 1px solid #1e1e30;
    border-left: 3px solid #7b6ef6;
    border-radius: 6px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
  }
  .step-card.active { border-left-color: #f0c060; }
  .step-card.done   { border-left-color: #56e39f; }
  .step-card.error  { border-left-color: #f06292; }

  .step-header {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.82rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
  }
  .step-header.active { color: #f0c060; }
  .step-header.done   { color: #56e39f; }
  .step-header.idle   { color: #444460; }

  /* ── Result expanders ── */
  .stExpander {
    border: 1px solid #1e1e30 !important;
    border-radius: 6px !important;
    background: #111120 !important;
  }
  details > summary {
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    color: #9090b8 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.05em !important;
  }

  /* ── Metric strip ── */
  .metric-strip {
    display: flex;
    gap: 1.5rem;
    padding: 0.8rem 1.2rem;
    background: #111120;
    border: 1px solid #1e1e30;
    border-radius: 6px;
    margin-bottom: 1.5rem;
  }
  .metric-item { display: flex; flex-direction: column; }
  .metric-label {
    font-size: 0.65rem;
    color: #555570;
    text-transform: uppercase;
    letter-spacing: 0.15em;
  }
  .metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #7b6ef6;
  }

  /* ── Divider ── */
  hr { border-color: #1e1e30 !important; }

  /* ── Output text areas ── */
  .output-block {
    background: #0d0d1a;
    border: 1px solid #1e1e30;
    border-radius: 4px;
    padding: 1rem 1.2rem;
    font-size: 0.85rem;
    line-height: 1.75;
    color: #c0c0d8;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 380px;
    overflow-y: auto;
  }

  /* scrollbar */
  .output-block::-webkit-scrollbar { width: 4px; }
  .output-block::-webkit-scrollbar-track { background: #0a0a0f; }
  .output-block::-webkit-scrollbar-thumb { background: #2a2a40; border-radius: 2px; }

  /* ── Status badge ── */
  .badge {
    display: inline-block;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.2rem 0.55rem;
    border-radius: 3px;
    margin-left: 0.5rem;
  }
  .badge-running { background: rgba(240,192,96,0.15); color: #f0c060; }
  .badge-done    { background: rgba(86,227,159,0.12); color: #56e39f; }
  .badge-idle    { background: rgba(100,100,120,0.15); color: #666680; }
</style>
""", unsafe_allow_html=True)


def extract_search_results(search_result):
    for msg in search_result["messages"]:
        if isinstance(msg, ToolMessage):
            return msg.content
    return "No search results found."


def badge(status: str) -> str:
    if status == "running":
        return '<span class="badge badge-running">● running</span>'
    elif status == "done":
        return '<span class="badge badge-done">✓ done</span>'
    return '<span class="badge badge-idle">○ idle</span>'


def step_card(number: str, title: str, status: str, description: str):
    cls = {"running": "active", "done": "done", "idle": ""}.get(status, "")
    hdr_cls = {"running": "active", "done": "done", "idle": "idle"}.get(status, "idle")
    st.markdown(f"""
    <div class="step-card {cls}">
      <div class="step-header {hdr_cls}">
        {number} · {title} {badge(status)}
      </div>
      <div style="font-size:0.82rem;color:#666680;">{description}</div>
    </div>
    """, unsafe_allow_html=True)



st.markdown('<div class="hero-title">ResearchMind</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Multi-Agent Autonomous Research System</div>', unsafe_allow_html=True)

col_input, col_btn = st.columns([5, 1])
with col_input:
    topic = st.text_input(
        label="topic",
        placeholder="e.g.  Quantum computing breakthroughs in 2025",
        label_visibility="collapsed",
    )
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    run = st.button("RUN →", use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

col_steps, col_results = st.columns([1, 2])

with col_steps:
    st.markdown(
        '<div style="font-family:\'Syne\',sans-serif;font-size:0.78rem;'
        'letter-spacing:0.14em;text-transform:uppercase;color:#555570;'
        'margin-bottom:0.8rem;">Pipeline Steps</div>',
        unsafe_allow_html=True,
    )
    step1_ph = st.empty()
    step2_ph = st.empty()
    step3_ph = st.empty()
    step4_ph = st.empty()

    def render_steps(s1="idle", s2="idle", s3="idle", s4="idle"):
        with step1_ph:
            step_card("01", "Search Agent", s1, "Web search · source discovery")
        with step2_ph:
            step_card("02", "Reader Agent", s2, "URL scraping · deep extraction")
        with step3_ph:
            step_card("03", "Writer Chain", s3, "Report drafting · synthesis")
        with step4_ph:
            step_card("04", "Critic Chain", s4, "Fact-checking · quality score")

    render_steps()

with col_results:
    results_header = st.empty()
    results_header.markdown(
        '<div style="font-family:\'Syne\',sans-serif;font-size:0.78rem;'
        'letter-spacing:0.14em;text-transform:uppercase;color:#555570;'
        'margin-bottom:0.8rem;">Output</div>',
        unsafe_allow_html=True,
    )
    output_ph = st.empty()
    output_ph.markdown(
        '<div class="output-block" style="color:#333350;font-style:italic;">'
        'Results will appear here once the pipeline runs…'
        '</div>',
        unsafe_allow_html=True,
    )

if run and topic.strip():
    state = {}
    t_start = time.time()

    render_steps(s1="running")
    with col_results:
        output_ph.markdown(
            '<div class="output-block">🔍  Search agent is querying the web…</div>',
            unsafe_allow_html=True,
        )

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    state["search_results"] = extract_search_results(search_result)
    render_steps(s1="done")

    render_steps(s1="done", s2="running")
    with col_results:
        output_ph.markdown(
            '<div class="output-block">📄  Reader agent is scraping the best URL…</div>',
            unsafe_allow_html=True,
        )

    reader_agent = build_reader_agent()
    reader_results = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results']}"
        )]
    })
    state["reader_results"] = reader_results["messages"][-1]
    render_steps(s1="done", s2="done")

    render_steps(s1="done", s2="done", s3="running")
    with col_results:
        output_ph.markdown(
            '<div class="output-block">✍️  Writer chain is drafting the report…</div>',
            unsafe_allow_html=True,
        )

    research_combined = (
        f"SEARCH RESULT:\n{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state['reader_results']}"
    )
    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined,
    })
    render_steps(s1="done", s2="done", s3="done")


    render_steps(s1="done", s2="done", s3="done", s4="running")
    with col_results:
        output_ph.markdown(
            '<div class="output-block">🧐  Critic chain is reviewing the report…</div>',
            unsafe_allow_html=True,
        )

    state["critic"] = critic_chain.invoke({"report": state["report"]})
    render_steps(s1="done", s2="done", s3="done", s4="done")

    elapsed = round(time.time() - t_start, 1)


    with col_results:
        output_ph.empty()
        st.markdown(f"""
        <div class="metric-strip">
          <div class="metric-item">
            <span class="metric-label">Topic</span>
            <span class="metric-value" style="font-size:0.9rem;color:#c0c0d8;">{topic[:40]}{'…' if len(topic)>40 else ''}</span>
          </div>
          <div class="metric-item">
            <span class="metric-label">Duration</span>
            <span class="metric-value">{elapsed}s</span>
          </div>
          <div class="metric-item">
            <span class="metric-label">Agents</span>
            <span class="metric-value">4</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("🔍  Search Results", expanded=False):
            st.markdown(
                f'<div class="output-block">{state["search_results"]}</div>',
                unsafe_allow_html=True,
            )

        with st.expander("📄  Scraped Content", expanded=False):
            reader_text = (
                state["reader_results"].content
                if hasattr(state["reader_results"], "content")
                else str(state["reader_results"])
            )
            st.markdown(
                f'<div class="output-block">{reader_text}</div>',
                unsafe_allow_html=True,
            )

        with st.expander("📝  Final Report", expanded=True):
            report_text = (
                state["report"].content
                if hasattr(state["report"], "content")
                else str(state["report"])
            )
            st.markdown(
                f'<div class="output-block">{report_text}</div>',
                unsafe_allow_html=True,
            )

        with st.expander("🧐  Critic Feedback", expanded=True):
            critic_text = (
                state["critic"].content
                if hasattr(state["critic"], "content")
                else str(state["critic"])
            )
            st.markdown(
                f'<div class="output-block">{critic_text}</div>',
                unsafe_allow_html=True,
            )

elif run and not topic.strip():
    st.warning("Please enter a research topic before running the pipeline.")