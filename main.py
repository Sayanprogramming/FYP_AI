# main.py
import streamlit as st
from views import utils, home, services, about, contact, footer


NAV_OPTS = ["🏠 Home", "🧪 Services", "📖 About", "📞 Contact"]


def sync_from_slider():
    """Update sidebar selection when slider changes."""
    st.session_state.side_page = st.session_state.page_slider

def sync_from_sidebar():
    """Update slider selection when sidebar changes."""
    st.session_state.page_slider = st.session_state.side_page



if __name__ == "__main__":

    # ---- Page configuration ----
    st.set_page_config(
        page_title="Mediwise",
        page_icon="🩺",
        layout="wide",
        initial_sidebar_state="expanded"
    )

   
    utils.apply_style()

    
    if "page_slider" not in st.session_state:
        st.session_state.page_slider = NAV_OPTS[0]
    if "side_page" not in st.session_state:
        st.session_state.side_page = NAV_OPTS[0]

    # title
    st.markdown(
        "<h1 style='text-align:center;'>🩺 Mediwise</h1>",
        unsafe_allow_html=True
    )

    
    st.select_slider(
        "Navigate",
        options=NAV_OPTS,
        key="page_slider",
        on_change=sync_from_slider
    )

    
    with st.sidebar:
        st.markdown(
            "<h2 style='text-align:center; border-bottom: 1px solid #fff;'>"
            "Mediwise Healthcare App</h2>",
            unsafe_allow_html=True
        )
        st.radio(
            "Go to",
            options=NAV_OPTS,
            index=NAV_OPTS.index(st.session_state.page_slider),
            key="side_page",
            on_change=sync_from_sidebar
        )

    # Page routing 
    current_page = st.session_state.page_slider

    if current_page == "🏠 Home":
        home.show()
    elif current_page == "🧪 Services":
        services.show()
    elif current_page == "📖 About":
        about.show()
    elif current_page == "📞 Contact":
        contact.show()
    else:
        st.error("Page not found.")


    # ---- Footer ----
    footer.show()
    