const API_BASE = window.location.origin + "/api"; // works both locally and online
const fileListDiv = document.getElementById("fileList");

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
        uploadMsg.textContent = res.ok ? data.message : (data.detail || "Upload failed.");
    } catch (err) {
        console.error(err);
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
        console.error(err);
        const botMsg = document.createElement("div");
        botMsg.className = "message bot";
        botMsg.textContent = "Error getting answer.";
        chatDiv.appendChild(botMsg);
    }

    chatDiv.scrollTop = chatDiv.scrollHeight;
}

async function listFiles() {
    if (!fileListDiv) return;
    try {
        const res = await fetch(`${API_BASE}/files/`);
        const files = await res.json();
        fileListDiv.innerHTML = "";
        if (!files.length) {
            fileListDiv.textContent = "No files uploaded.";
            return;
        }
        files.forEach(file => {
            const div = document.createElement("div");
            div.className = "file-item";
            div.innerHTML = `
                <strong>${file.filename}</strong> 
                <em>(uploaded ${new Date(file.upload_time).toLocaleString()})</em><br>
                Chunks: ${file.num_chunks}<br>
                Preview: ${file.preview}
            `;
            fileListDiv.appendChild(div);
        });
    } catch (err) {
        console.error(err);
        fileListDiv.textContent = "Error fetching files.";
    }
}