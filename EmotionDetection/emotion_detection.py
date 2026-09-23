"""Watson emotion analysis with bounded requests and validated scores."""
import math
import requests

EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")
URL = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"

class EmotionServiceError(RuntimeError):
    """Remote service unavailable or invalid response."""

def emotion_detector(text_to_analyse):
    """Analyze English text without making a network request for blank input."""
    if not isinstance(text_to_analyse, str) or not text_to_analyse.strip():
        return dict.fromkeys((*EMOTIONS, "dominant_emotion"))
    try:
        response = requests.post(
            URL, json={"raw_document": {"text": text_to_analyse.strip()}},
            headers={"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"},
            timeout=(5, 20),
        )
        if response.status_code == 400:
            return dict.fromkeys((*EMOTIONS, "dominant_emotion"))
        response.raise_for_status()
        emotions = response.json()["emotionPredictions"][0]["emotion"]
        scores = {name: emotions[name] for name in EMOTIONS}
        if any(isinstance(v, bool) or not isinstance(v, (int, float))
               or not math.isfinite(v) or not 0 <= v <= 1 for v in scores.values()):
            raise ValueError("Invalid scores")
    except (requests.RequestException, ValueError, KeyError, IndexError, TypeError) as exc:
        raise EmotionServiceError("Emotion service unavailable") from exc
    return {**scores, "dominant_emotion": max(scores, key=scores.get)}
