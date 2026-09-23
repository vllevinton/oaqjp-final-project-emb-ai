"""Local Flask interface for the Watson NLP educational project."""
from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import EmotionServiceError, emotion_detector

app = Flask("Emotion Detector")


@app.route("/emotionDetector")
def sent_detector():
    """Analyze input and expose clear input/provider errors."""
    text_to_analyze = request.args.get("textToAnalyze")

    if text_to_analyze and len(text_to_analyze) > 5000:
        return "Please enter at most 5000 characters.", 400
    try:
        response = emotion_detector(text_to_analyze)
    except EmotionServiceError:
        return "Emotion service unavailable. Please try again later.", 503

    if response["dominant_emotion"] is None:
        return "Invalid text! Please try again!", 400

    return (
        f"For the given statement, the system response is "
        f"'anger': {response['anger']}, "
        f"'disgust': {response['disgust']}, "
        f"'fear': {response['fear']}, "
        f"'joy': {response['joy']} and "
        f"'sadness': {response['sadness']}. "
        f"The dominant emotion is {response['dominant_emotion']}."
    )


@app.route("/")
def render_index_page():
    """Display the input form."""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
