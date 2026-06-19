import streamlit as st
from google import genai
import time

# Initialize the client
client = genai.Client(api_key=st.secrets["LLM_API_KEY"])


def ask_model(name, age, disease, prompt, symptoms):

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

    max_retries = 3
    base_delay = 25  # The API usually asks to wait ~22-35 seconds

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=full_prompt
            )
            return response.text
        
        except Exception as e:
            error_msg = str(e)
            # If we hit the rate limit, wait and try again
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                if attempt < max_retries - 1:
                    delay = base_delay + (attempt * 10)
                    time.sleep(delay)
                    continue
            
            # For any other error, or if we run out of retries, return the error
            return f"Error: {error_msg}"