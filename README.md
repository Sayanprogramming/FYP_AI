# 🏥 AI-Powered Health Recommendation System

An AI-based system that predicts possible health conditions based on patient-provided symptoms and suggests preventive measures or next steps.  

Developed as a **Final Year Project** by **Sayan, Arijit, Debaroti, and Joymalya**.

---

## 📌 Project Overview
The **AI-Powered Health Recommendation System** is designed to help individuals make informed decisions about their health by analyzing symptoms and providing relevant recommendations.

This system leverages **Machine Learning** to process patient data and generate possible health risks, along with advice for seeking professional medical help.

> ⚠️ **Disclaimer:** This tool is for **educational purposes only** and should not replace professional medical diagnosis.

---

## 🚀 Features
- 🩺 **Symptom-based disease prediction**
- 📊 **Data-driven AI recommendations**
- 📁 **Customizable dataset support**
- 💡 **User-friendly interface**
- 📱 **Scalable for web or mobile integration**

---

## 🛠️ Tech Stack
- **Programming Language:** Python  
- **Libraries & Frameworks:** Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn  
- **Frontend:** Streamlit  
- **Database:**CSV datasets  
- **Version Control:** Git & GitHub  

---# 🏥 AI-Powered Health Recommendation System  

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)  
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)  
[![Streamlit](https://img.shields.io/badge/Powered%20By-Streamlit-FF4B4B?logo=streamlit)](https://streamlit.io/)  

## 📂 Project Structure  

```plaintext

│
├── 📜 README.md                # Project documentation
├── 📜 requirements.txt         # List of dependencies
│
├── 🗃️ dataset/                  # Datasets for training & testing
│   ├── symptoms_dataset.csv     # Symptom-to-disease mapping data
│   ├── heart_disease_dataset.csv# Heart disease training data
│   ├── diabetes_dataset.csv     # Diabetes training data
│   └── diseases_info.csv        # General disease information
│
├── 📂 models/                   # Saved ML/DL models for different diseases
│   ├── general_health_model.pkl # General symptom-based model
│   ├── heart_disease_model.pkl  # ❤️ Heart disease prediction model
│   └── diabetes_model.pkl       # 🍬 Diabetes prediction model
│
├── 📂 src/                      # Main source code
│   ├── __init__.py              # Marks the folder as a package
│   ├── data_preprocessing.py    # Data cleaning & preparation
│   ├── train_model.py           # Model training script
│   ├── predict.py               # Prediction logic
│   └── utils.py                 # Helper functions
│
├── 📂 app/                      # Frontend interface
│   └── streamlit_app.py         # Streamlit web app for predictions
│
└── 📂 tests/                    # Unit tests for code & models
    ├── test_model.py            # Tests for ML models
    └── test_api.py              # Tests for app/API endpoints
