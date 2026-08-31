const API_URL = "http://127.0.0.1:8000";

const fileInput = document.getElementById("fileInput");
const uploadButton = document.getElementById("uploadButton");
const uploadStatus = document.getElementById("uploadStatus");

const questionInput = document.getElementById("questionInput");
const askButton = document.getElementById("askButton");
const answer = document.getElementById("answer");


uploadButton.addEventListener("click", async () => {
    const file = fileInput.files[0];

    if (!file) {
        uploadStatus.textContent = "Please select a PDF file first.";
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    uploadButton.disabled = true;
    uploadStatus.textContent = "Uploading and indexing document...";

    try {
        const response = await fetch(`${API_URL}/documents/upload`, {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Upload failed.");
        }

        uploadStatus.textContent =
            `${data.filename} uploaded successfully. ` +
            `${data.chunks_indexed} chunks indexed.`;

    } catch (error) {
        uploadStatus.textContent = `Error: ${error.message}`;
    } finally {
        uploadButton.disabled = false;
    }
});


askButton.addEventListener("click", async () => {
    const question = questionInput.value.trim();

    if (!question) {
        answer.textContent = "Please enter a question.";
        return;
    }

    askButton.disabled = true;
    answer.textContent = "Thinking...";

    try {
        const response = await fetch(`${API_URL}/ask`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Failed to get answer.");
        }

        answer.textContent = data.answer;

    } catch (error) {
        answer.textContent = `Error: ${error.message}`;
    } finally {
        askButton.disabled = false;
    }
});