import os
import sys
import torch

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controllers.blood_cancer_services import predict_from_image, is_model_available

print("Model available:", is_model_available())

# Point to the test_samples directory
test_samples_dir = r"c:\Users\sayan\Desktop\Final_Prj\models\blood cancer_model\test_samples"

test_files = [
    ("cancerous_1.bmp", "ALL (Cancerous)"),
    ("cancerous_2.bmp", "ALL (Cancerous)"),
    ("cancerous_3.bmp", "ALL (Cancerous)"),
    ("cancerous_4.bmp", "ALL (Cancerous)"),
    ("healthy_1.bmp", "HEM (Healthy)"),
    ("healthy_2.bmp", "HEM (Healthy)"),
    ("healthy_3.bmp", "HEM (Healthy)"),
    ("healthy_4.bmp", "HEM (Healthy)"),
]

for filename, expected in test_files:
    filepath = os.path.join(test_samples_dir, filename)
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        continue
        
    with open(filepath, "rb") as f:
        img_bytes = f.read()
        
    pred_class, conf = predict_from_image(img_bytes)
    print(f"File: {filename:15s} | Expected: {expected:16s} | Predicted: {pred_class} (Conf: {conf:.4f})")
