"""Shared UI helpers."""
import streamlit as st


def navbar(current: str) -> None:
    st.markdown("""
    <style>
    [data-testid="stPageLink"] {
        border: 1px solid #313244;
        border-radius: 99px;
        padding: 2px 4px;
        background: #1e1e2e;
    }
    [data-testid="stPageLink"]:hover {
        border-color: #89b4fa;
        background: #1e1e2e;
    }
    [data-testid="stPageLink"] p {
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        color: #a6adc8 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    _, col = st.columns([8, 2])
    with col:
        nav = st.columns(2)
        with nav[0]:
            st.page_link("app.py", label="🤖 App")
        with nav[1]:
            st.page_link("pages/1_Pipeline.py", label="🔄 Pipeline")
