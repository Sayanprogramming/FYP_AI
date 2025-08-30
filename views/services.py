import streamlit as st
from llm_model.gemini_service import ask_gemini



def show():

    
    st.markdown(
        """
        <style>
        /* Page background */
        .stApp {
            background-color: #0f111a;
            color: #f5f5f5;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        /* Header */
        .header-title {
            font-size: 42px;
            font-weight: 700;
            color: #ff6f91;
            text-align: center;
            margin-bottom: 10px;
        }

        /* Subheader/info box */
        .header-subtitle {
            font-size: 18px;
            text-align: center;
            color: #f0f0f0;
            background-color: royalblue;
            padding: 15px 20px;
            border-radius: 12px;
            max-width: 900px;
            margin: 0 auto 20px auto;
            line-height: 1.6;
        }

        /* Separator */
        .separator {
            border-top: 1px solid #333;
            margin: 20px 0;
        }
        .chatInfo {
            font-size: 1rem;
            color: #888;
            text-align: center;
            margin-top: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.set_page_config(page_title="AI Patient Health Suggestor", page_icon="💬")


    st.markdown('<div class="header-title">💖 AI Patient Health Suggestor</div>', unsafe_allow_html=True)

    st.markdown(
    '<div class="header-subtitle">'
    'Get personalized health insights instantly with our AI-powered health assistant, '
    'designed to provide smart, reliable, and user-friendly support for better wellness decisions.'
    '</div>',
    unsafe_allow_html=True
    )

    st.markdown("---")



    #------------------- CHAT MODEL INTEGRATION -------------------

    if "messages" not in st.session_state:
        st.session_state.messages = []


    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    if prompt := st.chat_input("What would you like to talk about?"):

        st.session_state.messages.append({
            "role": "user",
            "content": prompt + "Note: Below I provide the context of previous conversation"
        })

        with st.chat_message("user"):
            st.markdown(prompt)


        # creating a payload baby
        payload = ""
        for msg in st.session_state.messages:
            payload += f"{msg['role'].capitalize()}: {msg['content']}\n"

        
        # payload = [
        #     {
        #         "role" : msg["role"],
        #         "content": msg["content"]
        #     }
        #     for msg in st.session_state.messages
        # ]


        # model operation
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                model_response = ask_gemini(payload)
                st.markdown(model_response)
    
        st.session_state.messages.append({"role": "assistant", "content": model_response})
    if st.session_state.messages:
        st.button("Clear Chat", on_click=lambda: st.session_state.messages.clear())
    else:
        st.markdown("<div class='chatInfo'>No messages yet...</div>", unsafe_allow_html=True)