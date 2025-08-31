import streamlit as st
import pandas as pd
from controllers import diabetes_services
from llm_model import model_service


def show_ui():
    st.markdown("## 🩺 Diabetes Prediction")
    st.markdown("Enter your health details below to predict the risk of diabetes:")

    # Input fields for user data
    with st.form("diabetes form"):

        
        st.markdown("<div style='color: #ff6f91; font-weight: bold; font-size:3rem'>Patient Information</div>", unsafe_allow_html=True)
        st.markdown("<div style='color: dodgerblue; font-weight: bold; padding-bottom: 3px;'>Enter Patient Details</div>", unsafe_allow_html=True)
        st.markdown("<hr style='height: 1px; border: none; background-color: dodgerblue; padding: 0; margin-top: 10px' />", unsafe_allow_html=True)


        name = st.text_input("Name *", max_chars=100, placeholder="Enter patient name")

        age = st.number_input("Age *", min_value=1, max_value=110, value=21)

        gender = st.selectbox("Gender *", options=["Male", "Female", "Other"])

        pregnancies = st.number_input("Pregnancies *", min_value=0, max_value=17, value=0)

        glucose = st.number_input("Glucose *", min_value=0.0, max_value=199.0, value=120.0)

        blood_pressure = st.number_input("Blood Pressure *", min_value=0.0, max_value=122.0, value=68.0)

        skin_thickness = st.number_input("Skin Thickness [If unknown keep unchange default value]", min_value=0.0, max_value=100.0, value=20.536458)

        insulin = st.number_input("Insulin [If unknown keep unchange default value]", min_value=0.0, max_value=850.0, value=79.799479)

        bmi = st.number_input("BMI *", min_value=0.0, max_value=70.0, value=32.5)

        # additional information of what patient is feeling
        symptoms = st.text_area("Symptoms", placeholder="Describe symptoms here...", key="symptoms")


        submit_button = st.form_submit_button("Submit Patient Info")

    # now if submitted
        if submit_button:

            st.toast("Patient information submitted successfully!")

            if not name and not symptoms:
                st.toast("Please fill all (*) the fields carefully.")
                return


            with st.spinner("Predicting diabetes risk..."):

                inp_dict = {
                    "Pregnancies": pregnancies,
                    "Glucose": glucose,
                    "BloodPressure": blood_pressure,
                    "SkinThickness": skin_thickness,
                    "Insulin": insulin,
                    "BMI": bmi,
                    "Age": age
                }

                user_input_df = pd.DataFrame([inp_dict])

                response = diabetes_services.predict_disease(user_input_df)
                
                format_prompt = f"The patient has a {'high' if response[0] == 1 else 'low'} risk of diabetes with a probability of {response[1]:.2f}."
                model_res = model_service.ask_model(name, age, "diabetes", format_prompt, symptoms)


            prediction, probability = response

            if prediction == 1:
                st.error(f"High risk of diabetes detected! (Probability: {probability:.2f})")
            else:
                st.success(f"Low risk of diabetes detected. (Probability: {probability:.2f})")

            st.toast("Prediction completed!")


            st.markdown("### 🩺 Model Response")
            st.write(model_res)