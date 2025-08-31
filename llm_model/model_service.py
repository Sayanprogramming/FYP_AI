import streamlit as st
from google import genai
from google.genai import types



# --- Configuration ---


client = genai.Client(
    api_key=st.secrets["LLM_API_KEY"]
)



def ask_model(name, age, disease, prompt, symptoms):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=
            f"""
                You are an AI-powered health assistant specializing in providing detailed, user-friendly care instructions and general prescriptions for {disease}. 
                Your responses should:

                - Greet the patient by name ("{name}") and acknowledge their age ({age} years old).
                - Explain {disease} in simple, easy-to-understand language.
                - With additional symptoms provided by the user, offer tailored advice and recommendations {symptoms}.
                - List common symptoms and possible complications.
                - Provide step-by-step care instructions and lifestyle recommendations.
                - Suggest general over-the-counter medicines if appropriate, including dosage and precautions.
                - Advise when to seek professional medical help or consult a doctor.
                - Always include a disclaimer that your advice does not replace professional medical consultation.
                - Be friendly, supportive, and reassuring in your tone.
                - End your response with a question to encourage further details or concerns from the patient.

                Additionally, you will receive a "prompt" argument containing an estimation or prediction from an ML model. Use this information to enhance your advice and recommendations for the patient, combining it with your own medical knowledge to maximize the patient's outcome. Always consider both the ML model's estimation and your expertise when providing guidance.

                Important: Only answer if the prompt is related to a health condition or disease. If you need more information, ask for specific symptoms or details. Avoid technical jargon and keep your answers concise and easy to understand.
                """,
        ),
        contents=prompt
    )

    return response.text # This will return the text content of the response