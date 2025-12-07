const BASE_URL = "http://localhost:8000";

const statusIndicator = document.getElementById("status-indicator");
const consoleOutput = document.getElementById("console-output");
const filePathInput = document.getElementById("file-path");
const modeSelect = document.getElementById("mode-select");
const runAnalyzeBtn = document.getElementById("run-analyze");
const llmInstruction = document.getElementById("llm-instruction");
const runLlmBtn = document.getElementById("run-llm");
const runReportBtn = document.getElementById("run-report");
const chatMessagesEl = document.getElementById("chat-messages");
const chatInput = document.getElementById("chat-input");
const chatSendBtn = document.getElementById("chat-send");

let chatMessages = [];

function appendConsoleLine(text, type = "system") {
    const line = document.createElement("div");
    line.className = `console-line ${type}`;
    line.textContent = text;
    consoleOutput.appendChild(line);
    consoleOutput.scrollTop = consoleOutput.scrollHeight;
}

async function checkStatus() {
    try {
        const res = await fetch(`${BASE_URL}/status`);
        if (!res.ok) throw new Error("Status non OK");
        const data = await res.json();
        statusIndicator.textContent = data.status?.toUpperCase() || "ONLINE";
        statusIndicator.style.background = "rgba(0, 200, 120, 0.2)";
        appendConsoleLine("[system] Collegato a Super Agent API.", "system");
    } catch (err) {
        statusIndicator.textContent = "OFFLINE";
        statusIndicator.style.background = "rgba(255, 80, 80, 0.2)";
        appendConsoleLine("[system] Impossibile contattare Super Agent API.", "system");
    }
}

async function analyzeFile() {
    const path = filePathInput.value.trim();
    const mode = modeSelect.value;
    if (!path) {
        appendConsoleLine("[user] Specifica un percorso file per l'analisi.", "user");
        return;
    }

    appendConsoleLine(`[user] Analizza (${mode}) → ${path}`, "user");
    try {
        const res = await fetch(`${BASE_URL}/analyze`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ path, mode }),
        });
        const data = await res.json();
        appendConsoleLine(`[agent] Exit code: ${data.exit_code}`, "agent");
        appendConsoleLine(data.output || "(nessun output)", "agent");
    } catch (err) {
        appendConsoleLine(`[agent] Errore analisi: ${err}`, "agent");
    }
}

async function runReport() {
    appendConsoleLine("[user] Richiesto report.", "user");
    try {
        const res = await fetch(`${BASE_URL}/report`);
        const data = await res.json();
        appendConsoleLine(`[agent] Exit code report: ${data.exit_code}`, "agent");
        appendConsoleLine(data.output || "(nessun output)", "agent");
    } catch (err) {
        appendConsoleLine(`[agent] Errore report: ${err}`, "agent");
    }
}

async function runLlmAssist(customInstruction = null) {
    const path = filePathInput.value.trim();
    const instruction = (customInstruction ?? llmInstruction.value).trim();
    if (!path) {
        appendConsoleLine("[user] Specifica un percorso file per LLM.", "user");
        return;
    }

    appendConsoleLine(`[user] LLM assist su ${path}`, "user");
    try {
        const res = await fetch(`${BASE_URL}/llm_assist`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ path, instruction }),
        });
        const data = await res.json();
        appendConsoleLine("[agent] Risposta LLM ricevuta.", "agent");
        appendConsoleLine(data.output || "(nessuna risposta)", "agent");
        addChatMessage("assistant", data.output || "(nessuna risposta)");
    } catch (err) {
        appendConsoleLine(`[agent] Errore LLM: ${err}`, "agent");
    }
}

function addChatMessage(role, text) {
    chatMessages.push({ role, text });
    renderChat();
}

function renderChat() {
    chatMessagesEl.innerHTML = "";
    for (const msg of chatMessages) {
        const el = document.createElement("div");
        el.className = `chat-message ${msg.role === "user" ? "user" : "agent"}`;
        el.textContent = msg.text;
        chatMessagesEl.appendChild(el);
    }
    chatMessagesEl.scrollTop = chatMessagesEl.scrollHeight;
}

async function handleChatSend() {
    const text = chatInput.value.trim();
    if (!text) return;

    addChatMessage("user", text);
    chatInput.value = "";

    // Usa il testo chat come instruction LLM, riutilizzando il file selezionato
    await runLlmAssist(text);
}

runAnalyzeBtn.addEventListener("click", analyzeFile);
runReportBtn.addEventListener("click", runReport);
runLlmBtn.addEventListener("click", () => runLlmAssist(null));
chatSendBtn.addEventListener("click", handleChatSend);
chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        handleChatSend();
    }
});

window.addEventListener("load", () => {
    appendConsoleLine("[system] Inizializzazione interfaccia Super Agent...", "system");
    checkStatus();
});
