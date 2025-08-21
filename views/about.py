# views/about.py
import streamlit as st
from views import utils
utils.apply_style()

def show():
    st.header("About Mediwise")

    st.markdown("""
    **Mediwise** is a smart healthcare application aimed at enhancing **accessibility**
    and **efficiency** in healthcare delivery.

    Our platform is designed with **simplicity** and **security** in mind, supporting both **patients** and **practitioners** through:

    - 🤖 **AI-powered diagnostics**
    - 📁 **Medical record management**
    - 📅 **Easy scheduling systems**
    - 📡 **Remote monitoring tools**
    ---
    """)
    st.subheader("🎨 Credits")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='card' style='background-color: #222;'><h5 class='center'>Arijit Chowdhury</h5><p class='center'>Data Scientist</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='card' style='background-color: pink;'><h5 class='center'>Debarati Chaudhuri</h5><p class='center'>UI/UX Designer</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card' style='background-color: navy;'><h5 class='center'>Joymalya Dey</h5><p class='center'>Backend Engineer</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='card' style='background-color: brown;'><h5 class='center'>Sayan Sadhu</h5><p class='center'>AI Developer</p></div>", unsafe_allow_html=True)

    st.markdown("---\n> *Empowering smarter health decisions through technology.*")
