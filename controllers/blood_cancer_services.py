"""
Blood Cancer Detection — Inference Service
============================================
Loads the trained ResNet-18 model and provides a prediction function
that takes raw image bytes (from Streamlit file_uploader) and returns
the predicted class and confidence score.

Works entirely in-memory — no images are saved to disk.
"""

import os
import json
import io

import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models", "blood cancer_model")
MODEL_PATH = os.path.join(MODEL_DIR, "blood_cancer_model.pth")
CLASS_NAMES_PATH = os.path.join(MODEL_DIR, "class_names.json")

# ─── Constants ────────────────────────────────────────────────────────────────
IMAGE_SIZE = 128
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

# Friendly display names for each class
DISPLAY_NAMES = {
    "all": "ALL (Cancerous — Acute Lymphoblastic Leukemia)",
    "hem": "HEM (Healthy — Normal Cell)",
}

# ─── Inference Transform (same as validation) ────────────────────────────────
inference_transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
])

# ─── Load Model (lazy — only when model file exists) ─────────────────────────
_model = None
_class_names = None
_device = torch.device("cpu")


def _load_model():
    """Load model weights and class names from disk (called once, cached)."""
    global _model, _class_names

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Trained model not found at {MODEL_PATH}. "
            "Please run `python models/blood cancer_model/train_model.py` first."
        )

    # Load class names
    if os.path.exists(CLASS_NAMES_PATH):
        with open(CLASS_NAMES_PATH, "r") as f:
            _class_names = json.load(f).get("classes", ["all", "hem"])
    else:
        _class_names = ["all", "hem"]

    num_classes = len(_class_names)

    # Build the same model architecture used during training
    model = models.resnet18(weights=None)
    in_features = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Dropout(0.3),
        nn.Linear(in_features, num_classes),
    )

    # Load trained weights
    state_dict = torch.load(MODEL_PATH, map_location=_device, weights_only=True)
    model.load_state_dict(state_dict)
    model.eval()
    model.to(_device)

    _model = model
    return _model, _class_names


def _ensure_model():
    """Ensure the model is loaded before inference."""
    global _model, _class_names
    if _model is None:
        _load_model()
    return _model, _class_names


def predict_from_image(image_bytes: bytes) -> tuple:
    """
    Predict blood cancer from raw image bytes.

    Args:
        image_bytes: Raw image bytes (e.g. from Streamlit file_uploader).

    Returns:
        tuple: (predicted_class_display_name: str, confidence: float)
               e.g. ("ALL (Cancerous — Acute Lymphoblastic Leukemia)", 0.94)
    """
    model, class_names = _ensure_model()

    # Open image from bytes (in-memory, no disk write)
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # Apply transforms and add batch dimension
    input_tensor = inference_transform(image).unsqueeze(0).to(_device)

    # Inference
    with torch.no_grad():
        outputs = model(input_tensor)
        probabilities = torch.softmax(outputs, dim=1)
        confidence, predicted_idx = torch.max(probabilities, 1)

    predicted_class = class_names[predicted_idx.item()]
    confidence_value = confidence.item()

    # Map to friendly display name
    display_name = DISPLAY_NAMES.get(
        predicted_class.lower(),
        predicted_class,
    )

    return display_name, confidence_value


def is_model_available() -> bool:
    """Check whether the trained model file exists on disk."""
    return os.path.exists(MODEL_PATH)
