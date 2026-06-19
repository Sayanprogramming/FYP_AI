import os
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models", "blood_cancer_model")
MODEL_PATH = os.path.join(MODEL_DIR, "best_model.pth")

torch = None
transforms = None
DEVICE = None
TRANSFORM = None
MODEL = None


def ensure_torch():
    global torch, transforms, DEVICE, TRANSFORM
    if torch is not None:
        return

    try:
        import torch as _torch
        from torchvision import transforms as _transforms
    except ImportError as exc:
        raise ImportError(
            "PyTorch and torchvision are required for blood cancer prediction. "
            "Install them with `pip install torch torchvision` in your project environment."
        ) from exc

    torch = _torch
    transforms = _transforms
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    TRANSFORM = transforms.Compose([
        transforms.Resize((64, 64)),
        transforms.ToTensor()
    ])


def load_model():
    ensure_torch()

    model = torch.nn.Sequential(
        torch.nn.Conv2d(3, 16, kernel_size=3, padding=1),
        torch.nn.ReLU(),
        torch.nn.MaxPool2d(2),

        torch.nn.Conv2d(16, 32, kernel_size=3, padding=1),
        torch.nn.ReLU(),
        torch.nn.MaxPool2d(2),

        torch.nn.Flatten(),
        torch.nn.Linear(32 * 16 * 16, 128),
        torch.nn.ReLU(),
        torch.nn.Dropout(0.5),
        torch.nn.Linear(128, 2)
    ).to(DEVICE)

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Blood cancer model file not found at {MODEL_PATH}. "
            "Please place your trained weights as best_model.pth in models/blood_cancer_model/."
        )

    model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
    model.eval()
    return model


def get_model():
    global MODEL
    if MODEL is None:
        MODEL = load_model()
    return MODEL


def predict_image(image: Image.Image):
    ensure_torch()
    model = get_model()

    if not isinstance(image, Image.Image):
        image = Image.open(image)

    image = image.convert("RGB")
    image = TRANSFORM(image).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        output = model(image)
        probabilities = torch.softmax(output, dim=1)[0]
        pred = int(output.argmax(dim=1).item())
        confidence = float(probabilities[pred])

    # 0 -> Cancer, 1 -> Normal
    return pred, confidence
