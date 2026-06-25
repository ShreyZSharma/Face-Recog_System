# Face and emotion analysis using DeepFace

from deepface import DeepFace

def analyze_mood(frame):
    try:
        result = DeepFace.analyze(
            frame,
            actions=["emotion"],
            enforce_detection=True,
            silent=True
        )
        emotion = result[0]["dominant_emotion"]
        scores = {k: float(v) for k, v in result[0]["emotion"].items()}
        return emotion, scores
    except Exception:
        return None, None