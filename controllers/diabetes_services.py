import numpy as np
import joblib
import os
import pandas as pd

# Get the base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load scaler and model
scaler = joblib.load(os.path.join(BASE_DIR, "models", "diabetesPredict_model", "diabetes_scaler.joblib"))
model = joblib.load(os.path.join(BASE_DIR, "models", "diabetesPredict_model", "diabetes_model.joblib"))



def predict_disease(user_input_df):


    # Standardize user input
    user_input_std = scaler.transform(user_input_df)
    user_input_std_df = pd.DataFrame(user_input_std, columns=user_input_df.columns)

    # Predict
    prediction = model.predict(user_input_std_df)[0]
    probability = model.predict_proba(user_input_std_df)[0][1]

    return [prediction, probability]
