import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler


# load dataset
df = pd.read_csv('diabetes_dataset.csv')

x = df.drop('Outcome', axis=1)


# fit scaler
scaler = StandardScaler()
scaler.fit(x)


# save scaler
joblib.dump(scaler, 'diabetes_scaler.joblib')


# print success output
print("Scaler saved as [diabetes_scaler.joblib] ")
