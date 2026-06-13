import streamlit as st
from google import genai

# Initialize the client
client = genai.Client(api_key=st.secrets["LLM_API_KEY"])

def ask_gemini(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"""
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