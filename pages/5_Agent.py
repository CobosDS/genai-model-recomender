"""
Chat Agent flow page.
"""
import streamlit as st

st.set_page_config(page_title="Chat Agent", page_icon="🤖", layout="wide")

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

.flow { display: flex; flex-direction: column; align-items: center; width: 100%; max-width: 700px; gap: 0; }

.node {
  width: 100%; background: #181825;
  border: 1px solid #313244; border-radius: 12px;
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
.node.teal   { border-top: 3px solid #94e2d5; }

.arrow { color: #45475a; font-size: 1.3rem; text-align: center; line-height: 1; padding: 4px 0; }
.arrow-sm { color: #45475a; font-size: 1rem; text-align: center; padding: 2px 0; }

/* ── Loop badge ── */
.loop-badge {
  align-self: flex-end; margin-right: 0;
  font-size: 0.62rem; font-weight: 700; letter-spacing: .05em;
  color: #cba6f7; border: 1px dashed #cba6f7;
  border-radius: 99px; padding: 2px 9px;
}

/* ── Tool row ── */
.tool-row {
  display: flex; gap: 0.6rem; margin-top: 0.5rem; flex-wrap: wrap;
}
.tool-chip {
  background: #1e1e2e; border: 1px solid #fab387;
  border-radius: 8px; padding: 0.3rem 0.7rem;
  font-size: 0.7rem; color: #fab387; font-family: monospace;
}

/* ── Decision ── */
.decision-wrap { display: flex; flex-direction: column; align-items: center; width: 100%; }
.diamond {
  background: #181825; border: 1px solid #fab387;
  border-radius: 8px; padding: 0.5rem 1.4rem;
  font-size: 0.75rem; font-weight: 700; color: #fab387;
}
.branch-row {
  display: flex; justify-content: center; align-items: flex-start;
  gap: 5rem; width: 100%; margin: 0;
}
.branch { display: flex; flex-direction: column; align-items: center; gap: 0; }
.branch-label { font-size: 0.68rem; color: #6c7086; margin: 4px 0; }
.branch-node {
  background: #181825; border: 1px solid #313244; border-radius: 10px;
  padding: 0.6rem 0.9rem; font-size: 0.73rem; min-width: 150px; text-align: center;
}

/* ── Output row ── */
.output-row { display: flex; gap: 0.6rem; margin-top: 0.5rem; flex-wrap: wrap; }
.output-chip {
  flex: 1; min-width: 140px;
  background: #1e1e2e; border: 1px solid #a6e3a1;
  border-radius: 8px; padding: 0.45rem 0.7rem;
  font-size: 0.72rem;
}
.output-chip .label { color: #a6e3a1; font-weight: 700; margin-bottom: 0.2rem; font-size: 0.68rem; }
.output-chip .val   { color: #6c7086; font-family: monospace; font-size: 0.67rem; }

/* ── Back arrow ── */
.back-arrow {
  align-self: flex-end;
  font-size: 0.65rem; color: #cba6f7;
  display: flex; align-items: center; gap: 0.3rem;
  margin: 2px 0;
}
</style>
</head>
<body>
<div class="flow">

  <!-- 1. USER INPUT -->
  <div class="node blue">
    <div class="node-title">💬 You describe what you need</div>
    <div class="node-desc">You type your project, requirements, or budget in the chat. The conversation history is kept so the AI remembers what was said before.</div>
  </div>
  <div class="arrow">↓</div>

  <!-- 2. SYSTEM PROMPT + HISTORY -->
  <div class="node mauve">
    <div class="node-title">📋 The AI is given its role and the full conversation</div>
    <div class="node-desc">Before answering, the AI receives a set of instructions that define how to behave: ask for clarification if something is missing, never invent models, always recommend from the database.</div>
  </div>
  <div class="arrow">↓</div>

  <!-- 3. LLM CALL -->
  <div class="node pink">
    <div class="node-title">🤖 The AI reads your message and decides what to do</div>
    <div class="node-desc">It either asks you a clarifying question, or decides it has enough information to search the database for matching models.</div>
  </div>
  <div class="arrow">↓</div>

  <!-- 4. DECISION -->
  <div class="decision-wrap">
    <div class="diamond">does it need to search?</div>
    <div class="branch-row">

      <div class="branch">
        <span class="branch-label">yes</span>
        <div class="arrow-sm">↓</div>
        <div class="branch-node" style="border-color:#fab387; color:#cdd6f4;">
          <div style="font-size:0.72rem;font-weight:700;margin-bottom:0.3rem;color:#fab387">🔧 Queries the database</div>
          <div class="tool-row" style="justify-content:center">
            <span class="tool-chip">Search by filters</span>
            <span class="tool-chip">Get model details</span>
            <span class="tool-chip">Compare models</span>
            <span class="tool-chip">List providers</span>
          </div>
        </div>
        <div class="arrow-sm">↓</div>
        <div class="branch-node" style="border-color:#94e2d5;color:#94e2d5;">
          🗄️ Looks up models, pricing and benchmarks
        </div>
        <div class="arrow-sm">↓</div>
        <div class="branch-node" style="border-color:#cba6f7;color:#cba6f7;">↩ Results sent back to the AI</div>
      </div>

      <div class="branch">
        <span class="branch-label">no</span>
        <div class="arrow-sm">↓</div>
        <div class="branch-node" style="color:#a6e3a1;border-color:#a6e3a1;">
          ✅ Ready to answer
        </div>
      </div>

    </div>
  </div>
  <div class="arrow">↓</div>

  <!-- 5. STREAM -->
  <div class="node yellow">
    <div class="node-title">⚡ The AI writes its recommendation</div>
    <div class="node-desc">The answer appears word by word as it's generated, so you don't have to wait for the full response before starting to read.</div>
  </div>
  <div class="arrow">↓</div>

  <!-- 6. OUTPUT -->
  <div class="node green">
    <div class="node-title">🖥️ Results shown on screen</div>
    <div class="node-desc">Two things appear together:</div>
    <div class="output-row">
      <div class="output-chip">
        <div class="label">Model cards</div>
        <div class="val">Visual summary of the top matches with price, context and capabilities</div>
      </div>
      <div class="output-chip">
        <div class="label">Explanation</div>
        <div class="val">Why each model fits your needs and what trade-offs to consider</div>
      </div>
    </div>
  </div>

</div>
</body></html>
"""

st.title("💬 Chat Agent")
st.divider()
st.html(FLOW_HTML)
