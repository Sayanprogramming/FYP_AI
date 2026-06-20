import streamlit as st
import pandas as pd
from controllers import diabetes_services
from llm_model import model_service
from utils.prescription_service import send_prescription_email, generate_pdf_bytes


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
                
                format_prompt = f"The patient has a {'high' if response[0] == 1 else 'low'} risk of diabetes with a probability of {response[1]:.2%}."
                model_res = model_service.ask_model(name, age, "diabetes", format_prompt, symptoms)

                # Store results in session state so prescription section can access them
                st.session_state["diabetes_result"] = {
                    "name": name,
                    "age": age,
                    "prediction": response[0],
                    "probability": response[1],
                    "format_prompt": format_prompt,
                    "model_res": model_res,
                }

            st.toast("Prediction completed!")

    # ── Show results from session state (persists after download_button re-run) ──
    if "diabetes_result" in st.session_state and "prediction" in st.session_state["diabetes_result"]:
        res_display = st.session_state["diabetes_result"]
        prob = res_display["probability"]
        pred = res_display["prediction"]
        
        if pred == 1:
            st.error("High risk of diabetes detected!")
        else:
            st.success("Low risk of diabetes detected.")
            
        # Statistical Risk Assessment UI
        st.markdown("### 📊 Risk Assessment")
        
        disease_prob = prob
        if disease_prob > 0.7:
            risk_level = "High Risk"
            color = "#ef4444"  # red
        elif disease_prob > 0.4:
            risk_level = "Moderate Risk"
            color = "#f59e0b"  # orange
        else:
            risk_level = "Low Risk"
            color = "#10b981"  # green
            
        st.markdown(f"""
        <div style="background-color: #1e1e1e; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid {color};">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <span style="font-size: 18px; font-weight: bold; color: white;">Disease Probability</span>
                <span style="font-size: 24px; font-weight: bold; color: {color};">{disease_prob * 100:.1f}% ({risk_level})</span>
            </div>
            <div style="width: 100%; background-color: #333; border-radius: 5px; height: 12px;">
                <div style="width: {disease_prob * 100}%; background-color: {color}; height: 12px; border-radius: 5px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🩺 Model Response")
        st.write(res_display["model_res"])

    # ── Prescription Section (shown after prediction) ──────────────────────────
    if "diabetes_result" in st.session_state:
        res = st.session_state["diabetes_result"]

        st.markdown("---")
        st.markdown("### 📋 Prescription Actions")

        col_dl, col_mail = st.columns(2)

        # ── Download Button ──────────────────────────────────────────────────
        with col_dl:
            pdf_bytes = generate_pdf_bytes(
                patient_name=res["name"],
                age=res["age"],
                disease="Diabetes",
                prediction_summary=res["format_prompt"],
                prescription_text=res["model_res"],
            )
            st.download_button(
                label="⬇️ Download Prescription PDF",
                data=pdf_bytes,
                file_name=f"Prescription_Diabetes_{res['name'].replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="diabetes_download_btn",
            )

        # ── Email Button ─────────────────────────────────────────────────────
        with col_mail:
            if st.button("📩 Send to Email", use_container_width=True, key="diabetes_email_btn"):
                st.session_state["diabetes_show_email_form"] = True

        if st.session_state.get("diabetes_show_email_form"):
            with st.form("diabetes_email_form"):
                user_email = st.text_input(
                    "Patient's Email Address",
                    placeholder="example@gmail.com",
                    key="diabetes_email_input",
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
                                    disease="Diabetes",
                                    prediction_summary=res["format_prompt"],
                                    prescription_text=res["model_res"],
                                )
                                st.success(f"✅ Prescription sent successfully to **{user_email}**!")
                                st.session_state["diabetes_show_email_form"] = False
                            except Exception as e:
                                st.error(f"❌ Failed to send email: {e}")
                    else:
                        st.warning("⚠️ Please enter a valid email address.")