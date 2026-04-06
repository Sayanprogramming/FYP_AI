import streamlit as st
import google.generativeai as genai

# Configure API
genai.configure(api_key=st.secrets["LLM_API_KEY"])

# Create model
model = genai.GenerativeModel("gemini-1.5-flash")


def ask_model(name, age, disease, prompt, symptoms):

    try:
        full_prompt = f"""
        You are an AI-powered health assistant specializing in providing detailed, user-friendly care instructions and general guidance for {disease}.

        Patient Details:
        Name: {name}
        Age: {age}

        Symptoms: {symptoms}

        ML Prediction Info:
        {prompt}

        Instructions:
        - Greet the patient by name
        - Explain the disease in simple terms
        - Provide care tips and precautions
        - Suggest basic medicines (avoid strict prescriptions)
        - Mention when to consult a doctor
        - Add a disclaimer
        - Be friendly and simple
        - End with a follow-up question
        """

        response = model.generate_content(full_prompt)
        return response.text

    except Exception as e:
        return f"Error: {str(e)}"