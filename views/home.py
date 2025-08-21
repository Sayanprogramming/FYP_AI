import streamlit as st
import pandas as pd

def show():
    st.title("Hello, Welcome to Mediwise 👨‍⚕️")
    st.subheader("Your Intelligent Healthcare Companion")
    st.write("We provide smart and reliable tools to assist medical professionals and patients alike.")

    st.markdown("""
    #### Features:
    - Symptom Checker
    - Appointment Scheduling
    - Patient History Dashboard
    - AI-powered Health Predictions
    """)
    st.success("Explore from the navigation slider / sidebar to learn more.")

