# views/services.py
import streamlit as st

def simple_rule_predict(symptoms, severity):

    s = set(symptoms)

    if {"fever", "cough"}.issubset(s):
        return "Possible: Flu/COVID-like illness — consult a physician."
    if "shortness of breath" in s:
        return "Urgent: Shortness of breath flagged — seek immediate care!"
    if "headache" in s and len(s) == 1:
        return "Possible: Tension/migraine — monitor and consult if persists."
    if len(s) == 0:
        return "Please select symptoms so the model can suggest next steps."
    
    return "General Advice: Monitor symptoms, rest, hydrate, consult a doctor if it worsens."





def show():
    st.header("Our Services")
    st.markdown("""
    ### 🔍 Symptom Checker
    Enter your symptoms and get smart AI-based predictions (demo).
    """)
    with st.form("symptom_form"):
        symptoms = st.multiselect(
            "Select symptoms (demo)",
            ["fever", "cough", "headache", "fatigue", "sore throat", "runny nose", "shortness of breath"]
        )
        severity = st.slider("Overall severity (1-10)", 1, 10, 3)
        submitted = st.form_submit_button("Predict")
        if submitted:
            prediction = simple_rule_predict(symptoms, severity)

            st.warning(prediction)
            st.write(f"Symptoms: {symptoms} — Severity {severity}")


    st.markdown("### 📅 Appointment Scheduling\nSeamless booking (placeholder).")
    st.markdown("### 📂 Health Record Management\nSecure storage and retrieval (placeholder).")
    st.success("More production-ready features coming soon (model integration, db, auth).")
