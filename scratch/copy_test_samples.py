import os
import sys
import shutil
import csv

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controllers.blood_cancer_services import predict_from_image

val_images_dir = r"c:\Users\sayan\Desktop\Final_Prj\models\blood cancer_model\dataset\val\images"
val_labels_csv = r"c:\Users\sayan\Desktop\Final_Prj\models\blood cancer_model\dataset\val\labels.csv"
dest_dir = r"c:\Users\sayan\Desktop\Final_Prj\models\blood cancer_model\test_samples"

os.makedirs(dest_dir, exist_ok=True)

correct_all = []
correct_hem = []

with open(val_labels_csv, "r", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        fname = row["new_names"].strip()
        raw_label = int(row["labels"]) # 1 = ALL (cancer), 0 = HEM (healthy)
        
        filepath = os.path.join(val_images_dir, fname)
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, "rb") as img_f:
            img_bytes = img_f.read()
            
        pred_class, conf = predict_from_image(img_bytes)
        is_pred_cancerous = "ALL" in pred_class.upper()
        is_expected_cancerous = (raw_label == 1)
        
        # Check correctness
        if is_pred_cancerous == is_expected_cancerous:
            if is_expected_cancerous and len(correct_all) < 4:
                correct_all.append((fname, conf))
                # Copy to dest
                shutil.copy(filepath, os.path.join(dest_dir, f"cancerous_{len(correct_all)}.bmp"))
            elif not is_expected_cancerous and len(correct_hem) < 4:
                correct_hem.append((fname, conf))
                # Copy to dest
                shutil.copy(filepath, os.path.join(dest_dir, f"healthy_{len(correct_hem)}.bmp"))
                
        if len(correct_all) >= 4 and len(correct_hem) >= 4:
            break

print("Found correct cancerous cells:")
for i, (fname, conf) in enumerate(correct_all):
    print(f"  {fname} -> cancerous_{i+1}.bmp (Confidence: {conf:.4f})")

print("Found correct healthy cells:")
for i, (fname, conf) in enumerate(correct_hem):
    print(f"  {fname} -> healthy_{i+1}.bmp (Confidence: {conf:.4f})")

print("Done! Files copied to:", dest_dir)
