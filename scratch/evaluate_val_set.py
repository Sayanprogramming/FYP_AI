import os
import sys
import csv

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controllers.blood_cancer_services import predict_from_image

val_images_dir = r"c:\Users\sayan\Desktop\Final_Prj\models\blood cancer_model\dataset\val\images"
val_labels_csv = r"c:\Users\sayan\Desktop\Final_Prj\models\blood cancer_model\dataset\val\labels.csv"

all_count = 0
hem_count = 0
total_evaluated = 0

with open(val_labels_csv, "r", newline="") as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        fname = row["new_names"].strip()
        filepath = os.path.join(val_images_dir, fname)
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, "rb") as img_f:
            img_bytes = img_f.read()
            
        pred_class, conf = predict_from_image(img_bytes)
        if "ALL" in pred_class.upper():
            all_count += 1
        else:
            hem_count += 1
        total_evaluated += 1
        
        # Stop after 200 for a quick check
        if total_evaluated >= 200:
            break

print(f"Total evaluated: {total_evaluated}")
print(f"Predicted ALL (Cancerous): {all_count}")
print(f"Predicted HEM (Healthy): {hem_count}")
