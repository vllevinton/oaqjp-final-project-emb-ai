# Emotion Detection — Watson NLP + Flask

## Emotion Detection Project

Final project for the IBM/Coursera course Developing AI Applications with Python and Flask.

## Current verification status

Educational IBM/Coursera project; the model is provided by Watson, not trained in this repository. The Skills Network service did not respond from the validation environment on 2026-09-23. Live inference is therefore **not currently verified**. Local tests mock the provider; the app returns HTTP 503 on service failures and HTTP 400 on invalid input.

Input text is sent to the external Watson service. Use non-sensitive English sample text.

## Features

- Emotion analysis using the Watson NLP Emotion Predict endpoint.
- Scores for anger, disgust, fear, joy, and sadness.
- Dominant-emotion detection.
- Flask web interface.
- Blank-input error handling.
- Unit tests.
- PEP 8 / pylint-friendly structure.

## Project structure

```text
EmotionDetection/
  __init__.py
  emotion_detection.py
static/
  mywebscript.js
templates/
  index.html
server.py
test_emotion_detection.py
requirements.txt
```

## Run

```bash
pip install -r requirements.txt
python server.py
```

Then open `http://localhost:5000/`.

## Tests

```bash
python -m unittest discover -v
```

## Static analysis

```bash
pylint server.py
```

Live integration tests are opt-in: set `RUN_WATSON_INTEGRATION=1` before running the test suite. Five live tests are skipped by default. Mocked unit tests do not establish that the external service is available.
