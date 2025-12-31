from utils.image_ai_check import check_image_ai_fake

print("🔍 RakshaKAI Deepfake Detection Started\n")

image_path = "data/images/test.jpg"  # replace with any image
img_result, confidence = check_image_ai_fake(image_path)
print(f"🖼 Image Analysis : ({img_result}, {confidence}%)")

print("\n🤖 FINAL VERDICT : ✅ ANALYSIS COMPLETE")
