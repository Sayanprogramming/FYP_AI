import streamlit as st

def apply_style():

    st.markdown('''
    <style>
        # style for team card boxes
                .card {
                    border-radius: 10px;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
                    margin-bottom: 10px;
                }
                .center {
                    text-align: center;
                }

                /* reduce top padding of the page */
                .css-18e3th9 { padding-top: 0rem; }
    </style>
    ''',
    unsafe_allow_html=True)