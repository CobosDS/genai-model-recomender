"""
Discovery Agent page — flow diagram + latest report.
"""
import streamlit as st

st.set_page_config(page_title="Discovery Agent", page_icon="🔭", layout="wide")

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

.flow { display: flex; flex-direction: column; align-items: center; width: 100%; max-width: 680px; gap: 0; }

.node {
  width: 100%; background: #181825;
  border: 1px solid #313244; border-radius: 12px;
  padding: 0.9rem 1.2rem;
}
.node-title { font-size: 0.82rem; font-weight: 700; color: #cdd6f4; margin-bottom: 0.25rem; }
.node-desc  { font-size: 0.73rem; color: #6c7086; line-height: 1.5; }
.node.blue   { border-top: 3px solid #89b4fa; }
.node.yellow { border-top: 3px solid #f9e2af; }
.node.green  { border-top: 3px solid #a6e3a1; }
.node.pink   { border-top: 3px solid #f38ba8; }
.node.mauve  { border-top: 3px solid #cba6f7; }
.node.teal   { border-top: 3px solid #94e2d5; }

.arrow { color: #45475a; font-size: 1.3rem; text-align: center; line-height: 1; padding: 4px 0; }
.arrow-sm { color: #45475a; font-size: 1rem; text-align: center; line-height: 1; padding: 2px 0; }

/* ── Two-column check ── */
.check-row { display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem; width: 100%; }
.check-box {
  background: #181825; border: 1px solid #313244; border-radius: 10px;
  padding: 0.7rem 0.9rem;
}
.check-box .title { font-size: 0.75rem; font-weight: 700; color: #cdd6f4; margin-bottom: 0.3rem; }
.check-box .desc  { font-size: 0.68rem; color: #6c7086; line-height: 1.5; }
.check-box.yellow { border-top: 3px solid #f9e2af; }
.check-box.mauve  { border-top: 3px solid #cba6f7; }

/* ── Output chips ── */
.output-row { display: flex; gap: 0.6rem; margin-top: 0.5rem; flex-wrap: wrap; }
.output-chip {
  flex: 1; min-width: 140px;
  background: #1e1e2e; border-radius: 8px;
  padding: 0.45rem 0.7rem; font-size: 0.72rem;
}
.output-chip.green  { border: 1px solid #a6e3a1; }
.output-chip.red    { border: 1px solid #f38ba8; }
.output-chip .label { font-weight: 700; margin-bottom: 0.2rem; font-size: 0.68rem; }
.output-chip.green .label { color: #a6e3a1; }
.output-chip.red   .label { color: #f38ba8; }
.output-chip .val   { color: #6c7086; font-size: 0.67rem; }
</style>
</head>
<body>
<div class="flow">

  <!-- 1. TRIGGER -->
  <div class="node blue">
    <div class="node-title">⏰ Runs once a day per provider</div>
    <div class="node-desc">The agent checks each of the 8 providers (Anthropic, OpenAI, Google, Mistral, Cohere, DeepSeek, Meta, xAI) against what was last extracted.</div>
  </div>
  <div class="arrow">↓</div>

  <!-- 2. FETCH -->
  <div class="node yellow">
    <div class="node-title">🌐 Fetches the current docs page</div>
    <div class="node-desc">Downloads the provider's model listing page as clean text using Jina Reader, the same source the extractors use.</div>
  </div>
  <div class="arrow">↓</div>

  <!-- 3. TWO CHECKS -->
  <div class="check-row">
    <div class="check-box yellow">
      <div class="title">🏗️ Structural check</div>
      <div class="desc">
        Looks for key markers in the page: known model names, price headers, section titles.
        If they disappear, the page layout changed and the extractor regex will likely break.
        Also flags if the page shrank or grew by more than 40%.
      </div>
    </div>
    <div class="check-box mauve">
      <div class="title">🤖 New model detection</div>
      <div class="desc">
        Passes the page to an LLM and asks it to list every model ID it can find.
        Compares that list against the last raw extraction.
        Anything not seen before is flagged as a new model.
      </div>
    </div>
  </div>
  <div class="arrow">↓</div>

  <!-- 4. OUTPUT -->
  <div class="node green">
    <div class="node-title">📋 Report saved</div>
    <div class="node-desc">Results written to <code>data/discovery/YYYY-MM-DD.json</code>. One entry per provider.</div>
    <div class="output-row">
      <div class="output-chip green">
        <div class="label">New models</div>
        <div class="val">IDs found on the page that weren't in the last extraction</div>
      </div>
      <div class="output-chip red">
        <div class="label">Structural issues</div>
        <div class="val">Missing markers or significant page size change</div>
      </div>
    </div>
  </div>
  <div class="arrow">↓</div>

  <!-- 5. ACTION -->
  <div class="node teal">
    <div class="node-title">📬 Results available for review</div>
    <div class="node-desc">The report flags what changed. A human decides whether to re-run the full pipeline for that provider to ingest the new models.</div>
  </div>

</div>
</body></html>
"""

st.title("🔭 Discovery Agent")
st.divider()

st.subheader("Agent flow")
st.html(FLOW_HTML)
