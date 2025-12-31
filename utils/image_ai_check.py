import torch
from torchvision import models, transforms
from PIL import Image
import os

MODEL_PATH = "data/models/image_cnn_real_fake.pth"

def check_image_ai_fake(image_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = models.resnet18(pretrained=False)
    model.fc = torch.nn.Linear(model.fc.in_features, 2)
    model = model.to(device)

    if os.path.exists(MODEL_PATH):
        model.load_state_dict(torch.load(MODEL_PATH, map_location=device))

    model.eval()

    img = Image.open(image_path).convert("RGB")
    transform = transforms.Compose([
        transforms.Resize((256,256)),
        transforms.ToTensor(),
        transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
    ])
    img_tensor = transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(img_tensor)
        prob = torch.softmax(output, dim=1)
        confidence, pred = torch.max(prob, 1)

    # 🔁 LABEL FIX (REAL <-> FAKE)
    label = "REAL" if pred.item() == 1 else "FAKE"

    return label, round(confidence.item()*100,2)
