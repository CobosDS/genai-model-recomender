"""
Model Selector Chat — Streamlit app.

Run:
  streamlit run app.py
"""
import json
import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

load_dotenv(override=True)
sys.path.insert(0, str(Path(__file__).parent))

from src.agent.chat import ModelSelectorChat

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GenAI Model Recommender",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
[data-testid="stSidebarNav"] { display: none; }
.model-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 0.8rem; margin: 0.8rem 0 1.2rem; }
.mc {
    background: #1e1e2e;
    border: 1px solid #313244;
    border-radius: 12px;
    padding: 1rem 1.1rem;
    display: flex; flex-direction: column; gap: 0.5rem;
}
.mc.r1 { border-top: 3px solid #a6e3a1; }
.mc.r2 { border-top: 3px solid #89b4fa; }
.mc.r3 { border-top: 3px solid #cba6f7; }
.mc-badge { font-size: 0.68rem; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; color: #a6adc8; }
.mc.r1 .mc-badge { color: #a6e3a1; }
.mc.r2 .mc-badge { color: #89b4fa; }
.mc.r3 .mc-badge { color: #cba6f7; }
.mc-name { font-size: 0.95rem; font-weight: 700; color: #cdd6f4; line-height: 1.2; }
.mc-provider { font-size: 0.72rem; color: #6c7086; margin-top: -0.2rem; }
.mc-specs { display: flex; flex-wrap: wrap; gap: 0.5rem 1rem; }
.mc-spec { font-size: 0.78rem; color: #a6adc8; }
.mc-spec b { color: #cdd6f4; }
.mc-price { font-size: 0.82rem; font-weight: 600; }
.mc-price.free { color: #a6e3a1; }
.mc-price.paid { color: #f9e2af; }
.mc-caps { display: flex; flex-wrap: wrap; gap: 0.3rem; margin-top: 0.2rem; }
.mc-cap { font-size: 0.68rem; background: #313244; color: #89b4fa; padding: 2px 7px; border-radius: 99px; }
.mc-desc { font-size: 0.75rem; color: #6c7086; line-height: 1.4; }
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
WELCOME = (
    "Hi! I'm your GenAI model recommender. I search a database of 288 models "
    "across 9 providers and recommend the best fit for your project.\n\n"
    "To get a good recommendation, tell me:\n\n"
    "**What are you building?** A chatbot, a code assistant, document processing, "
    "image analysis...\n\n"
    "**What's your budget?** Free and self-hosted, cheap API, or no limit.\n\n"
    "The more context you give (latency needs, data privacy, expected volume) "
    "the better the recommendation."
)

QUICK_STARTS = [
    "Cheap model for a customer support chatbot",
    "Free open-source LLM for text classification",
    "Best model for code generation, no budget limit",
    "Vision model to process invoice images",
    "Fastest model for real-time chat under $1/1M tokens",
]

# ── Session state ─────────────────────────────────────────────────────────────
if "model" not in st.session_state:
    st.session_state.model = "gpt-4.1-mini"
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "agent" not in st.session_state:
    st.session_state.agent = None
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": WELCOME}]
if "quick_start" not in st.session_state:
    st.session_state.quick_start = None

agent: ModelSelectorChat | None = st.session_state.agent


# ── Helpers ───────────────────────────────────────────────────────────────────
def _ctx_str(ctx: int | None) -> str:
    if not ctx:
        return "—"
    if ctx >= 900_000:
        return f"{ctx // 1_000_000}M"
    return f"{ctx // 1000}k"


def render_model_card(m: dict, rank: int) -> str:
    rank_class = f"r{rank}" if rank <= 3 else ""
    rank_labels = {1: "★ Best match", 2: "Runner-up", 3: "Alternative"}
    rank_label = rank_labels.get(rank, f"#{rank}")

    ctx = _ctx_str(m.get("context_window"))
    inp = m.get("input_price") or m.get("input_per_1m")
    out = m.get("output_price") or m.get("output_per_1m")
    is_oss = m.get("is_open_source")

    vram = m.get("min_vram_gb")
    if vram is not None:
        price_html = f'<span class="mc-price free">Self-hosted · {vram:.0f} GB VRAM</span>'
    elif inp == 0.0:
        price_html = '<span class="mc-price free">Free API</span>'
    elif inp is not None:
        out_str = f"/ ${out:.2f} out" if out is not None else ""
        price_html = f'<span class="mc-price paid">${inp:.2f} in {out_str} per 1M</span>'
    else:
        price_html = '<span class="mc-price">—</span>'

    caps = m.get("features") or m.get("capabilities") or []
    caps_html = "".join(f'<span class="mc-cap">{c}</span>' for c in caps[:4]) if caps else ""

    desc_html = ""

    provider = m.get("provider") or ""
    oss_tag = " · open-source" if is_oss else ""
    license_str = m.get("license") or ""
    license_html = f'<span class="mc-cap">{license_str}</span>' if license_str else ""

    return f"""
    <div class="mc {rank_class}">
        <div class="mc-badge">{rank_label}</div>
        <div class="mc-name">{m.get("name") or m.get("model_id")}</div>
        <div class="mc-provider">{provider}{oss_tag}</div>
        {price_html}
        <div class="mc-specs">
            <div class="mc-spec">Context <b>{ctx}</b></div>
        </div>
        {"<div class='mc-caps'>" + license_html + caps_html + "</div>" if (license_html or caps_html) else ""}
        {desc_html}
    </div>
    """


def render_model_cards(models: list[dict]) -> str:
    cards = "".join(render_model_card(m, i + 1) for i, m in enumerate(models[:3]))
    return f'<div class="model-grid">{cards}</div>'


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    api_key_input = st.text_input(
        "OpenAI API key",
        type="password",
        placeholder="sk-...",
        value=st.session_state.api_key,
        help="Your key is only used in this session and never stored.",
    )
    if api_key_input != st.session_state.api_key:
        st.session_state.api_key = api_key_input
        st.session_state.agent = None
        agent = None
        st.rerun()

    model_choice = st.selectbox(
        "Agent model",
        ["gpt-4.1-mini", "o4-mini", "gpt-4.1"],
        index=["gpt-4.1-mini", "o4-mini", "gpt-4.1"].index(st.session_state.model),
    )
    if model_choice != st.session_state.model:
        st.session_state.model = model_choice
        st.session_state.messages = [{"role": "assistant", "content": WELCOME}]
        st.session_state.agent = None
        agent = None
        st.rerun()

    _key = st.session_state.api_key or __import__("os").environ.get("OPENAI_API_KEY", "")
    if _key and st.session_state.agent is None:
        st.session_state.agent = ModelSelectorChat(model=st.session_state.model, api_key=_key)
        agent = st.session_state.agent

    if st.button("New conversation", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": WELCOME}]
        _key = st.session_state.api_key or __import__("os").environ.get("OPENAI_API_KEY", "")
        st.session_state.agent = ModelSelectorChat(model=st.session_state.model, api_key=_key) if _key else None
        agent = st.session_state.agent
        st.rerun()

    st.divider()
    st.page_link("app.py",               label="🤖 App",        use_container_width=True)
    st.divider()
    st.page_link("pages/1_Pipeline.py",  label="🔄 Pipeline",   use_container_width=True)
    st.page_link("pages/5_Agent.py",     label="💬 Chat Agent", use_container_width=True)
    st.divider()
    st.caption("ETL Agents")
    st.page_link("pages/4_Enrich.py",    label="✨ Enrich Agent",     use_container_width=True)
    st.page_link("pages/6_Discovery.py", label="🔭 Discovery Agent",  use_container_width=True)

# ── Main ──────────────────────────────────────────────────────────────────────
st.title("🤖 GenAI Model Recommender")
st.divider()

# Quick start chips (only on first message)
if len(st.session_state.messages) == 1:
    st.markdown("**Quick starts:**")
    cols = st.columns(len(QUICK_STARTS))
    for col, label in zip(cols, QUICK_STARTS):
        if col.button(label, use_container_width=True):
            st.session_state.quick_start = label

    with st.expander("🔍 Quick filters"):
        col1, col2, col3 = st.columns(3)
        with col1:
            budget = st.select_slider(
                "Max input price ($/1M tokens)",
                options=["free", "$0.5", "$1", "$2", "$5", "$10", "no limit"],
                value="no limit",
            )
            min_ctx = st.selectbox(
                "Minimum context window",
                ["Any", "8k+", "32k+", "128k+", "200k+", "1M+"],
            )
        with col2:
            capabilities = st.multiselect(
                "Required capabilities",
                ["vision", "reasoning", "function_calling", "audio_input", "code", "structured_output"],
            )
            provider_filter = st.text_input("Provider", placeholder="e.g. Anthropic, OpenAI")
        with col3:
            open_source_only = st.checkbox(
                "Open-source only",
                disabled=bool(provider_filter),
            )
            if provider_filter:
                st.caption("_Open-source filter disabled when provider is set._")
            if st.button("Search with filters", use_container_width=True, type="primary"):
                parts = []
                if budget != "no limit":
                    parts.append(f"budget: {budget} per 1M tokens")
                if min_ctx != "Any":
                    parts.append(f"minimum context window: {min_ctx}")
                if capabilities:
                    parts.append(f"required capabilities: {', '.join(capabilities)}")
                if provider_filter:
                    parts.append(f"provider: {provider_filter}")
                elif open_source_only:
                    parts.append("open-source only, free to self-host")
                if parts:
                    st.session_state.quick_start = "I need a model with: " + "; ".join(parts)

# Chat history
for msg in st.session_state.messages:
    avatar = "developer.jpg" if msg["role"] == "user" else None
    with st.chat_message(msg["role"], avatar=avatar):
        if msg["role"] == "assistant" and msg.get("models"):
            st.html(render_model_cards(msg["models"]))
        st.markdown(msg["content"])

# ── Handle input (chat or quick start) ───────────────────────────────────────
prompt = st.chat_input("Describe your project or requirements...")

if st.session_state.quick_start and not prompt:
    prompt = st.session_state.quick_start
    st.session_state.quick_start = None

_has_key = bool(st.session_state.api_key or __import__("os").environ.get("OPENAI_API_KEY", ""))

if not _has_key:
    st.info("Enter your OpenAI API key in the sidebar to start chatting.", icon="🔑")

if prompt and _has_key and agent:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="developer.jpg"):
        st.markdown(prompt)

    found_models: list[dict] = []
    full_reply = ""

    with st.chat_message("assistant"):
        status = st.empty()
        placeholder = st.empty()
        for event, data in agent.stream(prompt):
            if event == "status":
                status.markdown(f"_{data}_")
            elif event == "models":
                status.empty()
                found_models = json.loads(data)
                st.html(render_model_cards(found_models))
            elif event == "token":
                status.empty()
                full_reply += data
                placeholder.markdown(full_reply + "▌")
        placeholder.markdown(full_reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": full_reply,
        "models": found_models,
    })
