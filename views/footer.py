import streamlit as st
from datetime import datetime

def show():
    current_year = datetime.now().year
    st.markdown(f"""
        <style>
        
        .footer {{
            height: 100px;
            width: 100%;
            position: relative;
            bottom: 0;
            left: 0;
           
            background: rgba(0, 0, 0, 0.8);
            color: #ccc;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 8px 0;
            font-size: 13px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            border-radius: 10px;
        }}
        .footer a {{
            color: #4FC3F7;
            text-decoration: none;
            font-weight: 500;
        }}
        .footer a:hover {{
            text-decoration: underline;
            color: #81D4FA;
        }}
        </style>
        <div class="footer">
            © {current_year} | Built with ❤️ by &nbsp; <a href="https://github.com/ARI-900/" target="_blank">Mediwise Team</a> &nbsp; 
            • Powered by &nbsp; <a href="#" target="_blank"> Mediwise</a>
        </div>
    """, unsafe_allow_html=True)
