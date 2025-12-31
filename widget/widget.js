const API_URL = "http://127.0.0.1:5000/chat";

const widget = document.getElementById("apk-widget");
const toggle = document.getElementById("apk-toggle");
const sendBtn = document.getElementById("apk-send");
const input = document.getElementById("apk-text");
const messages = document.getElementById("apk-messages");

let sessionId = localStorage.getItem("apk_session_id");

toggle.onclick = () => {
  widget.style.display = widget.style.display === "flex" ? "none" : "flex";
};

function addMessage(text, type) {
  const div = document.createElement("div");
  div.className = `apk-msg ${type}`;
  div.textContent = text;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

sendBtn.onclick = sendMessage;
input.addEventListener("keydown", e => {
  if (e.key === "Enter") sendMessage();
});

function sendMessage() {
  const text = input.value.trim();
  if (!text) return;

  addMessage(text, "apk-user");
  input.value = "";

  fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message: text,
      session_id: sessionId
    })
  })
  .then(res => res.json())
  .then(data => {
    addMessage(data.reply, "apk-bot");

    if (data.session_id) {
      sessionId = data.session_id;
      localStorage.setItem("apk_session_id", sessionId);
    }
  })
  .catch(() => {
    addMessage("Blad polaczenia z serwerem.", "apk-bot");
  });
}
