"""
Pipeline diagram page — Streamlit multipage.
"""
import streamlit as st

st.set_page_config(page_title="How it works", page_icon="🔄", layout="wide")

st.markdown('<style>[data-testid="stSidebarNav"] { display: none; }</style>', unsafe_allow_html=True)

DIAGRAM_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: #1e1e2e;
    color: #cdd6f4;
    font-family: 'Segoe UI', system-ui, sans-serif;
    padding: 2rem;
  }

  h2 { font-size: 1.4rem; color: #cdd6f4; margin-bottom: 0.3rem; text-align: center; }
  .subtitle { color: #6c7086; font-size: 0.82rem; text-align: center; margin-bottom: 2rem; }

  /* ── Layer ── */
  .layer {
    background: #181825;
    border: 1px solid #313244;
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.5rem;
    position: relative;
  }
  .layer-title {
    font-size: 0.65rem;
    font-weight: 800;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: #585b70;
    margin-bottom: 0.9rem;
  }

  /* ── Arrow connector ── */
  .arrow {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 28px;
    color: #45475a;
    font-size: 1.4rem;
  }
  .arrow-split {
    display: flex;
    justify-content: center;
    gap: 12rem;
    height: 28px;
    color: #45475a;
    font-size: 1.4rem;
  }
  .arrow-join {
    display: flex;
    justify-content: center;
    height: 28px;
    color: #45475a;
    font-size: 1.4rem;
  }

  /* ── Provider chips ── */
  .providers { display: flex; flex-wrap: wrap; gap: 0.7rem; align-items: center; }
  .provider {
    display: flex; align-items: center; gap: 0.45rem;
    background: #1e1e2e;
    border: 1px solid #313244;
    border-radius: 99px;
    padding: 0.35rem 0.75rem;
    font-size: 0.78rem;
    font-weight: 500;
    color: #cdd6f4;
  }
  .provider img { width: 16px; height: 16px; filter: brightness(0) invert(1); }
  .provider .badge {
    width: 16px; height: 16px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.55rem; font-weight: 900; color: #fff;
    flex-shrink: 0;
  }

  /* ── Step boxes ── */
  .steps { display: flex; gap: 0.8rem; flex-wrap: wrap; }
  .step {
    flex: 1; min-width: 160px;
    background: #1e1e2e;
    border: 1px solid #313244;
    border-radius: 10px;
    padding: 0.85rem 1rem;
  }
  .step-icon { font-size: 1.3rem; margin-bottom: 0.35rem; }
  .step-name { font-size: 0.82rem; font-weight: 700; color: #cdd6f4; margin-bottom: 0.25rem; }
  .step-desc { font-size: 0.72rem; color: #6c7086; line-height: 1.4; }
  .step-tag {
    display: inline-block; margin-top: 0.4rem;
    font-size: 0.65rem; padding: 2px 7px; border-radius: 99px;
    background: #313244; color: #89b4fa;
  }

  /* ── Split layers ── */
  .split { display: grid; grid-template-columns: 1fr 1fr; gap: 0.8rem; }

  /* ── Storage ── */
  .storage-row { display: flex; gap: 0.8rem; align-items: stretch; }
  .storage-box {
    flex: 1;
    background: #1e1e2e;
    border: 1px solid #313244;
    border-radius: 10px;
    padding: 0.85rem 1rem;
  }
  .storage-box .step-name { color: #a6e3a1; }

  /* ── Accent borders ── */
  .accent-blue  { border-top: 3px solid #89b4fa; }
  .accent-green { border-top: 3px solid #a6e3a1; }
  .accent-pink  { border-top: 3px solid #f38ba8; }
  .accent-peach { border-top: 3px solid #fab387; }
  .accent-mauve { border-top: 3px solid #cba6f7; }
  .accent-teal  { border-top: 3px solid #94e2d5; }
  .accent-yellow{ border-top: 3px solid #f9e2af; }

  /* ── DB tables ── */
  .db-tables { display: flex; gap: 0.5rem; margin-top: 0.6rem; flex-wrap: wrap; }
  .db-table {
    font-size: 0.68rem; padding: 3px 9px; border-radius: 6px;
    background: #313244; color: #94e2d5; font-family: monospace;
  }
</style>
</head>
<body>

<p class="subtitle">From provider docs to structured model data — automated, enriched, and queryable</p>

<!-- ── 1. SOURCES ── -->
<div class="layer accent-blue">
  <div class="layer-title">📡 Data Sources — 9 providers</div>
  <div class="providers">
    <div class="provider">
      <span class="badge" style="background:#10a37f">O</span>
      OpenAI
    </div>
    <div class="provider">
      <img src="https://cdn.simpleicons.org/anthropic/white">
      Anthropic
    </div>
    <div class="provider">
      <img src="https://cdn.simpleicons.org/google/white">
      Google
    </div>
    <div class="provider">
      <img src="https://cdn.simpleicons.org/meta/white">
      Meta
    </div>
    <div class="provider">
      <img src="https://cdn.simpleicons.org/mistralai/white">
      Mistral
    </div>
    <div class="provider">
      <span class="badge" style="background:#39594d">C</span>
      Cohere
    </div>
    <div class="provider">
      <span class="badge" style="background:#4D6BFE">D</span>
      DeepSeek
    </div>
    <div class="provider">
      <span class="badge" style="background:#111">𝕏</span>
      xAI
    </div>
    <div class="provider">
      <img src="https://cdn.simpleicons.org/huggingface/white">
      HuggingFace
    </div>
  </div>
</div>

<div class="arrow">↓</div>

<!-- ── 2. EXTRACT ── -->
<div class="layer accent-peach">
  <div class="layer-title">📥 Extract</div>
  <div class="steps">
    <div class="step">
      <div class="step-icon">🕷️</div>
      <div class="step-name">Jina Reader</div>
      <div class="step-desc">Fetches provider doc pages as clean markdown. One extractor per provider.</div>
      <span class="step-tag">r.jina.ai</span>
    </div>
    <div class="step">
      <div class="step-icon">🤗</div>
      <div class="step-name">HuggingFace API</div>
      <div class="step-desc">Pulls model metadata, config.json, model card, and architecture details via Hub API.</div>
      <span class="step-tag">huggingface_hub</span>
    </div>
    <div class="step">
      <div class="step-icon">💾</div>
      <div class="step-name">Raw snapshots</div>
      <div class="step-desc">Saved as daily JSON files in <code>data/raw/{provider}/YYYY-MM-DD.json</code></div>
      <span class="step-tag">idempotent</span>
    </div>
  </div>
</div>

<div class="arrow">↓</div>

<!-- ── 3. TRANSFORM ── -->
<div class="layer accent-mauve">
  <div class="layer-title">🔄 Transform — raw markdown → ModelRecord</div>
  <div class="steps">
    <div class="step">
      <div class="step-icon">📋</div>
      <div class="step-name">Per-provider parsers</div>
      <div class="step-desc">Regex + structural parsing extracts context window, pricing, modalities, capabilities, family.</div>
      <span class="step-tag">Pydantic schema</span>
    </div>
    <div class="step">
      <div class="step-icon">🏷️</div>
      <div class="step-name">Category derivation</div>
      <div class="step-desc">llm / embedding / image_gen / tts / realtime — inferred from input+output modalities.</div>
      <span class="step-tag">deterministic</span>
    </div>
  </div>
</div>

<div class="arrow">↓</div>

<!-- ── 4. AGENTS ── -->
<div class="layer accent-pink">
  <div class="layer-title">🤖 Agents</div>
  <div class="steps">
    <div class="step">
      <div class="step-icon">✨</div>
      <div class="step-name">Enrich Agent</div>
      <div class="step-desc">GPT-4o-mini fills missing fields: description, strengths, use cases. Grounded with Brave Search.</div>
      <span class="step-tag">tool use</span>
    </div>
    <div class="step">
      <div class="step-icon">📊</div>
      <div class="step-name">Benchmark Agent</div>
      <div class="step-desc">Scrapes artificialanalysis.ai via RSC payload decoding. Token-based fuzzy matching to link model IDs.</div>
      <span class="step-tag">MMLU · GPQA · HLE · AIME</span>
    </div>
    <div class="step">
      <div class="step-icon">👻</div>
      <div class="step-name">Staleness Agent</div>
      <div class="step-desc">Compares current provider listings against the DB and flags models that have disappeared.</div>
      <span class="step-tag">deprecation</span>
    </div>
    <div class="step">
      <div class="step-icon">🔍</div>
      <div class="step-name">Quality Agent</div>
      <div class="step-desc">LLM scans enriched records for inconsistencies: inverted pricing, out-of-range benchmarks, missing fields.</div>
      <span class="step-tag">validation</span>
    </div>
  </div>
</div>

<div class="arrow">↓</div>

<!-- ── 5. STORAGE ── -->
<div class="layer accent-green">
  <div class="layer-title">🗄️ Storage</div>
  <div class="storage-row">
    <div class="storage-box">
      <div class="step-icon">📁</div>
      <div class="step-name">JSON snapshots</div>
      <div class="step-desc">Daily versioned files per provider. Raw → Transformed → Enriched. Full history kept.</div>
      <span class="step-tag">data/raw · data/transformed · data/enriched</span>
    </div>
    <div class="storage-box">
      <div class="step-icon">🗃️</div>
      <div class="step-name">SQLite DB</div>
      <div class="step-desc">Queryable store loaded from latest enriched snapshots. Upsert on each run.</div>
      <div class="db-tables">
        <span class="db-table">models</span>
        <span class="db-table">pricing</span>
        <span class="db-table">benchmark_scores</span>
      </div>
    </div>
    <div class="storage-box">
      <div class="step-icon">📊</div>
      <div class="step-name">Coverage</div>
      <div class="step-desc">288 models · 9 providers · 168 with pricing · 78 with benchmark scores</div>
      <span class="step-tag">as of 2026-04-19</span>
    </div>
  </div>
</div>

<div class="arrow">↓</div>

<!-- ── 6. CHAT AGENT ── -->
<div class="layer accent-yellow">
  <div class="layer-title">💬 Chat Agent</div>
  <div class="steps">
    <div class="step">
      <div class="step-icon">🔧</div>
      <div class="step-name">SQL Tools</div>
      <div class="step-desc">search_models · get_model_details · compare_models · list_providers</div>
      <span class="step-tag">function calling</span>
    </div>
    <div class="step">
      <div class="step-icon">🧠</div>
      <div class="step-name">GPT-4.1-mini</div>
      <div class="step-desc">Conversational agent — asks one clarifying question if needed, then queries DB directly.</div>
      <span class="step-tag">off-topic guard</span>
    </div>
    <div class="step">
      <div class="step-icon">🖥️</div>
      <div class="step-name">Streamlit UI</div>
      <div class="step-desc">Streaming chat, model cards, sidebar filters, quick-start chips.</div>
      <span class="step-tag">localhost:8502</span>
    </div>
  </div>
</div>


</body>
</html>
"""

with st.sidebar:
    st.page_link("app.py",               label="🤖 App",        use_container_width=True)
    st.divider()
    st.page_link("pages/1_Pipeline.py",  label="🔄 Pipeline",   use_container_width=True)
    st.page_link("pages/5_Agent.py",     label="💬 Chat Agent", use_container_width=True)
    st.divider()
    st.caption("ETL Agents")
    st.page_link("pages/4_Enrich.py",    label="✨ Enrich Agent",     use_container_width=True)
    st.page_link("pages/6_Discovery.py", label="🔭 Discovery Agent",  use_container_width=True)

st.title("🔄 How it works")
st.html(DIAGRAM_HTML)
