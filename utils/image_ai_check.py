import torch
from torchvision import transforms
from PIL import Image
from utils.image_ai_model import SimpleCNN
import pickle
import os

MODEL_PATH = "data/models/image_cnn.pth"

def check_image_ai_fake(image_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = SimpleCNN()

    if os.path.exists(MODEL_PATH):
        try:
            model.load_state_dict(torch.load(MODEL_PATH, map_location=device, weights_only=False))
            print("✅ Model loaded")
        except pickle.UnpicklingError:
            print("⚠️ Model incompatible, demo mode")
    else:
        print("⚠️ Model not found, demo mode")

    model.to(device)
    model.eval()

    img = Image.open(image_path).convert("RGB")

    transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor()
    ])

    img_tensor = transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(img_tensor)
        prob = torch.softmax(output, dim=1)
        confidence, pred = torch.max(prob, 1)

    return ("LIKELY FAKE" if pred.item() == 1 else "LIKELY REAL",
            round(confidence.item() * 100, 2))
