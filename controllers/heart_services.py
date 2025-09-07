import pandas as pd
import joblib

SCALER_PATH = "C:/Users/sayan/OneDrive/Desktop/FYP_AI/models/heart disease_pred_model/heart_scaler.joblib"
MODEL_PATH = "C:/Users/sayan/OneDrive/Desktop/FYP_AI/models/heart disease_pred_model/heart_model.joblib"

scaler = joblib.load(SCALER_PATH)
model = joblib.load(MODEL_PATH)

# Make sure the order of features matches training
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