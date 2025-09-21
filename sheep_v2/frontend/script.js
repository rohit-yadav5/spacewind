const API_BASE = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
  ? "http://127.0.0.1:8000/api"
  : "https://sheep.spacewind.xyz/api";

async function uploadFile() {
    const fileInput = document.getElementById("fileInput");
    const uploadMsg = document.getElementById("uploadMsg");
    if (!fileInput || !fileInput.files.length) {
        uploadMsg.textContent = "Please select a file to upload.";
        return;
    }
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", file);
    try {
        const res = await fetch(`${API_BASE}/upload/`, {
            method: "POST",
            body: formData
        });
        const data = await res.json();
        if (res.ok) {
            uploadMsg.textContent = data.message;
        } else {
            uploadMsg.textContent = data.detail || "Upload failed.";
        }
    } catch (err) {
        uploadMsg.textContent = "Error uploading file.";
    }
}

async function askQuestion() {
    const questionInput = document.getElementById("question");
    const chatDiv = document.getElementById("chat");
    const question = questionInput.value.trim();
    if (!question) return;

    // Append user message
    const userMsg = document.createElement("div");
    userMsg.className = "message user";
    userMsg.textContent = question;
    chatDiv.appendChild(userMsg);

    questionInput.value = "";

    // Fetch bot answer
    try {
        const res = await fetch(`${API_BASE}/query/?question=${encodeURIComponent(question)}`, {
            method: "POST"
        });
        const data = await res.json();
        const botMsg = document.createElement("div");
        botMsg.className = "message bot";
        botMsg.textContent = data.answer || "No answer.";
        chatDiv.appendChild(botMsg);
    } catch (err) {
        const botMsg = document.createElement("div");
        botMsg.className = "message bot";
        botMsg.textContent = "Error getting answer.";
        chatDiv.appendChild(botMsg);
    }

    chatDiv.scrollTop = chatDiv.scrollHeight;
}