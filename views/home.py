import streamlit as st
import os

def show():
    # ── Global dashboard styles ──────────────────────────────────────────────
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Base */
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #0f1629 50%, #0a0e1a 100%);
        font-family: 'Inter', sans-serif;
        color: #f0f4ff;
    }

    /* ── Hero Section ── */
    .hero-section {
        background: linear-gradient(135deg, #1a1f3e 0%, #16213e 50%, #0f3460 100%);
        border: 1px solid rgba(99, 179, 237, 0.15);
        border-radius: 24px;
        padding: 56px 48px 48px 48px;
        margin-bottom: 36px;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(0,0,0,0.4);
    }
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(ellipse at center, rgba(99,179,237,0.06) 0%, transparent 60%);
        pointer-events: none;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(99,179,237,0.12);
        border: 1px solid rgba(99,179,237,0.3);
        border-radius: 50px;
        padding: 6px 18px;
        font-size: 13px;
        font-weight: 600;
        color: #63b3ed;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 20px;
    }
    .hero-title {
        font-size: 52px;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #63b3ed 50%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.15;
        margin: 0 0 16px 0;
        letter-spacing: -1px;
    }
    .hero-subtitle {
        font-size: 18px;
        color: #94a3b8;
        font-weight: 400;
        max-width: 700px;
        margin: 0 auto 36px auto;
        line-height: 1.7;
    }

    /* ── Image Placeholder ── */
    .img-placeholder {
        background: linear-gradient(135deg, rgba(99,179,237,0.08) 0%, rgba(167,139,250,0.08) 100%);
        border: 2px dashed rgba(99,179,237,0.25);
        border-radius: 16px;
        padding: 48px 20px;
        text-align: center;
        color: #4a5568;
        font-size: 14px;
        font-weight: 500;
        margin: 8px 0;
        transition: border-color 0.3s;
    }
    .img-placeholder .icon { font-size: 36px; display: block; margin-bottom: 10px; }
    .img-placeholder .label { color: #63b3ed; font-weight: 600; font-size: 13px; }

    /* ── Stat Cards ── */
    .stat-grid {
        display: flex;
        gap: 16px;
        margin-bottom: 32px;
        flex-wrap: wrap;
    }
    .stat-card {
        flex: 1;
        min-width: 140px;
        background: linear-gradient(135deg, #1a1f3e 0%, #16213e 100%);
        border: 1px solid rgba(99,179,237,0.15);
        border-radius: 16px;
        padding: 24px 20px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .stat-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(99,179,237,0.15);
    }
    .stat-number {
        font-size: 32px;
        font-weight: 800;
        background: linear-gradient(135deg, #63b3ed, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1;
        margin-bottom: 6px;
    }
    .stat-label {
        font-size: 13px;
        color: #64748b;
        font-weight: 500;
    }
    .stat-icon { font-size: 22px; margin-bottom: 8px; }

    /* ── Feature Cards ── */
    .feature-card {
        background: linear-gradient(135deg, #1a1f3e 0%, #16213e 100%);
        border: 1px solid rgba(99,179,237,0.12);
        border-radius: 16px;
        padding: 18px 16px;
        height: 100%;
        transition: transform 0.25s, border-color 0.25s, box-shadow 0.25s;
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
        margin-bottom: 4px;
    }
    .feature-card:hover {
        transform: translateY(-4px);
        border-color: rgba(99,179,237,0.35);
        box-shadow: 0 12px 40px rgba(99,179,237,0.12);
    }
    .feature-icon {
        font-size: 28px;
        margin-bottom: 8px;
        display: block;
    }
    .feature-title {
        font-size: 16px;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 6px;
    }
    .feature-desc {
        font-size: 13px;
        color: #64748b;
        line-height: 1.55;
    }
    .feature-tag {
        display: inline-block;
        margin-top: 8px;
        background: rgba(99,179,237,0.1);
        border: 1px solid rgba(99,179,237,0.2);
        border-radius: 50px;
        padding: 2px 10px;
        font-size: 11px;
        font-weight: 600;
        color: #63b3ed;
        letter-spacing: 0.5px;
    }

    /* ── Contributor cards ── */
    .contrib-card {
        background: linear-gradient(135deg, #1a1f3e, #16213e);
        border: 1px solid rgba(99,179,237,0.12);
        border-radius: 18px;
        padding: 28px 20px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
        transition: transform 0.25s, border-color 0.25s;
    }
    .contrib-card:hover {
        transform: translateY(-4px);
        border-color: rgba(167,139,250,0.35);
    }
    .contrib-avatar {
        width: 64px;
        height: 64px;
        border-radius: 50%;
        background: linear-gradient(135deg, #63b3ed, #a78bfa);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 14px auto;
        font-size: 26px;
        font-weight: 800;
        color: white;
        box-shadow: 0 4px 16px rgba(99,179,237,0.3);
    }
    .contrib-name {
        font-size: 15px;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 4px;
    }
    .contrib-role {
        font-size: 12px;
        color: #63b3ed;
        font-weight: 600;
        background: rgba(99,179,237,0.1);
        border: 1px solid rgba(99,179,237,0.2);
        border-radius: 50px;
        padding: 2px 12px;
        display: inline-block;
        margin-top: 4px;
    }

    /* ── Section Titles ── */
    .section-title {
        font-size: 22px;
        font-weight: 700;
        color: #e2e8f0;
        margin: 0 0 20px 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .section-title::after {
        content: '';
        flex: 1;
        height: 1px;
        background: linear-gradient(to right, rgba(99,179,237,0.3), transparent);
    }

    /* ── CTA Banner ── */
    .cta-banner {
        background: linear-gradient(135deg, #1e3a5f 0%, #1a1f3e 100%);
        border: 1px solid rgba(99,179,237,0.2);
        border-radius: 20px;
        padding: 36px 40px;
        text-align: center;
        margin-top: 32px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.3);
    }
    .cta-title {
        font-size: 26px;
        font-weight: 700;
        color: #f0f4ff;
        margin-bottom: 10px;
    }
    .cta-sub {
        font-size: 15px;
        color: #64748b;
        margin-bottom: 24px;
    }

    /* Hide Streamlit default padding */
    .block-container { padding-top: 1.5rem !important; }
    </style>
    """, unsafe_allow_html=True)

    # ── Hero Section ─────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero-section">
        <div class="hero-badge">⚡ Open Source · AI Research</div>
        <div class="hero-title">HealthForge AI</div>
        <div class="hero-subtitle">
            We are AI engineers contributing to the healthcare domain by trying to solve real-world problems.
            Our predictive models are completely open-source and free for anyone to integrate into their own systems.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Hero Content (Image Left, Features Right) ─────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    col_left, col_right = st.columns([1.1, 1])
    
    with col_left:
        try:
            st.image("utils/c51c8e9b-bd9d-4219-b807-5dc872a6b6cd.jpeg", use_container_width=True)
        except Exception:
            st.warning("Image not found: utils/c51c8e9b-bd9d-4219-b807-5dc872a6b6cd.jpeg")

    with col_right:
        right_html = (
            '<div style="display:flex;flex-direction:column;justify-content:center;height:100%;padding:20px;">'
            '<h3 style="color:#e2e8f0;font-weight:800;font-size:26px;margin-top:0;margin-bottom:24px;letter-spacing:-0.5px;">Why HealthForge AI?</h3>'
            '<div style="display:flex;align-items:flex-start;gap:16px;margin-bottom:24px;">'
            '<div style="font-size:24px;margin-top:2px;">🎯</div>'
            '<div>'
            '<h4 style="color:#f472b6;font-size:17px;font-weight:700;margin:0 0 6px 0;">High Accuracy</h4>'
            '<p style="color:#94a3b8;font-size:14.5px;margin:0;line-height:1.5;">Our predictive models achieve state-of-the-art accuracy on real-world datasets.</p>'
            '</div></div>'
            '<div style="display:flex;align-items:flex-start;gap:16px;margin-bottom:24px;">'
            '<div style="font-size:24px;margin-top:2px;">⚡</div>'
            '<div>'
            '<h4 style="color:#34d399;font-size:17px;font-weight:700;margin:0 0 6px 0;">Lightning Fast</h4>'
            '<p style="color:#94a3b8;font-size:14.5px;margin:0;line-height:1.5;">Instant predictions designed for scalable and modern healthcare applications.</p>'
            '</div></div>'
            '<div style="display:flex;align-items:flex-start;gap:16px;margin-bottom:24px;">'
            '<div style="font-size:24px;margin-top:2px;">🔒</div>'
            '<div>'
            '<h4 style="color:#a78bfa;font-size:17px;font-weight:700;margin:0 0 6px 0;">Data Protected</h4>'
            '<p style="color:#94a3b8;font-size:14.5px;margin:0;line-height:1.5;">Your health data stays private. End-to-end security with no third-party sharing.</p>'
            '</div></div>'
            '<div style="display:flex;align-items:flex-start;gap:16px;">'
            '<div style="font-size:24px;margin-top:2px;">🔓</div>'
            '<div>'
            '<h4 style="color:#63b3ed;font-size:17px;font-weight:700;margin:0 0 6px 0;">100% Open Source</h4>'
            '<p style="color:#94a3b8;font-size:14.5px;margin:0;line-height:1.5;">Built for the community. Free to use, fork, and integrate into your systems.</p>'
            '</div></div>'
            '</div>'
        )
        st.markdown(right_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Stats Row ─────────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">📊 Platform Overview</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    stats = [
        ("🤖", "4+", "AI Models"),
        ("🎯", "89%", "Accuracy"),
        ("⚡", "<1s", "Response Time"),
        ("🔒", "100%", "Data Private"),
    ]
    for col, (icon, num, label) in zip([c1, c2, c3, c4], stats):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">{icon}</div>
                <div class="stat-number">{num}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Features ─────────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">🚀 What We Offer</div>', unsafe_allow_html=True)

    features = [
        ("🧠", "Diabetes Prediction", "Advanced ML model analyses your health metrics to assess diabetes risk with high precision.", "ML · XGBoost"),
        ("❤️", "Heart Disease Detection", "Predict cardiovascular disease risk using clinical parameters and AI-driven analysis.", "ML · Random Forest"),
        ("💬", "General Health Support", "Chat with our expert AI health assistant for personalized wellness guidance and health tips.", "AI · Gemini 2.5"),
        ("🎗️", "Breast Cancer Detection", "Detect breast cancer through AI-powered analysis of medical images using deep learning.", "CNN · Image AI"),
    ]

    col_a, col_b = st.columns(2)
    col_c, col_d = st.columns(2)

    for col, (icon, title, desc, tag) in [(col_a, features[0]), (col_b, features[1])]:
        with col:
            card_html = (
                f'<div class="feature-card">'
                f'<span class="feature-icon">{icon}</span>'
                f'<div class="feature-title">{title}</div>'
                f'<div class="feature-desc">{desc}</div>'
                # f'<span class="feature-tag">{tag}</span>'
                f'</div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)

    for col, (icon, title, desc, tag) in [(col_c, features[2]), (col_d, features[3])]:
        with col:
            card_html = (
                f'<div class="feature-card">'
                f'<span class="feature-icon">{icon}</span>'
                f'<div class="feature-title">{title}</div>'
                f'<div class="feature-desc">{desc}</div>'
                # f'<span class="feature-tag">{tag}</span>'
                f'</div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Contributors ─────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">👥 Contributors</div>', unsafe_allow_html=True)

    contributors = [
        ("A", "Arijit Chowdhury", "Data Scientist"),
        ("D", "Debarati Chaudhuri", "UI/UX Designer"),
        ("J", "Joymalya Dey", "Backend Engineer"),
        ("S", "Sayan Sadhu", "AI Developer"),
    ]

    cc1, cc2, cc3, cc4 = st.columns(4)
    for col, (initial, name, role) in zip([cc1, cc2, cc3, cc4], contributors):
        with col:
            st.markdown(f"""
            <div class="contrib-card">
                <div class="contrib-avatar">{initial}</div>
                <div class="contrib-name">{name}</div>
                <span class="contrib-role">{role}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CTA Banner ───────────────────────────────────────────────────────────
    st.markdown("""
    <div class="cta-banner">
        <div class="cta-title">Ready to get started? 🚀</div>
        <div class="cta-sub">Navigate to <strong>Services</strong> from the sidebar to run an AI health prediction.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
