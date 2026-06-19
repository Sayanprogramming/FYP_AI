import streamlit as st
import pandas as pd
from controllers import heart_services
from llm_model import model_service
from utils.prescription_service import send_prescription_email, generate_pdf_bytes



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

                # Store results in session state so prescription section can access them
                st.session_state["heart_result"] = {
                    "name": name,
                    "age": age,
                    "prediction": response[0],
                    "probability": response[1],
                    "format_prompt": format_prompt,
                    "model_res": model_res,
                }

            st.toast("Prediction completed!")

    # ── Show results from session state (persists after download_button re-run) ──
    if "heart_result" in st.session_state and "prediction" in st.session_state["heart_result"]:
        res_display = st.session_state["heart_result"]
        prob = res_display["probability"]
        pred = res_display["prediction"]
        if pred == 1:
            st.error(f"High risk of heart disease detected! (Probability: {prob * 100:.2f}%)")
        else:
            st.success(f"Low risk of heart disease detected. (Probability: {prob * 100:.2f}%)")
        st.markdown("### 🧑‍⚕️ Model Response")
        st.write(res_display["model_res"])

    # ── Prescription Section (shown after prediction) ──────────────────────────
    if "heart_result" in st.session_state:
        res = st.session_state["heart_result"]

        st.markdown("---")
        st.markdown("### 📋 Prescription Actions")

        col_dl, col_mail = st.columns(2)

        # ── Download Button ──────────────────────────────────────────────────
        with col_dl:
            pdf_bytes = generate_pdf_bytes(
                patient_name=res["name"],
                age=res["age"],
                disease="Heart Disease",
                prediction_summary=res["format_prompt"],
                prescription_text=res["model_res"],
            )
            st.download_button(
                label="⬇️ Download Prescription PDF",
                data=pdf_bytes,
                file_name=f"Prescription_HeartDisease_{res['name'].replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="heart_download_btn",
            )

        # ── Email Button ─────────────────────────────────────────────────────
        with col_mail:
            if st.button("📩 Send to Email", use_container_width=True, key="heart_email_btn"):
                st.session_state["heart_show_email_form"] = True

        if st.session_state.get("heart_show_email_form"):
            with st.form("heart_email_form"):
                user_email = st.text_input(
                    "Patient's Email Address",
                    placeholder="example@gmail.com",
                    key="heart_email_input",
                )
                send_btn = st.form_submit_button("🚀 Send PDF Now")

                if send_btn:
                    if user_email:
                        with st.spinner("Generating PDF and sending email..."):
                            try:
                                send_prescription_email(
                                    recipient_email=user_email,
                                    patient_name=res["name"],
                                    age=res["age"],
                                    disease="Heart Disease",
                                    prediction_summary=res["format_prompt"],
                                    prescription_text=res["model_res"],
                                )
                                st.success(f"✅ Prescription sent successfully to **{user_email}**!")
                                st.session_state["heart_show_email_form"] = False
                            except Exception as e:
                                st.error(f"❌ Failed to send email: {e}")
                    else:
                        st.warning("⚠️ Please enter a valid email address.")
