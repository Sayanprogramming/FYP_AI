import streamlit as st
from llm_model.gemini_service import ask_gemini
import views.diabetes_ui as diabetes_ui
import views.heart_ui as heart_ui
import importlib
blood_cancer_ui = importlib.import_module("views.blood cancer_ui")

def show():
    # ── Styling and Aesthetics ──────────────────────────────────────────────
    st.markdown(
        """
        <style>
        /* Base page overrides */
        .stApp {
            background: linear-gradient(135deg, #0a0e1a 0%, #0f1629 50%, #0a0e1a 100%);
            font-family: 'Inter', sans-serif;
        }

        /* ── Services Header ── */
        .services-header {
            background: linear-gradient(135deg, #1e1b4b 0%, #311042 50%, #1e1b4b 100%);
            border: 1px solid rgba(167, 139, 250, 0.15);
            border-radius: 24px;
            padding: 48px 40px;
            margin-bottom: 32px;
            text-align: center;
            position: relative;
            overflow: hidden;
            box-shadow: 0 20px 50px rgba(0,0,0,0.3);
        }
        .services-badge {
            display: inline-block;
            background: rgba(167, 139, 250, 0.12);
            border: 1px solid rgba(167, 139, 250, 0.3);
            border-radius: 50px;
            padding: 6px 18px;
            font-size: 13px;
            font-weight: 600;
            color: #a78bfa;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-bottom: 16px;
        }
        .services-title {
            font-size: 48px;
            font-weight: 800;
            background: linear-gradient(135deg, #ffffff 0%, #a78bfa 50%, #f472b6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0 0 14px 0;
            letter-spacing: -1px;
        }
        .services-subtitle {
            font-size: 17px;
            color: #94a3b8;
            max-width: 750px;
            margin: 0 auto;
            line-height: 1.6;
        }

        /* ── Glassmorphic Forms Custom Styling ── */
        div[data-testid="stForm"] {
            background: linear-gradient(135deg, rgba(30, 27, 75, 0.25) 0%, rgba(15, 23, 42, 0.25) 100%) !important;
            border: 1px solid rgba(167, 139, 250, 0.15) !important;
            border-radius: 20px !important;
            padding: 32px 36px !important;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4) !important;
            margin-top: 10px;
        }
        
        /* Form titles adjustments */
        div[data-testid="stForm"] hr {
            border-color: rgba(167, 139, 250, 0.3) !important;
        }
        
        /* Submit button overrides */
        button[kind="formSubmit"] {
            background: linear-gradient(135deg, #a78bfa 0%, #f472b6 100%) !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            border: none !important;
            border-radius: 50px !important;
            padding: 10px 30px !important;
            box-shadow: 0 4px 14px rgba(167, 139, 250, 0.4) !important;
            transition: all 0.2s ease-in-out !important;
        }
        button[kind="formSubmit"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(167, 139, 250, 0.6) !important;
        }

        /* ── Chat Message Overrides ── */
        div[data-testid="stChatMessage"] {
            background: linear-gradient(135deg, rgba(30, 27, 75, 0.3) 0%, rgba(15, 23, 42, 0.3) 100%) !important;
            border: 1px solid rgba(167, 139, 250, 0.12) !important;
            border-radius: 18px !important;
            padding: 18px 22px !important;
            margin-bottom: 16px !important;
            box-shadow: 0 6px 20px rgba(0,0,0,0.2) !important;
        }
        div[data-testid="stChatMessageAdornment"] {
            display: none !important;
        }

        /* ── Chat Input Overrides ── */
        div[data-testid="stChatInput"] {
            border: 1px solid rgba(167, 139, 250, 0.25) !important;
            background-color: rgba(15, 23, 42, 0.8) !important;
            border-radius: 14px !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
        }
        div[data-testid="stChatInput"] textarea {
            color: #f0f4ff !important;
            background-color: transparent !important;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
        }
        div[data-testid="stChatInput"] textarea:focus {
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
        }
        div[data-testid="stChatInput"] button {
            background-color: transparent !important;
            color: #a78bfa !important;
            border: none !important;
            outline: none !important;
        }
        /* Remove default inner black border wrappers */
        div[data-testid="stChatInput"] > div,
        div[data-testid="stChatInput"] > div > div {
            border: none !important;
            outline: none !important;
            background: transparent !important;
            box-shadow: none !important;
        }

        /* ── Coming Soon Cards ── */
        .coming-soon-card {
            background: linear-gradient(135deg, #161b33 0%, #0d0f1d 100%);
            border: 1px solid rgba(167, 139, 250, 0.15);
            border-radius: 24px;
            padding: 48px 36px;
            text-align: center;
            max-width: 600px;
            margin: 40px auto;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
        }
        .cs-icon {
            font-size: 54px;
            margin-bottom: 16px;
            display: inline-block;
        }
        .cs-title {
            font-size: 24px;
            font-weight: 800;
            color: #e2e8f0;
            margin-bottom: 8px;
        }
        .cs-status {
            font-size: 12px;
            font-weight: 700;
            color: #f472b6;
            background: rgba(244, 114, 182, 0.12);
            border: 1px solid rgba(244, 114, 182, 0.25);
            padding: 4px 14px;
            border-radius: 50px;
            display: inline-block;
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .cs-desc {
            font-size: 14.5px;
            color: #94a3b8;
            line-height: 1.7;
            margin-bottom: 24px;
        }
        .cs-features {
            display: flex;
            justify-content: center;
            gap: 10px;
            flex-wrap: wrap;
        }
        .cs-feat-tag {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            color: #cbd5e1;
            padding: 4px 14px;
            border-radius: 50px;
            font-size: 12.5px;
            font-weight: 500;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # ── Header Banner ───────────────────────────────────────────────────────
    st.markdown(
        """
        <div class="services-header">
            <div class="services-badge">🧪 Diagnostic Sandbox</div>
            <div class="services-title">AI Predictive Services</div>
            <div class="services-subtitle">
                Interact with our production machine learning models and conversational research assistants. 
                Configure patient variables below to run diagnostics.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Sidebar model selector
    model_options = [
        "💬 General Health Assessment",
        "🧠 Diabetes Prediction",
        "❤️ Heart Disease Prediction",
        "🩸 Blood Cancer Detection",
    ]
    selected_model = st.sidebar.selectbox("Select a service:", model_options)

    # ── Routing ─────────────────────────────────────────────────────────────
    if "General Health" in selected_model:
        st.markdown("### 💬 Generative Wellness AI Assistant")
        st.write("An LLM assistant fine-tuned to converse about wellness, preventative care, and explain model inputs.")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask a wellness or diagnostic question..."):
            st.session_state.messages.append({
                "role": "user",
                "content": prompt
            })

            with st.chat_message("user"):
                st.markdown(prompt)

            payload = ""
            for msg in st.session_state.messages:
                payload += f"{msg['role'].capitalize()}: {msg['content']}\n"

            with st.chat_message("assistant"):
                with st.spinner("Processing queries..."):
                    model_response = ask_gemini(payload)
                    st.markdown(model_response)

            st.session_state.messages.append({"role": "assistant", "content": model_response})

        if st.session_state.messages:
            st.button("Clear Conversation", on_click=lambda: st.session_state.messages.clear(), use_container_width=True)
        else:
            st.markdown("<div style='text-align:center; color:#4a5568; padding:30px;'>No active chat history. Start typing below.</div>", unsafe_allow_html=True)

    elif "Diabetes" in selected_model:
        diabetes_ui.show_ui()

    elif "Heart Disease" in selected_model:
        heart_ui.show_ui()

    elif "Blood Cancer" in selected_model:
        blood_cancer_ui.show_ui()