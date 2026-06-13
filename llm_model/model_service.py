import streamlit as st
from google import genai

# Initialize the client
client = genai.Client(api_key=st.secrets["LLM_API_KEY"])


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

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt
        )
        return response.text

    except Exception as e:
        return f"Error: {str(e)}"