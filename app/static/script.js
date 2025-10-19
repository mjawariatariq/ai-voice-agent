document.addEventListener("DOMContentLoaded", () => {
  const recordBtn = document.getElementById("recordBtn");
  const statusText = document.getElementById("status");
  const userText = document.getElementById("userText");
  const aiReply = document.getElementById("aiReply");
  const languageSelect = document.getElementById("language");

  let mediaRecorder, chunks = [];

  recordBtn.addEventListener("click", async () => {
    if (!mediaRecorder || mediaRecorder.state === "inactive") {
      await startRecording();
    } else {
      stopRecording();
    }
  });

  async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    chunks = [];

    mediaRecorder.ondataavailable = e => chunks.push(e.data);
    mediaRecorder.onstop = sendToServer;

    mediaRecorder.start();
    statusText.textContent = "🎙️ Recording... click again to stop.";
    recordBtn.textContent = "⏹️ Stop Recording";
  }

  function stopRecording() {
    mediaRecorder.stop();
    recordBtn.textContent = "🎤 Start Recording";
    statusText.textContent = "Processing...";
  }

  async function sendToServer() {
    const blob = new Blob(chunks, { type: "audio/wav" });
    const formData = new FormData();
    formData.append("file", blob, "input.wav");
    formData.append("lang", languageSelect.value);

    try {
      const res = await fetch("/voice_vad", { method: "POST", body: formData });
      const data = await res.json();

      userText.textContent = data.user_text;
      aiReply.textContent = data.ai_reply;

      const utterance = new SpeechSynthesisUtterance(data.ai_reply);
      utterance.lang = languageSelect.value === "ur" ? "ur-PK" : "en-US";
      speechSynthesis.speak(utterance);

      statusText.textContent = "✅ Done!";
    } catch (err) {
      console.error(err);
      statusText.textContent = "❌ Failed to process audio";
    }
  }
});
