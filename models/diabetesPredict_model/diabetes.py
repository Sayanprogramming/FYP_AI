import pandas as pd
import os
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier

from sklearn.preprocessing import StandardScaler, MinMaxScaler # MinMaxScaler used for Normalization



# load dataset
df = pd.read_csv('diabetes_dataset.csv')


x = df.drop('Outcome', axis=1)
y = df['Outcome']


# train test split dataset
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)


# train model
model = RandomForestClassifier()
model.fit(x_train, y_train)


# save model

# os.makedirs("", exist_ok=True)
joblib.dump(model, "diabetes_model.joblib")


# model evaluation
y_pred = model.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)




print("--------------------- Model trained and saved successfully ------------------- ")


print(f"Model Accuracy: {accuracy * 100:.2f}%")


# classification report
report = classification_report(y_test, y_pred)
print(report)


print("✅ Model trained and saved as 'diabetes_model.joblib' ")