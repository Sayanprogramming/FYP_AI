import os #added for relative paths
import pandas as pd
import joblib
# Get the base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SCALER_PATH = os.path.join(BASE_DIR, "models", "heart disease_pred_model", "heart_scaler.joblib")
MODEL_PATH  = os.path.join(BASE_DIR, "models", "heart disease_pred_model", "heart_model.joblib")

# Load model and scaler
scaler = joblib.load(SCALER_PATH)
model = joblib.load(MODEL_PATH)

FEATURE_ORDER = [
    "Age","Gender","Smoking","Alcohol","Exercise (per week)","Diet Quality",
    "Overweight","Stress Level","Blood Pressure","Cholesterol",
    "Family History","Chest Pain","Shortness of Breath","Diabetes"
]

def predict_disease(user_input_df: pd.DataFrame):
    user_input_df = user_input_df[FEATURE_ORDER]
    user_input_std = scaler.transform(user_input_df)
    pred = model.predict(user_input_std)[0]
    proba = model.predict_proba(user_input_std)[0,1]
    return int(pred), float(proba)
