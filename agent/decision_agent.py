def final_decision(image_result, audio_result):

    if "NOT FOUND" in audio_result or "ERROR" in audio_result:
        return "❌ INCOMPLETE ANALYSIS (Audio Missing)"

    if "FAKE" in image_result or "FAKE" in audio_result:
        return "⚠️ DEEPFAKE SUSPECTED"

    if "REAL" in image_result and "REAL" in audio_result:
        return "✅ MEDIA AUTHENTIC"

    return "❓ UNDETERMINED"
