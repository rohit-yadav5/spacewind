const API_BASE = window.location.pathname.startsWith('/app') 
    ? window.location.origin + '/app/api' 
    : window.location.origin + '/api'; // works both locally and online

const fileListDiv = document.getElementById('fileList');

async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const uploadMsg = document.getElementById('uploadMsg');
    if (!fileInput || !fileInput.files.length) {
        uploadMsg.textContent = 'Please select a file to upload.';
        return;
    }
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    try {
        const res = await fetch(`${API_BASE}/upload/`, {
            method: 'POST',
            body: formData
        });
        const data = await res.json();
        uploadMsg.textContent = res.ok ? data.message : (data.detail || 'Upload failed.');
        if (res.ok) listFiles(); // Refresh file list after upload
    } catch (err) {
        console.error(err);
        uploadMsg.textContent = 'Error uploading file.';
    }
}

async function askQuestion() {
    const questionInput = document.getElementById('question');
    const chatDiv = document.getElementById('chat');
    const question = questionInput.value.trim();
    if (!question) return;

    const userMsg = document.createElement('div');
    userMsg.className = 'message user';
    userMsg.textContent = question;
    chatDiv.appendChild(userMsg);
    questionInput.value = '';

    try {
        const res = await fetch(`${API_BASE}/query/?question=${encodeURIComponent(question)}`, {
            method: 'POST'
        });
        const data = await res.json();
        const botMsg = document.createElement('div');
        botMsg.className = 'message bot';
        botMsg.textContent = data.answer || 'No answer.';
        chatDiv.appendChild(botMsg);
    } catch (err) {
        console.error(err);
        const botMsg = document.createElement('div');
        botMsg.className = 'message bot';
        botMsg.textContent = 'Error getting answer.';
        chatDiv.appendChild(botMsg);
    }

    chatDiv.scrollTop = chatDiv.scrollHeight;
}

async function listFiles() {
    if (!fileListDiv) return;
    try {
        const res = await fetch(`${API_BASE}/files/`);
        const data = await res.json();
        const files = data.files || {};
        fileListDiv.innerHTML = '';
        if (!Object.keys(files).length) {
            fileListDiv.textContent = 'No files uploaded.';
            return;
        }
        for (const [filename, info] of Object.entries(files)) {
            const div = document.createElement('div');
            div.className = 'file-item';
            div.innerHTML = `
                <strong>${filename}</strong> 
                <em>(uploaded ${new Date(info.uploaded_at).toLocaleString()})</em><br>
                Chunks: ${info.chunks}<br>
                Preview: ${info.sample_content || 'N/A'}<br>
                <a href="${API_BASE}/download/${encodeURIComponent(filename)}" target="_blank">Download</a>
            `;
            fileListDiv.appendChild(div);
        }
    } catch (err) {
        console.error(err);
        fileListDiv.textContent = 'Error fetching files.';
    }
}

// Call listFiles on page load
window.addEventListener('DOMContentLoaded', listFiles);