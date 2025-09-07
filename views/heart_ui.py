import streamlit as st
import pandas as pd
from controllers import heart_services
from llm_model import model_service


def show_ui():
    st.markdown("## ❤️ Heart Disease Prediction")
    st.markdown("Enter your health details below to predict the risk of heart disease:")

    # Input fields for user data
    with st.form("heart disease form"):

        st.markdown(
            "<div style='color: red; font-weight: bold; font-size:3rem'>Patient Information</div>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<div style='color: darkgreen; font-weight: bold; padding-bottom: 3px;'>Enter Patient Details</div>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<hr style='height: 2px; border: none; background-color: gray; padding: 0; margin-top: 10px' />",
            unsafe_allow_html=True
        )

        # Patient identity
        name = st.text_input("Name *", max_chars=100, placeholder="Enter patient name")
        age = st.number_input("Age *", min_value=1, max_value=110, value=40)
        gender = st.selectbox("Gender *", options=["Male", "Female", "Other"])

        # Lifestyle and health inputs
        smoking = st.selectbox("Smoking *", options=["No", "Yes"], help="Select if patient smokes")
        alcohol = st.selectbox("Alcohol *", options=["No", "Yes"], help="Select if patient drinks alcohol")
        exercise = st.slider("Exercise {per week-(Rate-0 - 10)} *", min_value=0, max_value=10, value=3)
        diet_quality = st.slider("Diet Quality *", min_value=1, max_value=10, value=5)
        overweight = st.selectbox("Overweight *", options=["No", "Yes"], help="Is patient overweight?")
        stress_level = st.slider("Stress Level *", min_value=1, max_value=10, value=5)

        blood_pressure = st.number_input("Blood Pressure *", min_value=50, max_value=200, value=120)
        cholesterol = st.number_input("Cholesterol *", min_value=100, max_value=400, value=200)

        family_history = st.selectbox("Family History of Heart Disease *", options=["No", "Yes"])
        chest_pain = st.selectbox("Chest Pain *", options=["No", "Yes"])
        shortness_of_breath = st.selectbox("Shortness of Breath *", options=["No", "Yes"])
        diabetes = st.selectbox("Diabetes *", options=["No", "Yes"])

        # Additional information
        symptoms = st.text_area("Symptoms", placeholder="Describe symptoms here...", key="heart_symptoms")

        # Submit button
        submit_button = st.form_submit_button("Submit Patient Info")

        if submit_button:
            st.toast("Patient information submitted successfully!")

            if not name and not symptoms:
                st.toast("Please fill all (*) the fields carefully.")
                return

            with st.spinner("Predicting heart disease risk..."):

                inp_dict = {
                    "Age": age,
                    "Gender": 1 if gender == "Male" else (0 if gender == "Female" else 2),
                    "Smoking": 1 if smoking == "Yes" else 0,
                    "Alcohol": 1 if alcohol == "Yes" else 0,
                    "Exercise (per week)": exercise,  # 👈 use model’s expected column name
                    "Diet Quality": diet_quality,
                    "Overweight": 1 if overweight == "Yes" else 0,
                    "Stress Level": stress_level,
                    "Blood Pressure": blood_pressure,
                    "Cholesterol": cholesterol,
                    "Family History": 1 if family_history == "Yes" else 0,
                    "Chest Pain": 1 if chest_pain == "Yes" else 0,
                    "Shortness of Breath": 1 if shortness_of_breath == "Yes" else 0,
                    "Diabetes": 1 if diabetes == "Yes" else 0
                }

                user_input_df = pd.DataFrame([inp_dict])
                response = heart_services.predict_disease(user_input_df)

                format_prompt = (
                    f"The patient has a {'high' if response[0] == 1 else 'low'} "
                    f"risk of heart disease with a probability of {response[1]:.2f}."
                )
                model_res = model_service.ask_model(name, age, "heart disease", format_prompt, symptoms)

            # Display prediction
            prediction, probability = response

            if prediction == 1:
                st.error(f"High risk of heart disease detected! (Probability: {probability * 100:.2f}%)")
            else:
                st.success(f"Low risk of heart disease detected. (Probability: {probability * 100:.2f}%)")

            st.toast("Prediction completed!")

            st.markdown("### 🧑‍⚕️ Model Response")
            st.write(model_res)
