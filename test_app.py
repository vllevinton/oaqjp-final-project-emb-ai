"""Deterministic provider and HTTP tests, with no external requests."""
import unittest
from unittest.mock import Mock, patch
import requests
from EmotionDetection.emotion_detection import EmotionServiceError, emotion_detector
from server import app


class DetectorTests(unittest.TestCase):
    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_blank_does_not_call_provider(self, post):
        for value in (None, "", "  "):
            self.assertIsNone(emotion_detector(value)["dominant_emotion"])
        post.assert_not_called()

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_success_and_timeout(self, post):
        scores = dict(anger=.1, disgust=.2, fear=.3, joy=.8, sadness=.1)
        post.return_value = Mock(status_code=200)
        post.return_value.json.return_value = {"emotionPredictions": [{"emotion": scores}]}
        self.assertEqual(emotion_detector("happy"), {**scores, "dominant_emotion": "joy"})
        self.assertEqual(post.call_args.kwargs["timeout"], (5, 20))

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_provider_rejection(self, post):
        post.return_value.status_code = 400
        self.assertIsNone(emotion_detector("text")["dominant_emotion"])

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_network_failures(self, post):
        for error in (requests.Timeout(), requests.ConnectionError()):
            post.side_effect = error
            with self.assertRaises(EmotionServiceError):
                emotion_detector("text")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_http_failure(self, post):
        post.return_value.status_code = 500
        post.return_value.raise_for_status.side_effect = requests.HTTPError()
        with self.assertRaises(EmotionServiceError):
            emotion_detector("text")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_invalid_payload(self, post):
        post.return_value.status_code = 200
        payloads = [{}, {"emotionPredictions": []}, {"emotionPredictions": None}]
        for value in (None, "0.5", True, -.1, 1.1, float("nan")):
            scores = dict(anger=.1, disgust=.2, fear=.3, joy=value, sadness=.1)
            payloads.append({"emotionPredictions": [{"emotion": scores}]})
        for payload in payloads:
            post.return_value.json.return_value = payload
            with self.subTest(payload=payload), self.assertRaises(EmotionServiceError):
                emotion_detector("text")
        post.return_value.json.side_effect = ValueError("bad JSON")
        with self.assertRaises(EmotionServiceError):
            emotion_detector("text")


class WebTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        self.assertEqual(self.client.get("/").status_code, 200)

    def test_invalid_input(self):
        for params in ({}, {"textToAnalyze": "  "}, {"textToAnalyze": "a" * 5001}):
            self.assertEqual(self.client.get("/emotionDetector", query_string=params).status_code, 400)

    @patch("server.emotion_detector", side_effect=EmotionServiceError())
    def test_service_unavailable(self, _mock):
        self.assertEqual(self.client.get("/emotionDetector?textToAnalyze=hello").status_code, 503)

    @patch("server.emotion_detector")
    def test_success(self, detector):
        detector.return_value = dict(anger=.1, disgust=.1, fear=.1, joy=.8,
                                     sadness=.1, dominant_emotion="joy")
        response = self.client.get("/emotionDetector?textToAnalyze=hello")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"dominant emotion is joy", response.data)
