async function runEmotionDetection() {
  const text = document.getElementById("textToAnalyze").value;
  const result = document.getElementById("result");
  const button = document.querySelector("button");
  button.disabled = true;
  result.textContent = "Analyzing…";
  try {
    const response = await fetch("/emotionDetector?textToAnalyze=" + encodeURIComponent(text));
    result.textContent = await response.text();
  } catch {
    result.textContent = "Could not connect. Please try again.";
  } finally {
    button.disabled = false;
  }
}
