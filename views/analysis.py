import streamlit as st
import os
import json
import joblib
import pandas as pd
import numpy as np
from pathlib import Path

# ─ Helper Functions ─────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@st.cache_data
def load_metrics(model_path):
    """Load metrics from JSON file"""
    try:
        with open(model_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading metrics: {e}")
        return None

@st.cache_data
def load_model_and_scaler(model_name):
    """Load model and scaler joblib files"""
    try:
        if model_name == "diabetes":
            model_path = os.path.join(BASE_DIR, "models", "diabetesPredict_model", "diabetes_model.joblib")
            scaler_path = os.path.join(BASE_DIR, "models", "diabetesPredict_model", "diabetes_scaler.joblib")
        else:  # heart
            model_path = os.path.join(BASE_DIR, "models", "heart disease_pred_model", "heart_model.joblib")
            scaler_path = os.path.join(BASE_DIR, "models", "heart disease_pred_model", "heart_scaler.joblib")
        
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        return model, scaler
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None

@st.cache_data
def load_testing_data(model_name):
    """Load testing dataset JSON"""
    try:
        if model_name == "diabetes":
            data_path = os.path.join(BASE_DIR, "models", "diabetesPredict_model", "testing_dataset.json")
        else:  # heart
            data_path = os.path.join(BASE_DIR, "models", "heart disease_pred_model", "testing_dataset.json")
        
        with open(data_path, 'r') as f:
            data = json.load(f)
            # Handle both list and dictionary formats
            if isinstance(data, dict):
                return [data]
            return data
    except Exception as e:
        st.error(f"Error loading testing data: {e}")
        return []

@st.cache_data
def load_dataset_csv(model_name):
    """Load dataset CSV for info"""
    try:
        if model_name == "diabetes":
            csv_path = os.path.join(BASE_DIR, "models", "diabetesPredict_model", "diabetes_dataset.csv")
        else:  # heart
            csv_path = os.path.join(BASE_DIR, "models", "heart disease_pred_model", "heart_disease_dataset.csv")
        
        return pd.read_csv(csv_path)
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None

def show():
    # ── Enhanced Styling ───────────────────────────────────────────────────
    st.markdown("""
    <style>
    /* Metric Cards */
    .metric-box {
        background: linear-gradient(135deg, #1a365d 0%, #2c5282 100%);
        border: 1px solid rgba(99, 179, 237, 0.3);
        border-radius: 12px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }
    .metric-box:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 35px rgba(99, 179, 237, 0.4);
        border-color: rgba(99, 179, 237, 0.6);
    }
    .metric-value {
        font-size: 42px;
        font-weight: 900;
        background: linear-gradient(135deg, #63b3ed, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 8px;
    }
    .metric-title {
        font-size: 13px;
        color: #cbd5e0;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Model Info Box */
    .model-info-box {
        background: linear-gradient(135deg, rgba(26, 54, 93, 0.8) 0%, rgba(44, 82, 130, 0.8) 100%);
        border-left: 5px solid #63b3ed;
        padding: 25px;
        border-radius: 12px;
        margin: 15px 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
    }
    .model-info-title {
        color: #63b3ed;
        font-weight: 800;
        font-size: 18px;
        margin-bottom: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .model-info-content {
        color: #e2e8f0;
        font-size: 14px;
        line-height: 1.8;
    }
    
    /* Feature Box */
    .feature-box {
        background: rgba(44, 82, 130, 0.4);
        border: 1px solid rgba(99, 179, 237, 0.2);
        padding: 15px;
        border-radius: 8px;
        margin: 8px 0;
        border-left: 4px solid #63b3ed;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Main Header ────────────────────────────────────────────────────────
    st.markdown(
        "<div style='text-align: center; margin-bottom: 30px;'>"
        "<h1 style='color: #63b3ed; margin-bottom: 10px;'>🏥 AI-Powered Medical Prediction Models</h1>"
        "<p style='color: #94a3b8; font-size: 16px; max-width: 900px; margin: 0 auto;'>"
        "Advanced machine learning analysis for diabetes and heart disease prediction with comprehensive model insights"
        "</p></div>",
        unsafe_allow_html=True
    )
    st.markdown("---")

    # ── Model Selection (TOP - Easy Access) ────────────────────────────────
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        selected_model = st.selectbox(
            "🔍 Select Model:", 
            ["Diabetes Prediction", "Heart Disease Prediction", "Blood Cancer Detection"],
            key="model_select"
        )
    
    if selected_model == "Diabetes Prediction":
        model_key = "diabetes"
    elif selected_model == "Heart Disease Prediction":
        model_key = "heart"
    else:
        model_key = "blood_cancer"
    
    # ── QUICK MODEL STATUS INDICATOR ────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%); 
                    padding: 15px; border-radius: 8px; text-align: center; color: white;'>
            <strong>✅ Status</strong><br>
            <span style='font-size: 18px; font-weight: bold;'>Active</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        alg = "Random Forest" if model_key == "diabetes" else ("XGBoost" if model_key == "heart" else "ResNet-18 CNN")
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); 
                    padding: 15px; border-radius: 8px; text-align: center; color: white;'>
            <strong>📦 Algorithm</strong><br>
            <span style='font-size: 16px;'>{alg}</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        purp = "Diabetes" if model_key == "diabetes" else ("Heart" if model_key == "heart" else "Blood Cancer")
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #ec4899 0%, #db2777 100%); 
                    padding: 15px; border-radius: 8px; text-align: center; color: white;'>
            <strong>🎯 Purpose</strong><br>
            <span style='font-size: 16px;'>{purp} Risk</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        typ = "Classification" if model_key != "blood_cancer" else "Image Classification"
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                    padding: 15px; border-radius: 8px; text-align: center; color: white;'>
            <strong>📊 Type</strong><br>
            <span style='font-size: 16px;'>{typ}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")

    # ── CREATE THREE TABS ──────────────────────────────────────────────────
    tab_overview, tab_results = st.tabs(["📋 Model Overview", "📈 Model Results"])

    # ═══════════════════════════════════════════════════════════════════════
    # TAB 1: MODEL OVERVIEW
    # ═══════════════════════════════════════════════════════════════════════
    with tab_overview:
        
        # ── SECTION 1: MODEL ARCHITECTURE ──────────────────────────────────
        st.markdown("<h2 style='color: #63b3ed;'>🏗️ Model Architecture & Design</h2>", unsafe_allow_html=True)
        
        if model_key == "diabetes":
            # ===== DIABETES MODEL DETAILS =====
            st.markdown("""
            <div class="model-info-box">
                <div class="model-info-title">🔬 Why Random Forest for Diabetes Prediction?</div>
                <div class="model-info-content">
                <strong>Random Forest was selected for the following reasons:</strong><br><br>
                ✅ <strong>Handles Non-linear Relationships:</strong> Diabetes development involves complex interactions between features like glucose, BMI, and age that are not strictly linear<br><br>
                ✅ <strong>Feature Importance Extraction:</strong> Identifies which health metrics (Glucose, BMI, Age) are most critical for prediction, helping doctors understand risk factors<br><br>
                ✅ <strong>Robustness to Outliers:</strong> Healthcare data often contains edge cases and anomalies; RF is inherently resistant to outliers<br><br>
                ✅ <strong>No Feature Scaling Required:</strong> Tree-based models are scale-invariant, maintaining biological meaning of features<br><br>
                ✅ <strong>High Interpretability:</strong> Medical professionals can understand decision logic for clinical validation<br><br>
                ✅ <strong>Ensemble Learning:</strong> 200 decision trees voting together reduces overfitting and improves generalization<br><br>
                <strong>Comparison:</strong> Logistic Regression (simpler but less accurate) vs XGBoost (overkill, slower training)
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        elif model_key == "heart":
            # ===== HEART DISEASE MODEL DETAILS =====
            st.markdown("""
            <div class="model-info-box">
                <div class="model-info-title">❤️ Why XGBoost for Heart Disease Prediction?</div>
                <div class="model-info-content">
                <strong>XGBoost was selected for the following reasons:</strong><br><br>
                ✅ <strong>Gradient Boosting Excellence:</strong> Iteratively improves predictions, capturing complex cardiovascular risk patterns<br><br>
                ✅ <strong>Superior Performance:</strong> Consistently outperforms traditional methods on medical classification tasks with complex features<br><br>
                ✅ <strong>Complex Feature Interactions:</strong> Captures interactions (high BP + high cholesterol + smoking are more dangerous together)<br><br>
                ✅ <strong>Imbalanced Data Handling:</strong> Heart disease prevalence may be skewed; XGBoost handles this naturally<br><br>
                ✅ <strong>Efficient Training:</strong> Fast convergence even with 11+ features and 300 decision trees<br><br>
                ✅ <strong>Built-in Regularization:</strong> L1/L2 regularization prevents overfitting on medical datasets<br><br>
                <strong>Key Difference:</strong> Heart disease requires XGBoost's boosting approach due to non-linear feature interactions; Diabetes uses simpler Random Forest
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # ===== BLOOD CANCER MODEL DETAILS =====
            st.markdown("""
            <div class="model-info-box">
                <div class="model-info-title">🩸 Why ResNet-18 for Blood Cancer Detection?</div>
                <div class="model-info-content">
                <strong>ResNet-18 was selected for the following reasons:</strong><br><br>
                ✅ <strong>Deep Residual Learning:</strong> Skip connections prevent the vanishing gradient problem, allowing the network to learn incredibly complex patterns from cell images.<br><br>
                ✅ <strong>Pre-trained on ImageNet:</strong> Leverages transfer learning. The model already knows how to detect edges, textures, and shapes from millions of images before even seeing a blood cell.<br><br>
                ✅ <strong>High Accuracy on Image Data:</strong> CNNs (Convolutional Neural Networks) are the gold standard for computer vision and medical image analysis.<br><br>
                ✅ <strong>Efficiency:</strong> ResNet-18 is lightweight enough to be trained rapidly on a CPU while retaining state-of-the-art predictive power.<br><br>
                ✅ <strong>Spatial Hierarchies:</strong> Automatically identifies microscopic anomalies like chromatin clumping or irregular cytoplasm borders without manual feature engineering.
                </div>
            </div>
            """, unsafe_allow_html=True)
    
        # ── SECTION 2: DATASET INFORMATION ─────────────────────────────────
        st.markdown("<h2 style='color: #63b3ed;'>📊 Dataset Details & Characteristics</h2>", unsafe_allow_html=True)
        
        if model_key == "blood_cancer":
            st.markdown("##### 🖼️ Image Dataset Characteristics")
            
            # Load dynamic values if metrics.json exists
            metrics_path = os.path.join(BASE_DIR, "models", "blood cancer_model", "metrics.json")
            train_count = 10661
            val_count = 1867
            img_size = "128x128"
            
            if os.path.exists(metrics_path):
                try:
                    with open(metrics_path, 'r') as f:
                        bc_data = json.load(f)
                    train_count = bc_data.get("training_images", train_count)
                    val_count = bc_data.get("validation_images", val_count)
                    size = bc_data.get("image_size", 128)
                    img_size = f"{size}x{size}"
                except:
                    pass
                    
            col1, col2, col3, col4 = st.columns(4)
            with col1: st.markdown(f"<div class='metric-box'><div class='metric-value'>{train_count:,}</div><div class='metric-title'>Training Images</div></div>", unsafe_allow_html=True)
            with col2: st.markdown(f"<div class='metric-box'><div class='metric-value'>{val_count:,}</div><div class='metric-title'>Validation Images</div></div>", unsafe_allow_html=True)
            with col3: st.markdown(f"<div class='metric-box'><div class='metric-value'>{img_size}</div><div class='metric-title'>Image Resolution</div></div>", unsafe_allow_html=True)
            with col4: st.markdown("<div class='metric-box'><div class='metric-value'>2</div><div class='metric-title'>Classes (ALL/HEM)</div></div>", unsafe_allow_html=True)
            dataset = None
        else:
            dataset = load_dataset_csv(model_key)
        
        if dataset is not None:
            # Dataset Overview Metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-value">{len(dataset):,}</div>
                    <div class="metric-title">Total Samples</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-value">{len(dataset.columns) - 1}</div>
                    <div class="metric-title">Input Features</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-value">2</div>
                    <div class="metric-title">Output Classes</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-value">80-20</div>
                    <div class="metric-title">Train-Test Ratio</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("")
            
            # Features Description
            st.markdown("##### 📋 Input Features")
            feature_cols = [col for col in dataset.columns if col not in ['Outcome', 'Heart Disease']]
            st.write(f"**Total Features:** {len(feature_cols)}")
            
            col1, col2 = st.columns(2)
            with col1:
                for i, feat in enumerate(feature_cols[:len(feature_cols)//2 + 1], 1):
                    st.markdown(f"<div class='feature-box'><strong>{i}. {feat}</strong></div>", unsafe_allow_html=True)
            
            with col2:
                if len(feature_cols) > len(feature_cols)//2 + 1:
                    for i, feat in enumerate(feature_cols[len(feature_cols)//2 + 1:], len(feature_cols)//2 + 2):
                        st.markdown(f"<div class='feature-box'><strong>{i}. {feat}</strong></div>", unsafe_allow_html=True)
            
            # Dataset Statistics
            st.markdown("")
            st.markdown("##### 📈 Statistical Summary")
            st.dataframe(dataset.describe(), use_container_width=True)
        
        
        # ── SECTION 3: MODEL LIMITATIONS & CONSIDERATIONS ────────────────────
        st.markdown("<h2 style='color: #63b3ed;'>⚠️ Model Limitations & Important Considerations</h2>", unsafe_allow_html=True)
        
        if model_key == "diabetes":
            st.markdown("""
            <div class="model-info-box">
                <div class="model-info-title">🔔 Important Limitations to Consider</div>
                <div class="model-info-content">
                <strong>1. Dataset Size:</strong> Model trained on finite historical data - may not capture rare disease presentations<br><br>
                <strong>2. Feature Limitations:</strong> Only uses provided medical metrics - doesn't consider family history, lifestyle changes, medications<br><br>
                <strong>3. Population Specificity:</strong> Trained on specific demographic - may perform differently on other populations<br><br>
                <strong>4. No Causation:</strong> Model identifies patterns but doesn't explain WHY someone has diabetes<br><br>
                <strong>5. Temporal Limitation:</strong> Data snapshot in time - disease risk factors may change<br><br>
                <strong>6. Clinical Context:</strong> Should NOT replace doctor's diagnosis - use as screening tool only<br><br>
                <strong>7. Class Imbalance:</strong> Model may be biased towards majority class despite stratification<br><br>
                <strong>✅ Best Practices:</strong> Always verify predictions with medical professionals before clinical decisions
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif model_key == "heart":
            st.markdown("""
            <div class="model-info-box">
                <div class="model-info-title">🔔 Important Limitations to Consider</div>
                <div class="model-info-content">
                <strong>1. Complex Cardiovascular Disease:</strong> Model simplifies multi-faceted heart conditions into binary prediction<br><br>
                <strong>2. Dynamic Nature:</strong> Heart disease risk changes over time; model uses point-in-time data<br><br>
                <strong>3. Missing Risk Factors:</strong> Doesn't account for stress, sleep quality, air quality, diet history<br><br>
                <strong>4. Medication Effects:</strong> Can't assess impact of current treatments on disease progression<br><br>
                <strong>5. Genetic Factors:</strong> Limited genetic risk information in features<br><br>
                <strong>6. Socioeconomic Factors:</strong> Model cannot capture healthcare access or quality differences<br><br>
                <strong>7. Edge Cases:</strong> May struggle with extremely rare presentations or combinations<br><br>
                <strong>✅ Best Practices:</strong> Use for risk stratification, not final diagnosis. Always consult cardiologists
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="model-info-box">
                <div class="model-info-title">🔔 Important Limitations to Consider</div>
                <div class="model-info-content">
                <strong>1. Image Quality Dependent:</strong> Predictions heavily rely on the quality, stain, and lighting of the uploaded microscopic image.<br><br>
                <strong>2. Cropping Artifacts:</strong> The model was trained on specifically cropped single-cell images (C-NMC dataset). Uploading a full slide will yield inaccurate results.<br><br>
                <strong>3. False Negatives:</strong> Difficult or uncommon cell morphologies may be missed by the model.<br><br>
                <strong>4. Limited Scope:</strong> The model only distinguishes between ALL (Acute Lymphoblastic Leukemia) and normal HEM cells, ignoring other leukemias.<br><br>
                <strong>✅ Best Practices:</strong> Never use as a standalone diagnostic tool. Hematologists should always review flagged cells under a microscope.
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
    
        # ═══════════════════════════════════════════════════════════════════════
    # TAB 2: MODEL RESULTS & PERFORMANCE
    # ═══════════════════════════════════════════════════════════════════════
    with tab_results:

        # ── SECTION 1: PERFORMANCE METRICS ─────────────────────────────────
        st.markdown(
            "<h2 style='color: #63b3ed;'>🎯 Model Performance Metrics</h2>",
            unsafe_allow_html=True
        )

        # ── LOAD METRICS FILE ──────────────────────────────────────────────
        if model_key == "blood_cancer":
            metrics_path = os.path.join(BASE_DIR, "models", "blood cancer_model", "metrics.json")
            if os.path.exists(metrics_path):
                with open(metrics_path, 'r') as f:
                    bc_data = json.load(f)
                metrics = {
                    "accuracy": bc_data.get("test_accuracy", 0),
                    "precision": bc_data.get("precision", 0),
                    "recall": bc_data.get("recall", 0),
                    "f1_score": bc_data.get("f1_score", 0),
                    "auc": bc_data.get("auc", 0)
                }
            else:
                metrics = None
        else:
            metrics_path = os.path.join(BASE_DIR, "utils", "metrics.json")
            all_metrics = load_metrics(metrics_path)
            metrics = all_metrics.get(model_key, {}) if all_metrics else None

        # ── DISPLAY METRICS ────────────────────────────────────────────────
        if metrics:

            accuracy = metrics.get("accuracy", 0)
            precision = metrics.get("precision", 0)
            recall = metrics.get("recall", 0)
            f1_score = metrics.get("f1_score", 0)
            auc_score = metrics.get("auc", 0)

            # ── METRIC CARDS ───────────────────────────────────────────────
            col1, col2, col3, col4, col5 = st.columns(5)

            metrics_list = [
                (col1, "Accuracy", accuracy, "{:.2%}"),
                (col2, "Precision", precision, "{:.2%}"),
                (col3, "Recall", recall, "{:.2%}"),
                (col4, "F1-Score", f1_score, "{:.2%}"),
                (col5, "AUC-ROC", auc_score, "{:.2%}"),
            ]

            for col, label, value, fmt in metrics_list:

                with col:

                    st.markdown(f"""
                    <div class="metric-box">
                        <div class="metric-value">{fmt.format(value)}</div>
                        <div class="metric-title">{label}</div>
                    </div>
                    """, unsafe_allow_html=True)

            # ── METRICS EXPLANATION ────────────────────────────────────────
            st.markdown("")
            st.markdown("##### 📚 Metrics Interpretation")

            metrics_explain = {
                "Accuracy": "Overall correctness of predictions - percentage of correct predictions out of total",
                "Precision": "Of positive predictions, how many were actually correct - avoids false alarms",
                "Recall": "Of actual positive cases, how many we correctly identified - captures actual cases",
                "F1-Score": "Balanced average of Precision and Recall - single score for model quality",
                "AUC-ROC": "Area Under ROC Curve - probability that model ranks positive higher than negative (0-1 scale)"
            }

            for metric, explanation in metrics_explain.items():
                st.markdown(f"**{metric}:** {explanation}")

        else:
            st.error("❌ Metrics file could not be loaded.")
            

        
        # ── SECTION 2: VISUALIZATIONS ──────────────────────────────────────
        st.markdown("<h2 style='color: #63b3ed;'>📊 Model Visualizations & Analysis Charts</h2>", unsafe_allow_html=True)
        
        # ── VISUALIZATION GUIDE ────────────────────────────────────────────
        st.markdown("##### 📚 How to Read These Visualizations")
        
        guide_col1, guide_col2, guide_col3 = st.columns(3)
        
        with guide_col1:
            st.markdown("""
            **📈 ROC Curve Guide**
            - X-axis: False Positive Rate (% false alarms)
            - Y-axis: True Positive Rate (% correct detections)
            - **Top-Left = Best**: Catches all cases, no false alarms
            - **Diagonal Line = Random**: No predictive power
            - **Higher AUC = Better**: Area under curve shows discrimination
            """)
        
        with guide_col2:
            st.markdown("""
            **🎯 Confusion Matrix Guide**
            - **True Positive (TP)**: Correctly predicted positive cases
            - **True Negative (TN)**: Correctly predicted negative cases
            - **False Positive (FP)**: Incorrectly flagged as positive
            - **False Negative (FN)**: Missed positive cases ⚠️
            - **Goal**: Maximize TP+TN, minimize FP+FN
            """)
        
        with guide_col3:
            st.markdown("""
            **🔍 Feature Importance Guide**
            - **Bar Height = Importance**: Taller bars = more important
            - **What it means**: How much this feature affects predictions
            - **Use case**: Identify key risk factors to monitor
            - **Clinical insight**: Doctors should focus on top 3-5 features
            """)
        
        st.markdown("---")
        
        if model_key == "diabetes":
            st.markdown("##### 🔬 Diabetes Model Visualization Suite")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📈 ROC Curve**")
                st.write("Shows the trade-off between True Positive Rate and False Positive Rate. Higher curve = better model")
                roc_curve_path = "utils/diabetes_roccurve.jpeg"
                if os.path.exists(os.path.join(BASE_DIR, roc_curve_path)):
                    st.image(os.path.join(BASE_DIR, roc_curve_path), use_container_width=True)
                else:
                    st.markdown("<div style='height: 300px; background-color: black; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white;'>[ Image Placeholder ]</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("**🎯 Confusion Matrix**")
                st.write("Shows True Positives, True Negatives, False Positives, and False Negatives")
                confusion_matrix_path = "utils/diabetes_confusion.jpeg"
                if os.path.exists(os.path.join(BASE_DIR, confusion_matrix_path)):
                    st.image(os.path.join(BASE_DIR, confusion_matrix_path), use_container_width=True)
                else:
                    st.markdown("<div style='height: 300px; background-color: black; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white;'>[ Image Placeholder ]</div>", unsafe_allow_html=True)
            
            st.markdown("")
            st.markdown("**🔍 Feature Importance Map**")
            st.write("Which features are most important for predictions? Higher bars = more important for diagnosis")
            feature_importance_path = "utils/diabetes_feature.jpeg"
            if os.path.exists(os.path.join(BASE_DIR, feature_importance_path)):
                st.image(os.path.join(BASE_DIR, feature_importance_path), use_container_width=True)
            else:
                st.markdown("<div style='height: 300px; background-color: black; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white;'>[ Image Placeholder ]</div>", unsafe_allow_html=True)
        
        elif model_key == "heart":
            st.markdown("##### ❤️ Heart Disease Model Visualization Suite")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📈 ROC Curve**")
                st.write("Shows the trade-off between True Positive Rate and False Positive Rate. Higher curve = better model")
                roc_curve_path = "utils/heart_roccurve.jpeg"
                if os.path.exists(os.path.join(BASE_DIR, roc_curve_path)):
                    st.image(os.path.join(BASE_DIR, roc_curve_path), use_container_width=True)
                else:
                    st.markdown("<div style='height: 300px; background-color: black; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white;'>[ Image Placeholder ]</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("**🎯 Confusion Matrix**")
                st.write("Shows True Positives, True Negatives, False Positives, and False Negatives")
                confusion_matrix_path = "utils/heart_confusion.jpeg"
                if os.path.exists(os.path.join(BASE_DIR, confusion_matrix_path)):
                    st.image(os.path.join(BASE_DIR, confusion_matrix_path), use_container_width=True)
                else:
                    st.markdown("<div style='height: 300px; background-color: black; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white;'>[ Image Placeholder ]</div>", unsafe_allow_html=True)
            
            st.markdown("")
            st.markdown("**🔍 Feature Importance Map**")
            st.write("Which cardiovascular factors matter most? Higher bars = more critical for heart disease risk assessment")
            feature_importance_path = "utils/heart_feature.jpeg"
            if os.path.exists(os.path.join(BASE_DIR, feature_importance_path)):
                st.image(os.path.join(BASE_DIR, feature_importance_path), use_container_width=True)
            else:
                st.markdown("<div style='height: 300px; background-color: black; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white;'>[ Image Placeholder ]</div>", unsafe_allow_html=True)
        else:
            st.markdown("##### 🩸 Blood Cancer Model Visualization Suite")
            
            st.markdown("**🎯 Confusion Matrix**")
            st.write("Shows True Positives, True Negatives, False Positives, and False Negatives")
            
            cm_path = "utils/blood_cancer_confusion.png"
            if os.path.exists(os.path.join(BASE_DIR, cm_path)):
                col_space_left, col_content, col_space_right = st.columns([1, 5, 1])
                with col_content:
                    st.image(os.path.join(BASE_DIR, cm_path), use_container_width=True)
            else:
                st.markdown("<div style='height: 300px; background-color: black; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white;'>[ Training Model... ]</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        
        
        # ── SECTION 4: KEY INSIGHTS & LEARNINGS ────────────────────────────
        st.markdown("<h2 style='color: #63b3ed;'>🧠 Key Insights & What Model Learned</h2>", unsafe_allow_html=True)
        
        if model_key == "diabetes":
            st.markdown("""
            <div class="model-info-box">
                <div class="model-info-title">📊 Model Insights from Diabetes Data</div>
                <div class="model-info-content">
                ✅ <strong>Glucose Level is Critical:</strong> Most important feature for diabetes prediction<br><br>
                ✅ <strong>BMI & Age Correlation:</strong> Combined effect stronger than individual impact<br><br>
                ✅ <strong>Pregnancy History Matters:</strong> Gestational diabetes increases risk<br><br>
                ✅ <strong>Insulin Sensitivity:</strong> Insulin levels show strong pattern in predictions<br><br>
                ✅ <strong>Non-linear Relationships:</strong> Simple threshold doesn't work - complex interactions detected
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif model_key == "heart":
            st.markdown("""
            <div class="model-info-box">
                <div class="model-info-title">📊 Model Insights from Heart Disease Data</div>
                <div class="model-info-content">
                ✅ <strong>Cholesterol is Dominant:</strong> Strongest predictor of heart disease risk<br><br>
                ✅ <strong>Age × Blood Pressure Interaction:</strong> Older patients with high BP at extreme risk<br><br>
                ✅ <strong>Chest Pain Type Patterns:</strong> Specific pain types show strong correlation<br><br>
                ✅ <strong>Smoking + Cholesterol:</strong> Dangerous combination identified by model<br><br>
                ✅ <strong>Non-linear Risk Escalation:</strong> Risk doesn't increase linearly - threshold effects detected
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="model-info-box">
                <div class="model-info-title">📊 Model Insights from Blood Cancer Images</div>
                <div class="model-info-content">
                ✅ <strong>Cell Morphology:</strong> Model strongly identifies chromatin clumping and irregular nuclear shapes.<br><br>
                ✅ <strong>Cytoplasm Ratio:</strong> High nucleus-to-cytoplasm ratio is a key indicator of ALL.<br><br>
                ✅ <strong>Deep Features:</strong> ResNet-18 learned hierarchical spatial patterns that are invisible to the naked eye.<br><br>
                ✅ <strong>Color Invariance:</strong> The model has generalized across slight variations in staining colors due to data augmentation.<br><br>
                ✅ <strong>High Confidence:</strong> True positives are usually detected with high confidence due to residual connections.
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
