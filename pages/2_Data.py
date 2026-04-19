"""
Data explorer page — browse the models database.
"""
import json
import os
import sqlite3
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

load_dotenv(override=True)

st.set_page_config(page_title="Data Explorer", page_icon="🗃️", layout="wide")

DB_PATH = Path(os.getenv("DB_PATH", "../llm-etl/data/models.db"))

st.markdown("""
<style>
[data-testid="stSidebarNav"] { display: none; }
[data-testid="stMetricValue"] { font-size: 1.6rem !important; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.page_link("app.py", label="🤖 App", use_container_width=True)
    st.divider()
    st.page_link("pages/1_Pipeline.py", label="🔄 Pipeline", use_container_width=True)
    st.page_link("pages/4_Enrich.py", label="✨ Enrich Agent", use_container_width=True)
    st.page_link("pages/5_Agent.py",     label="💬 Chat Agent",       use_container_width=True)
    st.page_link("pages/6_Discovery.py", label="🔭 Discovery Agent",  use_container_width=True)


@st.cache_data(ttl=300)
def load_data():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    models = conn.execute("""
        SELECT
            m.model_id, m.name, m.provider, m.family, m.model_category,
            m.is_open_source, m.context_window, m.parameter_count_b,
            m.capabilities, m.input_modalities, m.output_modalities,
            m.description,
            p.input_per_1m, p.output_per_1m,
            CASE WHEN b.model_id IS NOT NULL THEN 1 ELSE 0 END as has_benchmarks
        FROM models m
        LEFT JOIN pricing p ON m.model_id = p.model_id
        LEFT JOIN (SELECT DISTINCT model_id FROM benchmark_scores) b ON m.model_id = b.model_id
        ORDER BY m.provider, m.name
    """).fetchall()

    provider_stats = conn.execute("""
        SELECT m.provider,
               COUNT(*) as total,
               SUM(CASE WHEN p.input_per_1m IS NOT NULL THEN 1 ELSE 0 END) as with_price,
               SUM(CASE WHEN b.model_id IS NOT NULL THEN 1 ELSE 0 END) as with_bench,
               SUM(m.is_open_source) as oss
        FROM models m
        LEFT JOIN pricing p ON m.model_id = p.model_id
        LEFT JOIN (SELECT DISTINCT model_id FROM benchmark_scores) b ON m.model_id = b.model_id
        GROUP BY m.provider ORDER BY total DESC
    """).fetchall()

    cap_rows = [r["capabilities"] for r in conn.execute("SELECT capabilities FROM models WHERE capabilities IS NOT NULL").fetchall()]

    conn.close()
    return [dict(r) for r in models], [dict(r) for r in provider_stats], cap_rows


models, provider_stats, cap_rows = load_data()

from collections import Counter
cap_counter = Counter()
for caps_json in cap_rows:
    for c in json.loads(caps_json):
        cap_counter[c] += 1

total = len(models)
with_price = sum(1 for m in models if m["input_per_1m"] is not None)
with_bench = sum(1 for m in models if m["has_benchmarks"])
oss_count = sum(1 for m in models if m["is_open_source"])

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🗃️ Data Explorer")
st.divider()

import pandas as pd

st.divider()

# ── Filters ───────────────────────────────────────────────────────────────────
st.subheader("Model browser")

col1, col2, col3, col4 = st.columns([2, 2, 2, 2])

with col1:
    all_providers = sorted({m["provider"] for m in models if m["provider"]})
    sel_providers = st.multiselect("Provider", all_providers)

with col2:
    all_cats = sorted({m["model_category"] for m in models if m["model_category"]})
    sel_cats = st.multiselect("Category", all_cats)

with col3:
    sel_oss = st.selectbox("Open-source", ["All", "Yes", "No"])

with col4:
    sel_pricing = st.selectbox("Pricing", ["All", "Has pricing", "No pricing"])

# ── Apply filters ─────────────────────────────────────────────────────────────
filtered = models
if sel_providers:
    filtered = [m for m in filtered if m["provider"] in sel_providers]
if sel_cats:
    filtered = [m for m in filtered if m["model_category"] in sel_cats]
if sel_oss == "Yes":
    filtered = [m for m in filtered if m["is_open_source"]]
elif sel_oss == "No":
    filtered = [m for m in filtered if not m["is_open_source"]]
if sel_pricing == "Has pricing":
    filtered = [m for m in filtered if m["input_per_1m"] is not None]
elif sel_pricing == "No pricing":
    filtered = [m for m in filtered if m["input_per_1m"] is None]

st.caption(f"{len(filtered)} models")

# ── Table ─────────────────────────────────────────────────────────────────────
rows = []
for m in filtered:
    caps = json.loads(m["capabilities"] or "[]")
    rows.append({
        "Name": m["name"] or m["model_id"],
        "Provider": m["provider"],
        "Category": m["model_category"],
        "Context": f'{m["context_window"] // 1000}k' if m["context_window"] else "—",
        "Input $/1M": f'${m["input_per_1m"]:.3f}' if m["input_per_1m"] is not None else "—",
        "Output $/1M": f'${m["output_per_1m"]:.3f}' if m["output_per_1m"] is not None else "—",
        "Capabilities": ", ".join(caps),
    })

df = pd.DataFrame(rows)
st.dataframe(df, use_container_width=True, hide_index=True, height=500)
