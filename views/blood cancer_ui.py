"""
Blood Cancer Detection — Streamlit UI
=======================================
Provides an image-based prediction interface for detecting
Acute Lymphoblastic Leukemia (ALL) from blood cell microscopy images.
"""

import os
import streamlit as st
from PIL import Image
import io

from controllers import blood_cancer_services
from llm_model import model_service
from utils.prescription_service import send_prescription_email, generate_pdf_bytes

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def show_ui():
    st.markdown("## 🩸 Blood Cancer Detection")
    st.markdown(
        "Upload a microscopic blood cell image to detect **Blood Cancer** "
        "using our ResNet-18 deep learning model."
    )

    # Initialize key counter for resetting file selector and handle custom toasts
    if "blood_cancer_test_selectbox_counter" not in st.session_state:
        st.session_state["blood_cancer_test_selectbox_counter"] = 0

    if st.session_state.get("blood_cancer_success_toast"):
        st.toast(st.session_state.pop("blood_cancer_success_toast"))

    # ── Check model availability ──────────────────────────────────────────
    if not blood_cancer_services.is_model_available():
        st.warning(
            "⚠️ The blood cancer detection model has not been trained yet. "
            "Please run `python models/blood cancer_model/train_model.py` to train the model first."
        )
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e1b4b 0%, #311042 100%);
                    border: 1px solid rgba(167,139,250,0.2); border-radius: 16px;
                    padding: 30px; text-align: center; margin: 20px 0;">
            <div style="font-size: 48px; margin-bottom: 12px;">🔬</div>
            <div style="font-size: 20px; font-weight: 700; color: #e2e8f0; margin-bottom: 8px;">
                Model Training Required
            </div>
            <div style="font-size: 14px; color: #94a3b8; line-height: 1.6;">
                The CNN model needs to be trained on blood cell images before predictions can be made.<br>
                Run the training script with your dataset to generate the model weights.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── Input Form ────────────────────────────────────────────────────────
    with st.form("blood_cancer_form"):
        st.markdown(
            "<div style='color: #f472b6; font-weight: bold; font-size: 2.2rem'>Patient Information</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div style='color: #a78bfa; font-weight: bold; padding-bottom: 3px;'>Enter Patient Details & Upload Cell Image</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<hr style='height: 2px; border: none; background-color: gray; padding: 0; margin-top: 10px' />",
            unsafe_allow_html=True,
        )

        # Patient identity
        name = st.text_input("Name *", max_chars=100, placeholder="Enter patient name")
        age = st.number_input("Age *", min_value=1, max_value=110, value=30)

        # Image selection source (only showing the 8 test samples in test_samples folder)
        selected_test_image = None
        image_bytes = None

        test_samples_dir = os.path.join(BASE_DIR, "models", "blood cancer_model", "test_samples")
        if os.path.exists(test_samples_dir):
            sample_files = [f for f in os.listdir(test_samples_dir) if f.lower().endswith(('.bmp', '.png', '.jpg', '.jpeg'))]
            if sample_files:
                test_selectbox_key = f"blood_cancer_test_selectbox_{st.session_state['blood_cancer_test_selectbox_counter']}"
                selected_test_image = st.selectbox(
                    "🔬 Select from Test Dataset:",
                    options=["-- Select a test image --"] + sorted(sample_files),
                    key=test_selectbox_key
                )
            else:
                st.info("No cell images found in `test_samples` directory.")
        else:
            st.info("Test samples directory `test_samples` not found.")

        # Display preview and load bytes
        if selected_test_image and selected_test_image != "-- Select a test image --":
            sample_path = os.path.join(test_samples_dir, selected_test_image)
            try:
                image_to_analyze = Image.open(sample_path)
                st.image(image_to_analyze, caption=f"Selected Cell Image: {selected_test_image}", width=300)
                with open(sample_path, "rb") as f:
                    image_bytes = f.read()
            except Exception as e:
                st.error(f"Error loading cell image: {e}")

        submit_button = st.form_submit_button("🔬 Analyze Cell Image")

        if submit_button:
            if not name:
                st.toast("⚠️ Please enter the patient's name.")
                return
            if image_bytes is None:
                st.toast("⚠️ Please select a blood cell image.")
                return

            st.toast("Analyzing blood cell image...")

            with st.spinner("Running deep learning inference..."):
                try:
                    predicted_class, confidence = blood_cancer_services.predict_from_image(image_bytes)
                except FileNotFoundError as e:
                    st.error(str(e))
                    return
                except Exception as e:
                    st.error(f"Prediction failed: {e}")
                    return

                is_cancerous = predicted_class.startswith("ALL")

                format_prompt = (
                    f"The blood cell image analysis indicates: **{predicted_class}** "
                    f"with a confidence of {confidence:.2%}. "
                    f"{'The cell shows characteristics consistent with Acute Lymphoblastic Leukemia (ALL).' if is_cancerous else 'The cell appears to be a normal, healthy hematopoietic cell (HEM).'}"
                )

                model_res = model_service.ask_model(
                    name, age, "Blood Cancer (Leukemia)", format_prompt, "Not provided"
                )

                # Store results in session state
                st.session_state["blood_cancer_result"] = {
                    "name": name,
                    "age": age,
                    "predicted_class": predicted_class,
                    "confidence": confidence,
                    "is_cancerous": is_cancerous,
                    "format_prompt": format_prompt,
                    "model_res": model_res,
                }

                # Clear the selectbox selection by incrementing key counter
                st.session_state["blood_cancer_test_selectbox_counter"] += 1
                
                st.session_state["blood_cancer_success_toast"] = "✅ Analysis complete!"

            st.rerun()

    # ── Show results from session state ───────────────────────────────────
    if "blood_cancer_result" in st.session_state and "predicted_class" in st.session_state["blood_cancer_result"]:
        res = st.session_state["blood_cancer_result"]
        is_cancerous = res["is_cancerous"]

        # Result banner
        if is_cancerous:
            st.error("⚠️ **Cancerous Cell Detected**")
        else:
            st.success("✅ **Healthy--Normal Cell Detected**")

        # LLM Response
        st.markdown("### 🧑‍⚕️ AI Medical Analysis")
        st.write(res["model_res"])

    # ── Prescription Section ──────────────────────────────────────────────
    if "blood_cancer_result" in st.session_state:
        res = st.session_state["blood_cancer_result"]

        st.markdown("---")
        st.markdown("### 📋 Prescription Actions")

        col_dl, col_mail = st.columns(2)

        with col_dl:
            pdf_bytes = generate_pdf_bytes(
                patient_name=res["name"],
                age=res["age"],
                disease="Blood Cancer (Leukemia)",
                prediction_summary=res["format_prompt"],
                prescription_text=res["model_res"],
            )
            st.download_button(
                label="⬇️ Download Prescription PDF",
                data=pdf_bytes,
                file_name=f"Prescription_BloodCancer_{res['name'].replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="blood_cancer_download_btn",
            )

        with col_mail:
            if st.button("📩 Send to Email", use_container_width=True, key="blood_cancer_email_btn"):
                st.session_state["blood_cancer_show_email_form"] = True

        if st.session_state.get("blood_cancer_show_email_form"):
            with st.form("blood_cancer_email_form"):
                user_email = st.text_input(
                    "Patient's Email Address",
                    placeholder="example@gmail.com",
                    key="blood_cancer_email_input",
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
                                    disease="Blood Cancer (Leukemia)",
                                    prediction_summary=res["format_prompt"],
                                    prescription_text=res["model_res"],
                                )
                                st.success(f"✅ Prescription sent successfully to **{user_email}**!")
                                st.session_state["blood_cancer_show_email_form"] = False
                            except Exception as e:
                                st.error(f"❌ Failed to send email: {e}")
                    else:
                        st.warning("⚠️ Please enter a valid email address.")
