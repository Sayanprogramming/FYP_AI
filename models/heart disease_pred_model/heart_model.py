import pandas as pd
import os
import json
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    precision_score, recall_score, f1_score, confusion_matrix,
    classification_report, roc_curve, roc_auc_score
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

RANDOM_STATE = 42  

# === Paths ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # current script folder
DATASET_PATH = os.path.join(BASE_DIR, "heart_disease_dataset.csv")
SAVE_DIR = os.path.join(BASE_DIR, "artifacts")  # outputs saved here


def load_dataset(path=DATASET_PATH):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Dataset not found at {path}")
    df = pd.read_csv(path)
    if "Heart Disease" not in df.columns:
        raise ValueError("Dataset must contain a 'Heart Disease' column as target.")
    return df


def train(save_dir=SAVE_DIR, dataset_path=DATASET_PATH):
    os.makedirs(save_dir, exist_ok=True)

    # Load dataset
    df = load_dataset(dataset_path)
    X = df.drop(columns=["Heart Disease"])
    y = df["Heart Disease"]

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train the model
    model = XGBClassifier(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=5,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=RANDOM_STATE,
        eval_metric="logloss"
    )
    model.fit(X_train_scaled, y_train)

    # Predictions
    y_pred = model.predict(X_test_scaled)
    y_proba = model.predict_proba(X_test_scaled)[:, 1]  # for ROC curve

    # Metrics
    accuracy = model.score(X_test_scaled, y_test)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_proba)

    # Save artifacts
    joblib.dump(scaler, os.path.join(save_dir, "heart_scaler.joblib"))
    joblib.dump(model, os.path.join(save_dir, "heart_model.joblib"))

    # Default sample for UI
    default = X.iloc[0].to_dict()
    with open(os.path.join(save_dir, "testing_dataset.json"), "w") as f:
        json.dump(default, f, indent=2)

    # Save metrics
    metrics = {
        "test_accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1),
        "auc": float(auc)
    }
    with open(os.path.join(save_dir, "metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)

    # === Confusion Matrix Plot ===
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=["No Disease", "Disease"],
                yticklabels=["No Disease", "Disease"])
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix - Heart Disease Prediction")
    plt.tight_layout()
    plt.show()

    # === ROC Curve Plot ===
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    plt.figure(figsize=(6, 5))
    plt.plot(fpr, tpr, label=f"AUC = {auc:.4f}")
    plt.plot([0, 1], [0, 1], "k--")  # diagonal line
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve - Heart Disease Prediction")
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.show()

    # Print results
    print(f"✅ Training completed.")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-score: {f1:.4f}")
    print(f"AUC: {auc:.4f}")
    print("\nClassification Report:\n", classification_report(y_test, y_pred))


if __name__ == "__main__":
    train()
