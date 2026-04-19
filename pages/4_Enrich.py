"""
Enrich Agent page — flow diagram + before/after examples.
"""
import streamlit as st

st.set_page_config(page_title="Enrich Agent", page_icon="✨", layout="wide")

st.markdown('<style>[data-testid="stSidebarNav"] { display: none; }</style>', unsafe_allow_html=True)

with st.sidebar:
    st.page_link("app.py",               label="🤖 App",        use_container_width=True)
    st.divider()
    st.page_link("pages/1_Pipeline.py",  label="🔄 Pipeline",   use_container_width=True)
    st.page_link("pages/5_Agent.py",     label="💬 Chat Agent", use_container_width=True)
    st.divider()
    st.caption("ETL Agents")
    st.page_link("pages/4_Enrich.py",    label="✨ Enrich Agent",     use_container_width=True)
    st.page_link("pages/6_Discovery.py", label="🔭 Discovery Agent",  use_container_width=True)

FLOW_HTML = """
<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: #1e1e2e; color: #cdd6f4;
  font-family: 'Segoe UI', system-ui, sans-serif;
  padding: 2rem;
  display: flex; flex-direction: column; align-items: center; gap: 0;
}

/* ── Flow nodes ── */
.flow { display: flex; flex-direction: column; align-items: center; width: 100%; max-width: 680px; gap: 0; }

.node {
  width: 100%;
  background: #181825; border: 1px solid #313244; border-radius: 12px;
  padding: 0.9rem 1.2rem;
}
.node-title { font-size: 0.82rem; font-weight: 700; color: #cdd6f4; margin-bottom: 0.25rem; }
.node-desc  { font-size: 0.73rem; color: #6c7086; line-height: 1.5; }
.node-tag {
  display: inline-block; margin-top: 0.4rem;
  font-size: 0.65rem; padding: 2px 8px; border-radius: 99px;
  background: #313244; color: #89b4fa;
}
.node.blue   { border-top: 3px solid #89b4fa; }
.node.yellow { border-top: 3px solid #f9e2af; }
.node.green  { border-top: 3px solid #a6e3a1; }
.node.pink   { border-top: 3px solid #f38ba8; }
.node.mauve  { border-top: 3px solid #cba6f7; }

/* ── Decision diamond ── */
.diamond-wrap { display: flex; flex-direction: column; align-items: center; width: 100%; }
.diamond {
  width: 180px; height: 60px;
  background: #181825; border: 1px solid #fab387;
  transform: rotate(0deg); border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.75rem; font-weight: 700; color: #fab387;
  position: relative;
}
.diamond::before, .diamond::after {
  content: ''; position: absolute;
  border: 8px solid transparent;
}
.branch-row {
  display: flex; justify-content: center; align-items: flex-start;
  gap: 4rem; width: 100%; margin: 0;
}
.branch { display: flex; flex-direction: column; align-items: center; gap: 0; }
.branch-label { font-size: 0.68rem; color: #6c7086; margin: 4px 0; }

/* ── Arrows ── */
.arrow { color: #45475a; font-size: 1.3rem; text-align: center; line-height: 1; padding: 4px 0; }
.arrow-sm { color: #45475a; font-size: 1rem; text-align: center; line-height: 1; padding: 2px 0; }

/* ── Tool node ── */
.tool-node {
  background: #1e1e2e; border: 1px dashed #fab387; border-radius: 10px;
  padding: 0.6rem 0.9rem; font-size: 0.73rem; color: #fab387; text-align: center;
  min-width: 140px;
}

/* ── Merge table ── */
.merge-grid {
  display: grid; grid-template-columns: 1fr 1fr 1fr;
  gap: 0.5rem; margin-top: 0.5rem;
}
.merge-cell {
  background: #1e1e2e; border: 1px solid #313244; border-radius: 8px;
  padding: 0.4rem 0.6rem; font-size: 0.7rem;
}
.merge-cell .label { color: #89b4fa; font-weight: 700; margin-bottom: 0.2rem; }
.merge-cell .fields { color: #6c7086; font-family: monospace; font-size: 0.65rem; line-height: 1.6; }
</style>
</head>
<body>
<div class="flow">

  <!-- 1. INPUT -->
  <div class="node blue">
    <div class="node-title">📂 Take each model from the database</div>
    <div class="node-desc">For every AI model collected from providers, the agent checks if its information is complete enough to be useful.</div>
  </div>
  <div class="arrow">↓</div>

  <!-- 2. CHECK -->
  <div class="node yellow">
    <div class="node-title">🔍 What information is incomplete?</div>
    <div class="node-desc">
      The agent skips models that are already fully documented. It flags a model if the description, strengths, use cases, or ideal audience are missing or too thin.
    </div>
  </div>
  <div class="arrow">↓</div>

  <!-- 3. PROMPT -->
  <div class="node mauve">
    <div class="node-title">📝 Prepare the AI's instructions</div>
    <div class="node-desc">The agent gathers everything already known about the model and tells the AI exactly which fields need filling, without overwriting good existing data.</div>
  </div>
  <div class="arrow">↓</div>

  <!-- 4. LLM LOOP -->
  <div class="node pink">
    <div class="node-title">🤖 AI reads the available information</div>
    <div class="node-desc">The AI reads what we know about the model and decides whether it has enough to fill in the missing details, or whether it needs to look something up first.</div>
  </div>
  <div class="arrow">↓</div>

  <!-- 5. BRANCH -->
  <div class="diamond-wrap">
    <div class="diamond">enough information?</div>
    <div class="branch-row">
      <div class="branch">
        <span class="branch-label">no</span>
        <div class="arrow-sm">↓</div>
        <div class="tool-node">🔎 Search the web<br><span style="font-size:0.62rem;color:#6c7086">Brave Search</span></div>
        <div class="arrow-sm">↓</div>
        <div class="tool-node" style="border-color:#cba6f7;color:#cba6f7">↩ Back to AI with new info</div>
      </div>
      <div class="branch">
        <span class="branch-label">yes</span>
        <div class="arrow-sm">↓</div>
        <div class="tool-node" style="border-color:#6c7086;color:#a6adc8">📄 Uses existing docs<br><span style="font-size:0.62rem;color:#6c7086">+ general knowledge</span></div>
      </div>
    </div>
  </div>
  <div class="arrow">↓</div>

  <!-- 6. PARSE -->
  <div class="node yellow">
    <div class="node-title">📤 AI writes the missing fields</div>
    <div class="node-desc">The AI produces a structured response with each missing field filled in: description, strengths, use cases, and who the model is ideal for.</div>
  </div>
  <div class="arrow">↓</div>

  <!-- 7. MERGE -->
  <div class="node green">
    <div class="node-title">🔀 Update the model's record</div>
    <div class="node-desc">The new information is merged carefully into the existing record. Fields already populated are never overwritten; only gaps are filled.</div>
    <div class="merge-grid">
      <div class="merge-cell">
        <div class="label">Fill if empty</div>
        <div class="fields">Description<br>Strengths<br>Use cases<br>Ideal for</div>
      </div>
      <div class="merge-cell">
        <div class="label">Add new items</div>
        <div class="fields">Capabilities<br>(no duplicates)</div>
      </div>
      <div class="merge-cell">
        <div class="label">Fill if unknown</div>
        <div class="fields">Context window<br>Parameter count</div>
      </div>
    </div>
  </div>
  <div class="arrow">↓</div>

  <!-- 8. SAVE -->
  <div class="node blue">
    <div class="node-title">💾 Save the enriched data</div>
    <div class="node-desc">The updated records are saved as a daily snapshot. Each run only touches what's changed, so the full history is preserved.</div>
  </div>

</div>
</body></html>
"""

EXAMPLES_HTML = """
<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: #1e1e2e; color: #cdd6f4;
  font-family: 'Segoe UI', system-ui, sans-serif;
  padding: 1.5rem 2rem;
  display: flex; flex-direction: column; gap: 1.2rem;
}
.example { display: grid; grid-template-columns: 1fr 64px 1fr; align-items: center; }
.box { background: #181825; border: 1px solid #313244; border-radius: 12px; overflow: hidden; }
.box-header { padding: 0.5rem 1rem; font-size: 0.68rem; font-weight: 800; letter-spacing: .1em; text-transform: uppercase; }
.box-header.before { background: #252536; color: #6c7086; border-bottom: 2px solid #45475a; }
.box-header.after  { background: #1e3a2e; color: #a6e3a1; border-bottom: 2px solid #a6e3a1; }
.box-body { padding: 0.5rem 0; }
.field { display: flex; gap: 0.6rem; padding: 0.28rem 1rem; font-size: 0.75rem; align-items: flex-start; }
.field-name { color: #6c7086; font-family: monospace; min-width: 105px; flex-shrink: 0; }
.field-val        { color: #cdd6f4; line-height: 1.4; }
.field-val.empty  { color: #45475a; font-style: italic; }
.field-val.filled { color: #a6e3a1; }
.arrow-col { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.2rem; }
.arrow-label { font-size: 0.6rem; font-weight: 800; letter-spacing: .06em; text-transform: uppercase; color: #f9e2af; }
.arrow-icon { font-size: 1.6rem; color: #f9e2af; }
</style>
</head>
<body>

<!-- claude-opus-4-7 -->
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

<!-- gpt-4.1-mini -->
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

<!-- mistral-large-2512 -->
<div class="example">
  <div class="box">
    <div class="box-header before">⚙️ After transform · mistral-large-2512</div>
    <div class="box-body">
      <div class="field"><span class="field-name">description</span><span class="field-val">"Mistral Large 3, is a state-of-the-art, open-weight, general-purpose multimodal model…"</span></div>
      <div class="field"><span class="field-name">strengths</span><span class="field-val empty">[]</span></div>
      <div class="field"><span class="field-name">use_cases</span><span class="field-val empty">[]</span></div>
      <div class="field"><span class="field-name">ideal_for</span><span class="field-val empty">null</span></div>
    </div>
  </div>
  <div class="arrow-col"><span class="arrow-label">✨ enrich</span><span class="arrow-icon">→</span></div>
  <div class="box">
    <div class="box-header after">✨ After enrichment</div>
    <div class="box-body">
      <div class="field"><span class="field-name">description</span><span class="field-val">"Mistral Large 3, is a state-of-the-art, open-weight, general-purpose multimodal model…"</span></div>
      <div class="field"><span class="field-name">strengths</span><span class="field-val filled">["MoE architecture for high scalability", "Strong performance across text tasks", "Function calling for API integration"]</span></div>
      <div class="field"><span class="field-name">use_cases</span><span class="field-val filled">["Customer service chatbots", "Automated content generation", "API integration"]</span></div>
      <div class="field"><span class="field-name">ideal_for</span><span class="field-val filled">"Developers and researchers needing powerful text generation with high efficiency."</span></div>
    </div>
  </div>
</div>

</body></html>
"""

COVERAGE_HTML = """
<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: #1e1e2e; color: #cdd6f4;
  font-family: 'Segoe UI', system-ui, sans-serif;
  padding: 1.5rem 2rem;
  display: flex; flex-direction: column; gap: 1.5rem;
}
table { width: 100%; border-collapse: collapse; }
thead tr { border-bottom: 2px solid #313244; }
th { font-size: 0.72rem; font-weight: 800; letter-spacing: .07em; text-transform: uppercase;
     color: #6c7086; padding: 0.5rem 1rem; text-align: left; }
tbody tr { border-bottom: 1px solid #252536; }
tbody tr:hover { background: #252536; }
td { padding: 0.45rem 1rem; font-size: 0.8rem; vertical-align: middle; }
.field-name { font-family: monospace; color: #cdd6f4; }
.pct-before { text-align: right; color: #6c7086; white-space: nowrap; }
.pct-after  { text-align: right; color: #a6e3a1; font-weight: 700; white-space: nowrap; }
.gain       { text-align: right; color: #f9e2af; font-weight: 700; white-space: nowrap; }
.bar-cell { width: 220px; }
.bar-wrap { position: relative; height: 8px; background: #313244; border-radius: 99px; overflow: hidden; }
.bar-before { position: absolute; height: 100%; background: #45475a; border-radius: 99px; }
.bar-after  { position: absolute; height: 100%; background: #a6e3a1; border-radius: 99px; opacity: 0.85; }

.section-label { font-size: 0.68rem; font-weight: 800; letter-spacing: .1em; text-transform: uppercase; color: #6c7086; }
</style>
</head>
<body>

<div>
  <div class="section-label" style="margin-bottom:0.8rem">Field coverage: 289 models</div>
  <table>
    <thead>
      <tr><th>Field</th><th style="text-align:right">Before</th><th style="text-align:right">After</th><th style="text-align:right">Gain</th><th></th></tr>
    </thead>
    <tbody>
      <tr><td class="field-name">description</td><td class="pct-before">157 &nbsp;(54%)</td><td class="pct-after">288 &nbsp;(99%)</td><td class="gain">+131</td><td class="bar-cell"><div class="bar-wrap"><div class="bar-before" style="width:54%"></div><div class="bar-after" style="width:99%"></div></div></td></tr>
      <tr><td class="field-name">strengths</td><td class="pct-before">0 &nbsp;(0%)</td><td class="pct-after">288 &nbsp;(99%)</td><td class="gain">+288</td><td class="bar-cell"><div class="bar-wrap"><div class="bar-before" style="width:0%"></div><div class="bar-after" style="width:99%"></div></div></td></tr>
      <tr><td class="field-name">use_cases</td><td class="pct-before">0 &nbsp;(0%)</td><td class="pct-after">288 &nbsp;(99%)</td><td class="gain">+288</td><td class="bar-cell"><div class="bar-wrap"><div class="bar-before" style="width:0%"></div><div class="bar-after" style="width:99%"></div></div></td></tr>
      <tr><td class="field-name">ideal_for</td><td class="pct-before">0 &nbsp;(0%)</td><td class="pct-after">288 &nbsp;(99%)</td><td class="gain">+288</td><td class="bar-cell"><div class="bar-wrap"><div class="bar-before" style="width:0%"></div><div class="bar-after" style="width:99%"></div></div></td></tr>
      <tr><td class="field-name">capabilities</td><td class="pct-before">141 &nbsp;(48%)</td><td class="pct-after">209 &nbsp;(72%)</td><td class="gain">+68</td><td class="bar-cell"><div class="bar-wrap"><div class="bar-before" style="width:48%"></div><div class="bar-after" style="width:72%"></div></div></td></tr>
      <tr><td class="field-name">context_window</td><td class="pct-before">204 &nbsp;(70%)</td><td class="pct-after">258 &nbsp;(89%)</td><td class="gain">+54</td><td class="bar-cell"><div class="bar-wrap"><div class="bar-before" style="width:70%"></div><div class="bar-after" style="width:89%"></div></div></td></tr>
      <tr><td class="field-name">parameter_count_b</td><td class="pct-before">48 &nbsp;(16%)</td><td class="pct-after">109 &nbsp;(37%)</td><td class="gain">+61</td><td class="bar-cell"><div class="bar-wrap"><div class="bar-before" style="width:16%"></div><div class="bar-after" style="width:37%"></div></div></td></tr>
    </tbody>
  </table>
</div>

</body></html>
"""

ACCURACY_HTML = """
<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: #1e1e2e; color: #cdd6f4;
  font-family: 'Segoe UI', system-ui, sans-serif;
  padding: 1.5rem 2rem;
  display: flex; flex-direction: column; gap: 1.8rem;
}
.section-label { font-size: 0.68rem; font-weight: 800; letter-spacing: .1em; text-transform: uppercase; color: #6c7086; margin-bottom: 0.7rem; }

/* ── Model comparison header ── */
.model-header {
  display: flex; gap: 1rem; align-items: center; margin-bottom: 1rem;
}
.model-pill {
  font-size: 0.72rem; font-weight: 700; padding: 3px 12px; border-radius: 99px;
  font-family: monospace;
}
.pill-old { background: #252536; color: #6c7086; border: 1px solid #45475a; }
.pill-new { background: #1e3a24; color: #a6e3a1; border: 1px solid #a6e3a1; }
.pill-arrow { color: #45475a; font-size: 1rem; }

/* ── Score grid ── */
.score-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.7rem; }
.score-card {
  background: #181825; border: 1px solid #313244; border-radius: 12px;
  padding: 0.8rem 1rem;
}
.score-card .field { font-size: 0.68rem; font-weight: 800; letter-spacing: .07em; text-transform: uppercase; color: #6c7086; margin-bottom: 0.6rem; }
.score-row { display: flex; align-items: baseline; gap: 0.5rem; margin-bottom: 0.15rem; }
.score-old { font-size: 1.3rem; font-weight: 800; color: #6c7086; }
.score-arrow { color: #45475a; font-size: 0.9rem; }
.score-new { font-size: 1.6rem; font-weight: 800; }
.score-new.green  { color: #a6e3a1; }
.score-new.yellow { color: #f9e2af; }
.score-new.red    { color: #f38ba8; }
.score-label { font-size: 0.68rem; color: #6c7086; }

/* ── Diff table ── */
table { width: 100%; border-collapse: collapse; }
thead tr { border-bottom: 2px solid #313244; }
th { font-size: 0.68rem; font-weight: 800; letter-spacing: .07em; text-transform: uppercase; color: #6c7086; padding: 0.4rem 0.8rem; text-align: left; }
tbody tr { border-bottom: 1px solid #252536; }
tbody tr:hover { background: #252536; }
td { padding: 0.45rem 0.8rem; font-size: 0.75rem; vertical-align: top; line-height: 1.5; }
.model-id { font-family: monospace; color: #89b4fa; white-space: nowrap; }
.field-tag { display: inline-block; font-size: 0.62rem; padding: 1px 6px; border-radius: 99px; background: #313244; color: #cba6f7; font-family: monospace; margin-bottom: 2px; }
.val-old { color: #585b70; font-size: 0.72rem; }
.val-new { color: #a6e3a1; font-size: 0.72rem; }
.verdict-badge { display: inline-block; font-size: 0.6rem; font-weight: 700; padding: 2px 7px; border-radius: 99px; white-space: nowrap; }
.badge-fixed    { background: #1a3d24; color: #a6e3a1; border: 1px solid #a6e3a1; }
.badge-persist  { background: #3d1a1a; color: #f38ba8; border: 1px solid #f38ba8; }
.badge-improved { background: #3d3214; color: #f9e2af; border: 1px solid #f9e2af; }

/* ── Why section ── */
.why-grid { display: flex; flex-direction: column; gap: 0.7rem; }
.why-card {
  background: #181825; border-left: 3px solid #45475a;
  border-radius: 0 8px 8px 0; padding: 0.6rem 1rem;
  font-size: 0.73rem; color: #6c7086; line-height: 1.6;
}
.why-card .why-title { color: #cdd6f4; font-weight: 700; margin-bottom: 0.2rem; }
.why-card.green  { border-left-color: #a6e3a1; }
.why-card.yellow { border-left-color: #f9e2af; }
.why-card.red    { border-left-color: #f38ba8; }
</style>
</head>
<body>

<!-- Header -->
<div>
  <div class="section-label">Accuracy: 11 LLM models sampled across 8 providers</div>
  <div class="model-header">
    <span class="model-pill pill-old">gpt-4o-mini</span>
    <span class="pill-arrow">→</span>
    <span class="model-pill pill-new">gpt-5.4-mini</span>
  </div>
  <div class="score-grid">
    <div class="score-card">
      <div class="field">Capabilities</div>
      <div class="score-row">
        <span class="score-old">45%</span>
        <span class="score-arrow">→</span>
        <span class="score-new green">91%</span>
      </div>
      <div class="score-label">complete &amp; correct</div>
    </div>
    <div class="score-card">
      <div class="field">Descriptions</div>
      <div class="score-row">
        <span class="score-old">75%</span>
        <span class="score-arrow">→</span>
        <span class="score-new green">91%</span>
      </div>
      <div class="score-label">factually correct</div>
    </div>
    <div class="score-card">
      <div class="field">Strengths</div>
      <div class="score-row">
        <span class="score-old">81%</span>
        <span class="score-arrow">→</span>
        <span class="score-new green">100%</span>
      </div>
      <div class="score-label">factually correct</div>
    </div>
    <div class="score-card">
      <div class="field">Use cases</div>
      <div class="score-row">
        <span class="score-old">88%</span>
        <span class="score-arrow">→</span>
        <span class="score-new green">100%</span>
      </div>
      <div class="score-label">plausible &amp; correct</div>
    </div>
  </div>
</div>

<!-- Diff table -->
<div>
  <div class="section-label">What changed, model by model</div>
  <table>
    <thead>
      <tr><th>Model</th><th>Field</th><th>gpt-4o-mini</th><th>gpt-5.4-mini</th><th></th></tr>
    </thead>
    <tbody>
      <tr>
        <td class="model-id">o3</td>
        <td><span class="field-tag">strengths</span></td>
        <td class="val-old">"Excels in technical writing and instruction-following"</td>
        <td class="val-new">"Strong multi-step reasoning on complex tasks" · "Solving math and science problems"</td>
        <td><span class="verdict-badge badge-fixed">Fixed</span></td>
      </tr>
      <tr>
        <td class="model-id">gpt-4o-mini</td>
        <td><span class="field-tag">description</span><br><span class="field-tag">capabilities</span></td>
        <td class="val-old">"a fine-tuned version of the GPT-4o model" · caps: [fine_tuning]</td>
        <td class="val-new">Correct: separate smaller model · caps: [multilingual, function_calling, structured_output]</td>
        <td><span class="verdict-badge badge-fixed">Fixed</span></td>
      </tr>
      <tr>
        <td class="model-id">claude-sonnet-4-6<br>claude-haiku-4-5</td>
        <td><span class="field-tag">capabilities</span></td>
        <td class="val-old">[reasoning] only</td>
        <td class="val-new">[reasoning, multilingual] + image support detected from input_modalities</td>
        <td><span class="verdict-badge badge-fixed">Fixed</span></td>
      </tr>
      <tr>
        <td class="model-id">command-a-03-2025<br>command-r7b-12-2024</td>
        <td><span class="field-tag">capabilities</span><br><span class="field-tag">strengths</span></td>
        <td class="val-old">caps: [reasoning] · strengths generic (conversational responses)</td>
        <td class="val-new">caps: [function_calling, structured_output, multilingual] · strengths: tool use, RAG, 256K context</td>
        <td><span class="verdict-badge badge-fixed">Fixed</span></td>
      </tr>
      <tr>
        <td class="model-id">mistral-large-2512</td>
        <td><span class="field-tag">capabilities</span><br><span class="field-tag">use_cases</span></td>
        <td class="val-old">caps: [function_calling, structured_output, code] · use cases: chatbot, content generation</td>
        <td class="val-new">caps: adds moe, multilingual · use cases: long-context docs, tool use, code (more specific and accurate)</td>
        <td><span class="verdict-badge badge-improved">Improved</span></td>
      </tr>
      <tr>
        <td class="model-id">deepseek-chat<br>deepseek-reasoner<br>gemini-3.1-pro</td>
        <td><span class="field-tag">strengths</span><br><span class="field-tag">use_cases</span></td>
        <td class="val-old">Generic phrasing, some marketing copy</td>
        <td class="val-new">More concrete and specific: actual use cases, no change in factual accuracy</td>
        <td><span class="verdict-badge badge-improved">Improved</span></td>
      </tr>
    </tbody>
  </table>
</div>

<!-- Why -->
<div>
  <div class="section-label">Why gpt-5.4-mini does better</div>
  <div class="why-grid">
    <div class="why-card green">
      <div class="why-title">Better knowledge of the model taxonomy</div>
      gpt-4o-mini was confused about newer models from its own family (described gpt-4o-mini as a fine-tune,
      missed function_calling on command models). gpt-5.4-mini has more reliable internal knowledge about which
      models support which features, with fewer gaps in capabilities and fewer wrong descriptions.
    </div>
    <div class="why-card green">
      <div class="why-title">Less likely to copy generic text</div>
      gpt-4o-mini often applied the same strengths template across model families ("versatile in handling both text and image inputs")
      regardless of what made each model distinctive. gpt-5.4-mini produces more specific, differentiated content per model.
    </div>
  </div>
</div>

</body></html>
"""

st.title("✨ Enrich Agent")
st.divider()

st.subheader("Agent flow")
st.html(FLOW_HTML)
st.divider()
st.subheader("Coverage: before vs after enrichment")
st.html(COVERAGE_HTML)
st.divider()
st.subheader("Accuracy: sampling analysis")
st.html(ACCURACY_HTML)
st.divider()
st.subheader("Before / after examples")
st.html(EXAMPLES_HTML)
