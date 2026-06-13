import streamlit as st
import pandas as pd
from pathlib import Path

DATA_PATH = Path("utils/contributions.csv")

def save_contribution(name, email, role, bio, message):
    row = {"name": name, "email": email, "role": role, "bio": bio, "message": message}
    
    # Ensure directory exists
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    if DATA_PATH.exists():
        try:
            df = pd.read_csv(DATA_PATH)
        except Exception:
            df = pd.DataFrame()
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])

    df.to_csv(DATA_PATH, index=False)

    # Reset session state
    st.session_state['contrib_form'] = {
        'name': '',
        'email': '',
        'role': 'Machine Learning / AI Research',
        'bio': '',
        'message': ''
    }

def show():
    # Initialize state
    if 'contrib_form' not in st.session_state:
        st.session_state['contrib_form'] = {
            'name': '',
            'email': '',
            'role': 'Machine Learning / AI Research',
            'bio': '',
            'message': ''
        }

    # Style block
    st.markdown("""
    <style>
    /* Image on the left side — match form height exactly */
    div[data-testid="stImage"] {
        height: 560px !important;
        overflow: hidden;
        border-radius: 24px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }
    div[data-testid="stImage"] img {
        width: 100% !important;
        height: 560px !important;
        object-fit: cover !important;
        border-radius: 24px;
    }
    .contrib-img-placeholder .icon {
        font-size: 52px;
        margin-bottom: 18px;
        display: block;
    }
    .contrib-img-placeholder .label {
        color: #a78bfa;
        font-weight: 700;
        font-size: 17px;
        margin-bottom: 8px;
    }
    .contrib-img-placeholder .hint {
        color: #94a3b8;
        font-size: 13.5px;
        max-width: 280px;
        line-height: 1.6;
    }
    
    /* Styled container for the right side form */
    div[data-testid="stForm"] {
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.25) 0%, rgba(15, 23, 42, 0.25) 100%) !important;
        border: 1px solid rgba(167, 139, 250, 0.12) !important;
        border-radius: 24px !important;
        padding: 36px 30px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4) !important;
        height: 560px; /* Match left side height exactly */
    }

    /* Roadmap Table styling */
    .roadmap-table {
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0 40px 0;
        font-size: 14.5px;
    }
    .roadmap-table th, .roadmap-table td {
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 14px 16px;
        text-align: left;
    }
    .roadmap-table th {
        background-color: rgba(167, 139, 250, 0.1);
        color: #a78bfa;
        font-weight: 700;
    }
    .roadmap-table tr:hover {
        background-color: rgba(255, 255, 255, 0.02);
    }
    
    /* Priority tag colors */
    .priority-tag {
        font-size: 11px;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 50px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: inline-block;
        text-align: center;
    }
    .priority-tag.high {
        background: rgba(245, 101, 101, 0.15);
        color: #f56565;
        border: 1px solid rgba(245, 101, 101, 0.3);
    }
    .priority-tag.med {
        background: rgba(237, 137, 54, 0.15);
        color: #ed8936;
        border: 1px solid rgba(237, 137, 54, 0.3);
    }
    .priority-tag.low {
        background: rgba(72, 187, 120, 0.15);
        color: #48bb78;
        border: 1px solid rgba(72, 187, 120, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

    # Page title
    st.markdown("<h2 style='text-align:center;'>🤝 Join & Contribute</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center; color:#94a3b8; max-width:800px; margin: 0 auto 30px auto;'>"
        "HealthForge AI is completely open-source. Whether you are a researcher, AI engineer, data scientist, "
        "or frontend developer, your contribution can help shape the future of digital medicine."
        "</p>",
        unsafe_allow_html=True
    )

    # 2 Column layout
    col_img, col_form = st.columns([1, 1], gap="large")
    with col_img:
        try:
            st.image("utils/doctor.jpeg", use_container_width=True)
        except Exception:
            st.warning("Image not found: utils/doctor.jpeg")

    with col_form:
        with st.form(key='contrib_form_ui'):
            name = st.text_input(
                "Name *", 
                value=st.session_state['contrib_form'].get('name', ''), 
                placeholder="Enter your name"
            )
            email = st.text_input(
                "Email *", 
                value=st.session_state['contrib_form'].get('email', ''), 
                placeholder="Enter your email"
            )
            role = st.selectbox(
                "Primary Focus Area *",
                options=[
                    "Machine Learning / AI Research",
                    "UI/UX & Frontend Development",
                    "Data Engineering & Pipeline",
                    "Medical Domain Expert"
                ],
                index=options_index if (options_index := [
                    "Machine Learning / AI Research",
                    "UI/UX & Frontend Development",
                    "Data Engineering & Pipeline",
                    "Medical Domain Expert"
                ].index(st.session_state['contrib_form'].get('role', 'Machine Learning / AI Research'))) != -1 else 0
            )
            bio = st.text_input(
                "Brief Bio / Skills", 
                value=st.session_state['contrib_form'].get('bio', ''), 
                placeholder="e.g. Python, PyTorch, Streamlit"
            )
            message = st.text_area(
                "How do you want to contribute? *", 
                value=st.session_state['contrib_form'].get('message', ''), 
                placeholder="Describe your ideas or interest..."
            )
            
            submit = st.form_submit_button("Submit Application")

            if submit:
                if not name or not email or not message:
                    st.error("Please fill in all the required fields (*).")
                else:
                    save_contribution(name, email, role, bio, message)
                    st.success(f"Thank you, {name}! Your contribution interest has been recorded successfully.")
                    st.toast("Contribution application saved to contributions.csv!")

    # ── Roadmap Section ───────────────────────────────────────────────────────
    st.markdown("<br><hr style='border-color: rgba(255,255,255,0.08);'><br>", unsafe_allow_html=True)
    st.markdown("### 🛠️ Active Contribution Roadmap")
    st.write("Below are the current open research objectives and priorities where you can collaborate:")
    
    st.markdown("""
    <table class="roadmap-table">
        <thead>
            <tr>
                <th>Focus Area</th>
                <th>Active Goal / Tasks</th>
                <th>Required Stack / Skillset</th>
                <th>Priority</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>🧠 Model Development</strong></td>
                <td>Train and deploy the upcoming Oncology (Cancer) CNN Classifier</td>
                <td>PyTorch, CNN architectures, ResNet-50</td>
                <td><span class="priority-tag high">High</span></td>
            </tr>
            <tr>
                <td><strong>🍲 Stomach Issues Predictor</strong></td>
                <td>Define baseline dataset and select features for the stomach classification model</td>
                <td>Pandas, Scikit-learn, XGBoost</td>
                <td><span class="priority-tag med">Medium</span></td>
            </tr>
            <tr>
                <td><strong>🎨 Frontend Polish</strong></td>
                <td>Design interactive confusion matrix plots and glassmorphism theme components</td>
                <td>Streamlit, CSS, Plotly/Matplotlib</td>
                <td><span class="priority-tag low">Low</span></td>
            </tr>
            <tr>
                <td><strong>🩺 Clinical Validation</strong></td>
                <td>Review diagnostics safety boundaries, disclaimers, and write diagnostic guidelines</td>
                <td>Clinical Practice, Medical Domain expertise</td>
                <td><span class="priority-tag high">High</span></td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)
