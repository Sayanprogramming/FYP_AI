import streamlit as st
import pandas as pd
from pathlib import Path


DATA_PATH = Path("utils/messages.csv")


def save_message(name, email, message):
    row = {"name": name, "email": email, "message": message}
    if DATA_PATH.exists():
        df = pd.read_csv(DATA_PATH)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])

    df.to_csv(DATA_PATH, index=False)

    # clear form fields
    st.session_state['contact_form'] = {
        'name': '',
        'email': '',
        'message': ''
    }



def show():
    if 'contact_form' not in st.session_state:
        st.session_state['contact_form'] = {
            'name': '',
            'email': '',
            'message': ''
        }

    st.header("Contact Us")
    st.write("Reach out for feedback, collaborations or support.")

    # 🔹 Changed form key to avoid conflict
    with st.form(key='contact_form_ui'):
        name = st.text_input("Your Name", value=st.session_state['contact_form'].get('name', ''))
        email = st.text_input("Your Email", value=st.session_state['contact_form'].get('email', ''))
        message = st.text_area("Your Message", value=st.session_state['contact_form'].get('message', ''))
        submit = st.form_submit_button("Send")

        if submit:
            save_message(name, email, message)
            st.success(f"Thanks {name}, we received your message!")
            st.toast("Messages are saved to messages.csv (for dev/demo).")

    st.markdown("---")
    st.markdown("# 📍 Location")
    st.info("Find us at: 123 Mediwise Lane, Health City, HC 12345")

    data = pd.DataFrame({'lat': [22.61888108086453], 'lon': [88.40462144986203]})
    col1, col2, col3 = st.columns([1, 10, 1])
    with col2:
        st.markdown("### 📍 Our location")
        st.map(data)
