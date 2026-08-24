"""Emotion detection using IBM Watson NLP."""
import requests

URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
HEADERS = {
    "grpc-metadata-mm-model-id":
        "emotion_aggregated-workflow_lang_en_stock"
}


def _empty_result():
    """Return the standard empty result used for invalid input."""
    return {
        "anger": None,
        "disgust": None,
        "fear": None,
        "joy": None,
        "sadness": None,
        "dominant_emotion": None,
    }


def emotion_detector(text_to_analyze):
    """Analyze text and return emotion scores plus the dominant emotion."""
    if not text_to_analyze or not text_to_analyze.strip():
        return _empty_result()

    payload = {"raw_document": {"text": text_to_analyze}}

    try:
        response = requests.post(
            URL,
            json=payload,
            headers=HEADERS,
            timeout=10,
        )
    except requests.RequestException:
        return _empty_result()

    if response.status_code == 400:
        return _empty_result()

    try:
        response.raise_for_status()
        response_data = response.json()
        emotions = response_data["emotionPredictions"][0]["emotion"]
    except (requests.RequestException, KeyError, IndexError, TypeError, ValueError):
        return _empty_result()

    scores = {
        "anger": emotions.get("anger"),
        "disgust": emotions.get("disgust"),
        "fear": emotions.get("fear"),
        "joy": emotions.get("joy"),
        "sadness": emotions.get("sadness"),
    }
    valid_scores = {
        name: value for name, value in scores.items()
        if isinstance(value, (int, float))
    }
    dominant = max(valid_scores, key=valid_scores.get) if valid_scores else None

    return {**scores, "dominant_emotion": dominant}
