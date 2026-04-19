"""
Schema diagram page.
"""
import streamlit as st

st.set_page_config(page_title="Schema", page_icon="📐", layout="wide")

st.markdown('<style>[data-testid="stSidebarNav"] { display: none; }</style>', unsafe_allow_html=True)

with st.sidebar:
    st.page_link("app.py", label="🤖 App", use_container_width=True)
    st.divider()
    st.page_link("pages/1_Pipeline.py", label="🔄 Pipeline", use_container_width=True)
    st.page_link("pages/4_Enrich.py", label="✨ Enrich Agent", use_container_width=True)
    st.page_link("pages/5_Agent.py",     label="💬 Chat Agent",       use_container_width=True)
    st.page_link("pages/6_Discovery.py", label="🔭 Discovery Agent",  use_container_width=True)

SCHEMA_HTML = """
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
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
  }

  .erd {
    display: flex;
    gap: 3rem;
    align-items: flex-start;
    justify-content: center;
    flex-wrap: wrap;
  }

  /* ── Table card ── */
  .tbl {
    background: #181825;
    border: 1px solid #313244;
    border-radius: 12px;
    overflow: hidden;
    min-width: 220px;
  }
  .tbl-header {
    padding: 0.6rem 1rem;
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: .08em;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  .tbl-header.blue  { background: #1e3a5f; border-bottom: 2px solid #89b4fa; color: #89b4fa; }
  .tbl-header.green { background: #1e3a2e; border-bottom: 2px solid #a6e3a1; color: #a6e3a1; }
  .tbl-header.mauve { background: #2e1e3a; border-bottom: 2px solid #cba6f7; color: #cba6f7; }

  .tbl-body { padding: 0.4rem 0; }

  .col {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.28rem 1rem;
    font-size: 0.78rem;
  }
  .col:hover { background: #252536; }
  .col-name { color: #cdd6f4; font-family: monospace; flex: 1; }
  .col-type { color: #6c7086; font-size: 0.68rem; }
  .badge {
    font-size: 0.58rem;
    font-weight: 800;
    padding: 1px 5px;
    border-radius: 4px;
    letter-spacing: .04em;
    text-transform: uppercase;
  }
  .pk  { background: #f9e2af22; color: #f9e2af; border: 1px solid #f9e2af55; }
  .fk  { background: #89b4fa22; color: #89b4fa; border: 1px solid #89b4fa55; }
  .idx { background: #a6e3a122; color: #a6e3a1; border: 1px solid #a6e3a155; }
  .enrich { background: #f9e2af22; color: #f9e2af; border: 1px solid #f9e2af55; }

  .divider { border: none; border-top: 1px solid #313244; margin: 0.3rem 0; }

  /* ── Connector lines ── */
  .connectors {
    position: relative;
    width: 100%;
    max-width: 900px;
  }
  svg.lines {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    overflow: visible;
  }

  /* ── Legend ── */
  .legend {
    display: flex;
    gap: 1.2rem;
    font-size: 0.72rem;
    color: #6c7086;
    flex-wrap: wrap;
    justify-content: center;
  }
  .legend-item { display: flex; align-items: center; gap: 0.4rem; }
</style>
</head>
<body>

<div class="erd">

  <!-- ── models ── -->
  <div class="tbl" id="tbl-models">
    <div class="tbl-header blue">🗂️ models</div>
    <div class="tbl-body">
      <div class="col"><span class="badge pk">PK</span><span class="col-name">model_id</span><span class="col-type">TEXT</span></div>
      <hr class="divider">
      <div class="col"><span class="col-name">name</span><span class="col-type">TEXT</span></div>
      <div class="col"><span class="col-name">provider</span><span class="col-type">TEXT</span></div>
      <div class="col"><span class="col-name">family</span><span class="col-type">TEXT</span></div>
      <div class="col"><span class="col-name">is_open_source</span><span class="col-type">INTEGER</span></div>
      <div class="col"><span class="col-name">model_category</span><span class="col-type">TEXT</span></div>
      <div class="col"><span class="badge enrich">✨</span><span class="col-name">context_window</span><span class="col-type">INTEGER</span></div>
      <div class="col"><span class="badge enrich">✨</span><span class="col-name">parameter_count_b</span><span class="col-type">REAL</span></div>
      <div class="col"><span class="col-name">active_parameters_b</span><span class="col-type">REAL</span></div>
      <div class="col"><span class="col-name">input_modalities</span><span class="col-type">JSON</span></div>
      <div class="col"><span class="col-name">output_modalities</span><span class="col-type">JSON</span></div>
      <div class="col"><span class="badge enrich">✨</span><span class="col-name">capabilities</span><span class="col-type">JSON</span></div>
      <div class="col"><span class="col-name">license</span><span class="col-type">TEXT</span></div>
      <div class="col"><span class="col-name">commercial_use</span><span class="col-type">TEXT</span></div>
      <div class="col"><span class="badge enrich">✨</span><span class="col-name">description</span><span class="col-type">TEXT</span></div>
      <div class="col"><span class="badge enrich">✨</span><span class="col-name">strengths</span><span class="col-type">JSON</span></div>
      <div class="col"><span class="badge enrich">✨</span><span class="col-name">use_cases</span><span class="col-type">JSON</span></div>
      <div class="col"><span class="badge enrich">✨</span><span class="col-name">ideal_for</span><span class="col-type">TEXT</span></div>
      <div class="col"><span class="col-name">created_at</span><span class="col-type">TEXT</span></div>
      <div class="col"><span class="col-name">last_modified</span><span class="col-type">TEXT</span></div>
      <div class="col"><span class="col-name">loaded_at</span><span class="col-type">TEXT</span></div>
    </div>
  </div>

  <!-- ── pricing ── -->
  <div class="tbl" id="tbl-pricing">
    <div class="tbl-header green">💰 pricing</div>
    <div class="tbl-body">
      <div class="col"><span class="badge pk">PK</span><span class="col-name">model_id</span><span class="col-type">TEXT</span></div>
      <div class="col"><span class="badge fk">FK</span><span class="col-name">→ models</span><span class="col-type"></span></div>
      <hr class="divider">
      <div class="col"><span class="col-name">input_per_1m</span><span class="col-type">REAL</span></div>
      <div class="col"><span class="col-name">output_per_1m</span><span class="col-type">REAL</span></div>
      <div class="col"><span class="col-name">cached_input_per_1m</span><span class="col-type">REAL</span></div>
      <div class="col"><span class="col-name">batch_input_per_1m</span><span class="col-type">REAL</span></div>
      <div class="col"><span class="col-name">batch_output_per_1m</span><span class="col-type">REAL</span></div>
    </div>
  </div>

  <!-- ── benchmark_scores ── -->
  <div class="tbl" id="tbl-bench">
    <div class="tbl-header mauve">📊 benchmark_scores</div>
    <div class="tbl-body">
      <div class="col"><span class="badge pk">PK</span><span class="col-name">model_id</span><span class="col-type">TEXT</span></div>
      <div class="col"><span class="badge pk">PK</span><span class="col-name">name</span><span class="col-type">TEXT</span></div>
      <div class="col"><span class="badge fk">FK</span><span class="col-name">→ models</span><span class="col-type"></span></div>
      <hr class="divider">
      <div class="col"><span class="col-name">value</span><span class="col-type">REAL</span></div>
      <div class="col"><span class="col-name">metric</span><span class="col-type">TEXT</span></div>
      <div class="col"><span class="col-name">split</span><span class="col-type">TEXT</span></div>
    </div>
  </div>

</div>

<div class="legend">
  <div class="legend-item"><span class="badge pk">PK</span> Primary key</div>
  <div class="legend-item"><span class="badge fk">FK</span> Foreign key</div>
  <div class="legend-item"><span style="color:#6c7086">JSON</span> Stored as JSON array</div>
  <div class="legend-item"><span class="badge enrich">✨</span> Filled by Enrich Agent</div>
</div>

</body>
</html>
"""

ENRICH_EXAMPLE_HTML = """
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
    padding: 1.5rem 2rem;
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
  }
  .example {
    display: grid;
    grid-template-columns: 1fr 64px 1fr;
    align-items: center;
  }
  .box {
    background: #181825;
    border: 1px solid #313244;
    border-radius: 12px;
    overflow: hidden;
  }
  .box-header {
    padding: 0.5rem 1rem;
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: .1em;
    text-transform: uppercase;
  }
  .box-header.before { background: #252536; color: #6c7086; border-bottom: 2px solid #45475a; }
  .box-header.after  { background: #1e3a2e; color: #a6e3a1; border-bottom: 2px solid #a6e3a1; }
  .box-body { padding: 0.5rem 0; }
  .field {
    display: flex;
    gap: 0.6rem;
    padding: 0.28rem 1rem;
    font-size: 0.75rem;
    align-items: flex-start;
  }
  .field-name { color: #6c7086; font-family: monospace; min-width: 105px; flex-shrink: 0; }
  .field-val        { color: #cdd6f4; line-height: 1.4; }
  .field-val.empty  { color: #45475a; font-style: italic; }
  .field-val.filled { color: #a6e3a1; }
  .arrow-col {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    gap: 0.2rem;
  }
  .arrow-label {
    font-size: 0.6rem; font-weight: 800; letter-spacing: .06em;
    text-transform: uppercase; color: #f9e2af;
  }
  .arrow-icon { font-size: 1.6rem; color: #f9e2af; }
</style>
</head>
<body>

<!-- ── Example 1: claude-opus-4-7 ── -->
<div class="example">
  <div class="box">
    <div class="box-header before">⚙️ After transform · claude-opus-4-7</div>
    <div class="box-body">
      <div class="field"><span class="field-name">description</span><span class="field-val">"Our most capable generally available model for complex reasoning and agentic coding"</span></div>
      <div class="field"><span class="field-name">strengths</span><span class="field-val empty">[]</span></div>
      <div class="field"><span class="field-name">use_cases</span><span class="field-val empty">[]</span></div>
      <div class="field"><span class="field-name">ideal_for</span><span class="field-val empty">null</span></div>
    </div>
  </div>
  <div class="arrow-col"><span class="arrow-label">✨ enrich</span><span class="arrow-icon">→</span></div>
  <div class="box">
    <div class="box-header after">✨ After enrichment</div>
    <div class="box-body">
      <div class="field"><span class="field-name">description</span><span class="field-val filled">"Anthropic's most capable model, excelling at complex reasoning, agentic coding, and long-context tasks with a 1M token window."</span></div>
      <div class="field"><span class="field-name">strengths</span><span class="field-val filled">["Highly capable in complex reasoning", "Improved intelligence over predecessors", "Supports text and image inputs"]</span></div>
      <div class="field"><span class="field-name">use_cases</span><span class="field-val filled">["Complex language understanding", "Agentic coding", "Structured data extraction"]</span></div>
      <div class="field"><span class="field-name">ideal_for</span><span class="field-val filled">"Professionals seeking advanced reasoning, coding, and multilingual capabilities."</span></div>
    </div>
  </div>
</div>

<!-- ── Example 2: gpt-4.1-mini ── -->
<div class="example">
  <div class="box">
    <div class="box-header before">⚙️ After transform · gpt-4.1-mini</div>
    <div class="box-body">
      <div class="field"><span class="field-name">description</span><span class="field-val empty">null</span></div>
      <div class="field"><span class="field-name">strengths</span><span class="field-val empty">[]</span></div>
      <div class="field"><span class="field-name">use_cases</span><span class="field-val empty">[]</span></div>
      <div class="field"><span class="field-name">ideal_for</span><span class="field-val empty">null</span></div>
    </div>
  </div>
  <div class="arrow-col"><span class="arrow-label">✨ enrich</span><span class="arrow-icon">→</span></div>
  <div class="box">
    <div class="box-header after">✨ After enrichment</div>
    <div class="box-body">
      <div class="field"><span class="field-name">description</span><span class="field-val filled">"GPT-4.1 mini excels at instruction following and tool calling, with a 1M token context window at low cost."</span></div>
      <div class="field"><span class="field-name">strengths</span><span class="field-val filled">["High instruction-following accuracy", "Fast response time", "Effective tool calling"]</span></div>
      <div class="field"><span class="field-name">use_cases</span><span class="field-val filled">["Conversational agents", "Task automation via function calling", "Content summarization"]</span></div>
      <div class="field"><span class="field-name">ideal_for</span><span class="field-val filled">"Developers seeking efficient text and image processing with structured output."</span></div>
    </div>
  </div>
</div>

<!-- ── Example 3: mistral-large-2512 ── -->
<div class="example">
  <div class="box">
    <div class="box-header before">⚙️ After transform · mistral-large-2512</div>
    <div class="box-body">
      <div class="field"><span class="field-name">description</span><span class="field-val">"Mistral Large 3, is a state-of-the-art, open-weight, general-purpose multimodal model with a granular instruction-following…"</span></div>
      <div class="field"><span class="field-name">strengths</span><span class="field-val empty">[]</span></div>
      <div class="field"><span class="field-name">use_cases</span><span class="field-val empty">[]</span></div>
      <div class="field"><span class="field-name">ideal_for</span><span class="field-val empty">null</span></div>
    </div>
  </div>
  <div class="arrow-col"><span class="arrow-label">✨ enrich</span><span class="arrow-icon">→</span></div>
  <div class="box">
    <div class="box-header after">✨ After enrichment</div>
    <div class="box-body">
      <div class="field"><span class="field-name">description</span><span class="field-val filled">"Mistral Large 3, is a state-of-the-art, open-weight, general-purpose multimodal model with a granular instruction-following…"</span></div>
      <div class="field"><span class="field-name">strengths</span><span class="field-val filled">["Mixture-of-Experts architecture for high scalability", "Strong text generation across varied tasks", "Function calling for API integration"]</span></div>
      <div class="field"><span class="field-name">use_cases</span><span class="field-val filled">["Customer service chatbots", "Automated content generation", "API integration via function calling"]</span></div>
      <div class="field"><span class="field-name">ideal_for</span><span class="field-val filled">"Developers and researchers needing powerful text generation with high efficiency."</span></div>
    </div>
  </div>
</div>

</body>
</html>
"""

st.title("📐 Schema")
st.html(SCHEMA_HTML)
st.divider()
st.subheader("✨ Enrich Agent — example")
st.html(ENRICH_EXAMPLE_HTML)
