# main.py
import streamlit as st
from views import utils, home, services, analysis, contribution, footer

NAV_OPTS = ["🏠 Dashboard", "🧪 Services", "📊 Analysis", "🤝 Contribute"]

if __name__ == "__main__":
    # ---- Page configuration ----
    st.set_page_config(
        page_title="HealthForge AI",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    utils.apply_style()

    # ---- Sidebar navigation ----
    with st.sidebar:
        st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0d1117 0%, #0f1629 100%);
            border-right: 1px solid rgba(99,179,237,0.12);
        }
        .sidebar-brand {
            text-align: center;
            padding: 16px 0 24px 0;
            border-bottom: 1px solid rgba(99,179,237,0.12);
            margin-bottom: 16px;
        }
        .sidebar-brand .brand-icon { font-size: 36px; }
        .sidebar-brand .brand-name {
            font-size: 20px;
            font-weight: 800;
            background: linear-gradient(135deg, #63b3ed, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 6px 0 2px 0;
        }
        .sidebar-brand .brand-sub {
            font-size: 11px;
            color: #4a5568;
            letter-spacing: 1.5px;
            text-transform: uppercase;
        }
        </style>
        <div class="sidebar-brand">
            <div class="brand-icon">⚡</div>
            <div class="brand-name">HealthForge AI</div>
            <div class="brand-sub">Open Source Health AI</div>
        </div>
        """, unsafe_allow_html=True)
        
        current_page = st.radio(
            "Go to",
            options=NAV_OPTS,
            key="side_page"
        )



    # ---- Page routing ----
    if current_page == "🏠 Dashboard":
        home.show()
        footer.show()
    elif current_page == "🧪 Services":
        services.show()
    elif current_page == "📊 Analysis":
        analysis.show()
        footer.show()
    elif current_page == "🤝 Contribute":
        contribution.show()
        footer.show()
    else:
        st.error("Page not found.")