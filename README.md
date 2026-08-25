# Final Project

## Emotion Detection Project

Final project for the IBM/Coursera course Developing AI Applications with Python and Flask.

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
python -m unittest test_emotion_detection.py -v
```

## Static analysis

```bash
pylint server.py
```
