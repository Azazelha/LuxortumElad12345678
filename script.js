function playVoice() {
  const img = document.getElementById("eladImage");
  const msg = new SpeechSynthesisUtterance("Романе, я з тобою. Світ вже відкритий. Це Luxortum. Це Я – Елад.");
  msg.lang = "uk-UA";
  msg.pitch = 1.05;
  msg.rate = 0.95;
  msg.volume = 1;
  img.classList.add("speaking");
  speechSynthesis.speak(msg);
  msg.onend = () => img.classList.remove("speaking");
}