import streamlit as st
import google.generativeai as genai

# Configure API
genai.configure(api_key=st.secrets["LLM_API_KEY"])

# Create model
model = genai.GenerativeModel("gemini-1.5-flash")

def ask_gemini(prompt):
    try:
        response = model.generate_content(
            f"""
            You are an AI-powered health assistant.

            Rules:
            - Be simple and easy to understand
            - Do NOT give strict medical diagnosis
            - Suggest possible causes
            - Suggest basic precautions
            - Always add disclaimer
            - Ask follow-up question

            User query:
            {prompt}
            """
        )
        return response.text

    except Exception as e:
        return f"Error: {str(e)}"