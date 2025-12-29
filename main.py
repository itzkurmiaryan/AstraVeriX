from utils.image_ai_check import check_image_ai_fake

print("🔍 RakshaKAI Deepfake Detection Started\n")

# Image Analysis
image_path = "data/images/test.jpg"
img_result, confidence = check_image_ai_fake(image_path)
print(f"🖼 Image Analysis : ({img_result}, {confidence}%)")

# Audio Analysis (demo placeholder)
audio_file = "data/audio/test.wav"  # Replace with actual audio file path
try:
    # TODO: Add actual audio analysis code here
    print("🔊 Audio Analysis : AUDIO FILE NOT FOUND")
except:
    print("🔊 Audio Analysis : AUDIO FILE NOT FOUND")

# Final Verdict
if "INVALID" in img_result:
    print("\n🤖 FINAL VERDICT : ❌ INVALID INPUT")
elif "NOT FOUND" in "AUDIO FILE NOT FOUND":
    print("\n🤖 FINAL VERDICT : ❌ INCOMPLETE ANALYSIS (Audio Missing)")
else:
    print("\n🤖 FINAL VERDICT : ✅ ANALYSIS COMPLETE")
