import streamlit as st
import os

def show():
    # ── Styling and Theme ───────────────────────────────────────────────────
    st.markdown("""
    <style>
    /* Metric Card Styling */
    .metric-container {
        display: flex;
        gap: 16px;
        margin-bottom: 24px;
        flex-wrap: wrap;
    }
    .metric-box {
        flex: 1;
        min-width: 180px;
        background: linear-gradient(135deg, #16213e 0%, #0f3460 100%);
        border: 1px solid rgba(99, 179, 237, 0.2);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
    }
    .metric-value {
        font-size: 36px;
        font-weight: 800;
        background: linear-gradient(135deg, #63b3ed, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.1;
        margin-bottom: 4px;
    }
    .metric-title {
        font-size: 13px;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Code and Info Cards */
    .info-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
    }
    .info-header {
        font-size: 18px;
        font-weight: 700;
        color: #63b3ed;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Tables and results */
    .matrix-table {
        width: 100%;
        border-collapse: collapse;
        margin: 16px 0;
        font-size: 14px;
    }
    .matrix-table th, .matrix-table td {
        border: 1px solid rgba(255,255,255,0.1);
        padding: 12px;
        text-align: center;
    }
    .matrix-table th {
        background-color: rgba(99, 179, 237, 0.1);
        color: #63b3ed;
        font-weight: 700;
    }
    .matrix-cell-green {
        background-color: rgba(72, 187, 120, 0.15);
        color: #48bb78;
        font-weight: bold;
    }
    .matrix-cell-red {
        background-color: rgba(245, 101, 101, 0.15);
        color: #f56565;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Header ──────────────────────────────────────────────────────────────
    st.markdown("<h2 style='text-align:center;'>📊 Model Performance & Analysis</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center; color:#94a3b8; max-width:800px; margin: 0 auto 30px auto;'>"
        "Deep-dive into our production ML models — from raw performance metrics to architectural decisions."
        "</p>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ── Two Main Tabs ────────────────────────────────────────────────────────
    tab_results, tab_overview = st.tabs(["📈 Model Results", "📘 Model Overview"])

    with tab_results:
        st.markdown("## 📈 Model Results")

    with tab_overview:
        st.markdown("## 📘 Model Overview")
