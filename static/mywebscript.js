async function runEmotionDetection() {
  const text = document.getElementById("textToAnalyze").value;
  const result = document.getElementById("result");
  const response = await fetch(
    "/emotionDetector?textToAnalyze=" + encodeURIComponent(text)
  );
  result.textContent = await response.text();
}
