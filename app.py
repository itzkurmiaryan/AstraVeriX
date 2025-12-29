import streamlit as st
from utils.image_ai_check import check_image_ai_fake
from PIL import Image
import os

st.set_page_config(page_title="RakshaKAI", layout="centered")

st.title("🛡️ RakshaKAI – AI Image Deepfake Detector")

uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    os.makedirs("data/uploads", exist_ok=True)
    image_path = f"data/uploads/{uploaded_file.name}"

    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image(image_path, caption="Uploaded Image", use_container_width=True)

    with st.spinner("🔍 Analyzing image..."):
        result, confidence = check_image_ai_fake(image_path)

    st.subheader("🤖 AI Result")
    st.write(f"**Result:** {result}")
    st.write(f"**Confidence:** {confidence}%")
