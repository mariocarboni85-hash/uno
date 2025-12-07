@app.get("/team/graph")
async def team_graph():
    # Restituisce dati per network graph agenti-task
    nodes = []
    edges = []
    for agent in team:
        nodes.append({'id': agent.name, 'type': 'agent'})
        for t in agent.tasks:
            tid = f"{agent.name}_{t['task']}"
            nodes.append({'id': tid, 'type': 'task', 'priority': t['priority']})
            edges.append({'from': agent.name, 'to': tid})
    return {'nodes': nodes, 'edges': edges}
from core.planner import create_plan
from tools.llm import call_llm
from core.brain import shared_knowledge
@app.post("/team/goal")
async def team_goal(request: Request):
    data = await request.json()
    goal = data.get('goal')
    llm = data.get('llm', 'default')
    if not goal:
        return {"error": "Obiettivo mancante"}
    plan = create_plan(goal)
    response = call_llm(llm, f"Pianifica: {goal}")
    return {"plan": plan, "llm_response": response}
@app.post("/team/knowledge")
async def team_knowledge(request: Request):
    data = await request.json()
    info = data.get('info')
    agent = data.get('agent')
    if not info or not agent:
        return {"error": "Info o agente mancante"}
    # Trova agente e aggiorna memoria
    for a in team:
        if a.name == agent:
            a.add_knowledge(info)
            return {"result": "Memoria aggiornata"}
    return {"error": "Agente non trovato"}
@app.get("/team/knowledge")
async def get_knowledge():
    return shared_knowledge[-20:]
@app.get("/team/plans")
async def get_plans(goal: str = None):
    if not goal:
        return {"error": "Obiettivo mancante"}
    return create_plan(goal)
@app.get("/ui/dashboard")
async def agent_dashboard_ui():
    return HTMLResponse(
        content=f"""
        <html>
        <head>
            <title>Super Agent Dashboard</title>
            <link rel='icon' href='/favicon.ico'>
            <style>
                body {{ font-family: Arial, sans-serif; background: #f7f7f7; margin: 0; padding: 0; }}
                .container {{ max-width: 900px; margin: 40px auto; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px #0001; padding: 32px; }}
                h1 {{ text-align: center; }}
                .agent-block {{ border: 1px solid #e0e0e0; border-radius: 6px; margin-bottom: 24px; padding: 16px; background: #f5f5f5; }}
                .agent-title {{ font-weight: bold; font-size: 1.1em; margin-bottom: 8px; }}
                .log, .conflicts, .tasks {{ margin-bottom: 8px; }}
                .conflict {{ color: #d32f2f; }}
                .task {{ color: #1976d2; }}
                #newTaskForm, #newGoalForm {{ margin: 24px 0; text-align: center; }}
                #newTaskInput, #newGoalInput {{ width: 60%; font-size: 1em; padding: 6px; border-radius: 4px; border: 1px solid #ccc; }}
                #assignBtn, #goalBtn {{ background: #388e3c; color: #fff; border: none; padding: 8px 20px; border-radius: 4px; cursor: pointer; font-size: 1em; margin-left: 8px; }}
                #llmSelect {{ font-size: 1em; padding: 6px 12px; border-radius: 4px; border: 1px solid #ccc; margin-left: 8px; }}
                .knowledge-block {{ background: #e3f2fd; border-radius: 6px; padding: 12px; margin-bottom: 16px; }}
                .plan-block {{ background: #f1f8e9; border-radius: 6px; padding: 12px; margin-bottom: 16px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Super Agent Dashboard</h1>
                <form id="newTaskForm">
                    <input id="newTaskInput" type="text" placeholder="Nuovo task da assegnare...">
                    <button id="assignBtn" type="submit">Assegna task</button>
                </form>
                <form id="newGoalForm">
                    <input id="newGoalInput" type="text" placeholder="Nuovo obiettivo multi-step...">
                    <select id="llmSelect">
                        <option value="default">default</option>
                        <option value="mock">mock</option>
                        <option value="ollama">ollama</option>
                    </select>
                    <button id="goalBtn" type="submit">Crea piano</button>
                </form>
                <div id="plan"></div>
                <div id="agents"></div>
                <div class="knowledge-block">
                    <b>Memoria condivisa agenti:</b>
                    <div id="knowledge"></div>
                </div>
            </div>
            <script>
                async function fetchStatus() {
                    const resp = await fetch('/team/status');
                    const data = await resp.json();
                    renderAgents(data);
                }
                async function fetchKnowledge() {
                    const resp = await fetch('/team/knowledge');
                    const data = await resp.json();
                    renderKnowledge(data);
                }
                function renderAgents(data) {
                    const agentsDiv = document.getElementById('agents');
                    agentsDiv.innerHTML = data.map(agent => `
                        <div class="agent-block">
                            <div class="agent-title">${agent.name}</div>
                            <div class="tasks"><b>Task:</b> ${agent.tasks.map(t => `<span class='task'>${t.task} <span style='color:#888'>(P${t.priority})</span></span>`).join(', ') || 'Nessuno'}</div>
                            <div class="log"><b>Log:</b><br>${agent.log.map(l => `<div>${l}</div>`).join('')}</div>
                            <div class="conflicts"><b>Conflitti:</b> ${agent.conflicts.map(c => `<span class='conflict'>${c}</span>`).join(', ') || 'Nessuno'}</div>
                            <div class="skills"><b>Skill:</b> ${agent.skills.join(', ')}</div>
                            <form class="knowledgeForm" data-agent="${agent.name}">
                                <input type="text" class="knowledgeInput" placeholder="Aggiungi info a memoria condivisa...">
                                <button type="submit">Salva</button>
                            </form>
                        </div>
                    `).join('');
                    document.querySelectorAll('.knowledgeForm').forEach(form => {
                        form.addEventListener('submit', async (e) => {
                            e.preventDefault();
                            const agent = form.getAttribute('data-agent');
                            const info = form.querySelector('.knowledgeInput').value;
                            if (!info || info.trim().length === 0) return;
                            await fetch('/team/knowledge', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ agent, info })
                            });
                            form.querySelector('.knowledgeInput').value = '';
                            setTimeout(fetchKnowledge, 500);
                        });
                    });
                }
                function renderKnowledge(data) {
                    const kDiv = document.getElementById('knowledge');
                    kDiv.innerHTML = data.map(k => `<div><b>${k.from}:</b> ${k.info}</div>`).join('');
                }
                document.getElementById('newTaskForm').addEventListener('submit', async (e) => {
                    e.preventDefault();
                    const val = document.getElementById('newTaskInput').value;
                    if (!val || val.trim().length === 0) return;
                    await fetch('/team/assign', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ task: val })
                    });
                    document.getElementById('newTaskInput').value = '';
                    setTimeout(fetchStatus, 500);
                });
                document.getElementById('newGoalForm').addEventListener('submit', async (e) => {
                    e.preventDefault();
                    const val = document.getElementById('newGoalInput').value;
                    const llm = document.getElementById('llmSelect').value;
                    if (!val || val.trim().length === 0) return;
                    const resp = await fetch('/team/goal', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ goal: val, llm })
                    });
                    const data = await resp.json();
                    renderPlan(data);
                });
                function renderPlan(data) {
                    const planDiv = document.getElementById('plan');
                    if (data.error) {
                        planDiv.innerHTML = `<div class='plan-block'><b>Errore:</b> ${data.error}</div>`;
                        return;
                    }
                    planDiv.innerHTML = `
                        <div class='plan-block'>
                            <b>Obiettivo:</b> ${data.plan.goal}<br>
                            <b>Step:</b><br>
                            ${data.plan.steps.map((s, i) => `<div>${i+1}. ${s} <span style='color:#aaa'>(${data.plan.status[i]})</span></div>`).join('')}
                            <b>LLM/API:</b> ${data.llm_response}
                        </div>
                    `;
                }
                setInterval(fetchStatus, 2000);
                setInterval(fetchKnowledge, 4000);
                fetchStatus();
                fetchKnowledge();
            </script>
        </body>
        </html>
        """,
        status_code=200,
    )
from fastapi import Request
from core.brain import get_team_status, assign_task_to_team
@app.get("/ui/dashboard")
async def agent_dashboard_ui():
    return HTMLResponse(
        content=f"""
        <html>
        <head>
            <title>Super Agent Dashboard</title>
            <link rel='icon' href='/favicon.ico'>
            <style>
                body {{ font-family: Arial, sans-serif; background: #f7f7f7; margin: 0; padding: 0; }}
                .container {{ max-width: 900px; margin: 40px auto; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px #0001; padding: 32px; }}
                h1 {{ text-align: center; }}
                .agent-block {{ border: 1px solid #e0e0e0; border-radius: 6px; margin-bottom: 24px; padding: 16px; background: #f5f5f5; }}
                .agent-title {{ font-weight: bold; font-size: 1.1em; margin-bottom: 8px; }}
                .log, .conflicts, .tasks {{ margin-bottom: 8px; }}
                .conflict {{ color: #d32f2f; }}
                .task {{ color: #1976d2; }}
                #newTaskForm {{ margin: 24px 0; text-align: center; }}
                #newTaskInput {{ width: 60%; font-size: 1em; padding: 6px; border-radius: 4px; border: 1px solid #ccc; }}
                #assignBtn {{ background: #388e3c; color: #fff; border: none; padding: 8px 20px; border-radius: 4px; cursor: pointer; font-size: 1em; margin-left: 8px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Super Agent Dashboard</h1>
                <form id="newTaskForm">
                    <input id="newTaskInput" type="text" placeholder="Nuovo task da assegnare...">
                    <button id="assignBtn" type="submit">Assegna task</button>
                </form>
                <div id="agents"></div>
            </div>
            <script>
                async function fetchStatus() {
                    const resp = await fetch('/team/status');
                    const data = await resp.json();
                    renderAgents(data);
                }
                function renderAgents(data) {
                    const agentsDiv = document.getElementById('agents');
                    agentsDiv.innerHTML = data.map(agent => `
                        <div class="agent-block">
                            <div class="agent-title">${agent.name}</div>
                            <div class="tasks"><b>Task:</b> ${agent.tasks.map(t => `<span class='task'>${t}</span>`).join(', ') || 'Nessuno'}</div>
                            <div class="log"><b>Log:</b><br>${agent.log.map(l => `<div>${l}</div>`).join('')}</div>
                            <div class="conflicts"><b>Conflitti:</b> ${agent.conflicts.map(c => `<span class='conflict'>${c}</span>`).join(', ') || 'Nessuno'}</div>
                        </div>
                    `).join('');
                }
                document.getElementById('newTaskForm').addEventListener('submit', async (e) => {
                    e.preventDefault();
                    const val = document.getElementById('newTaskInput').value;
                    if (!val || val.trim().length === 0) return;
                    await fetch('/team/assign', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ task: val })
                    });
                    document.getElementById('newTaskInput').value = '';
                    setTimeout(fetchStatus, 500);
                });
                setInterval(fetchStatus, 2000);
                fetchStatus();
            </script>
        </body>
        </html>
        """,
        status_code=200,
    )
# Endpoint API per dashboard
@app.get("/team/status")
async def team_status():
    return get_team_status()

@app.post("/team/assign")
async def team_assign(request: Request):
    data = await request.json()
    task = data.get('task')
    if not task:
        return {"error": "Task mancante"}
    agent_name = assign_task_to_team(task)
    return {"assigned_to": agent_name}
def llm_review_agent(prompt: str) -> str:
    """Usa Ollama per generare una revisione, oppure restituisce una risposta mock se non disponibile."""
    if ollama:
        try:
            response = ollama.chat(model='llama2', messages=[
                {'role': 'user', 'content': prompt}
            ])
            return response['message']['content']
        except Exception as e:
            return f"[LLM ERROR] {e}\nPrompt:\n{prompt}"
    else:
        return f"[MOCK] Revisione fittizia. Prompt:\n{prompt}"

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/ui/agent-review")
async def agent_review_ui():
    """Serve una pagina HTML locale per revisionare agenti con il team."""
    html = '''
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <title>SuperAgent - Revisione Agente</title>
        <link rel="icon" type="image/png" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFUlEQVQYV2NkYGD4z0AEYBxVSFQAAAwAAf4A3XwAAAAASUVORK5CYII=" />
        <style>
            body { font-family: Arial, sans-serif; margin: 2em; background: #f7f7f7; }
            textarea { width: 100%; height: 180px; font-size: 1em; }
            button { padding: 0.5em 1.5em; font-size: 1em; margin-top: 1em; }
            .result { background: #fff; border-radius: 8px; padding: 1em; margin-top: 2em; box-shadow: 0 2px 8px #ccc; }
            h2 { margin-top: 1.5em; }
        </style>
    </head>
    <body>
        <h1>SuperAgent - Revisione Agente Locale</h1>
        <p>Incolla la descrizione dell'agente (scopo, prompt, tools, problemi):</p>
        <textarea id="desc" placeholder="Incolla qui la descrizione..."></textarea><br>
        <button onclick="reviewAgent()">Fai lavorare il team</button>
        <div id="result" class="result"></div>
        <script>
        async function reviewAgent() {
            const description = document.getElementById('desc').value;
            document.getElementById('result').innerHTML = '<em>Team al lavoro... <span style="font-size:2em;">⏳</span></em>';
            try {
                const resp = await fetch('/agent/review', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ description })
                });
                if (!resp.ok) {
                    throw new Error('Errore ' + resp.status + ': ' + (await resp.text()));
                }
                const data = await resp.json();
                let html = '';
                html += `<h2>Problemi individuati</h2><pre>${data.issues || '(nessuno)'}</pre>`;
                html += `<h2>Miglioramenti proposti</h2><pre>${data.improvements || '(nessuno)'}</pre>`;
                html += `<h2>Rischi e failure mode</h2><pre>${data.risks || '(nessuno)'}</pre>`;
                html += `<h2>QA Checklist</h2><pre>${data.qa_feedback || '(nessuna)'}</pre>`;
                html += `<h2>File review</h2><pre>${data.review_file || '(non salvato)'}</pre>`;
                document.getElementById('result').innerHTML = html;
            } catch (err) {
                document.getElementById('result').innerHTML = `<span style='color:red;'>Errore: ${err}</span>`;
            }
        }
        </script>
    </body>
    </html>
    '''
    return HTMLResponse(content=html)

"""HTTP API per il team di SuperAgent, basata su FastAPI.

Endpoint principali:
- POST /team/analyze: il team analizza un problema e salva il report.
- GET  /reports: lista dei report disponibili.
- GET  /reports/{name}: contenuto di un report.
"""

import os
from datetime import datetime
from typing import List, Dict

from fastapi import FastAPI, HTTPException
try:
    import ollama
except ImportError:
    ollama = None
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse

from agent import SuperAgent
from tools import shell, files, browser
from core.team import TeamCoordinator, AgentProfile

try:
    return HTMLResponse(
        content=f"""
        <html>
        <head>
            <title>Agent Review Team</title>
            <link rel='icon' href='/favicon.ico'>
            <style>
                body {{ font-family: Arial, sans-serif; background: #f7f7f7; margin: 0; padding: 0; transition: background 0.2s, color 0.2s; }}
                .container {{ max-width: 600px; margin: 40px auto; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px #0001; padding: 32px; }}
                h1 {{ text-align: center; }}
                textarea {{ width: 100%; min-height: 80px; margin-bottom: 12px; font-size: 1em; }}
                button {{ background: #0078d4; color: #fff; border: none; padding: 10px 24px; border-radius: 4px; cursor: pointer; font-size: 1em; }}
                button:disabled {{ background: #aaa; }}
                .spinner {{ display: none; text-align: center; margin: 16px 0; }}
                .error {{ color: #d32f2f; margin-bottom: 12px; text-align: center; }}
                .result {{ background: #e3f2fd; border-radius: 4px; padding: 12px; margin-top: 16px; white-space: pre-wrap; }}
                #downloadBtn {{ display: none; margin-top: 12px; background: #388e3c; }}
                #themeToggle {{ position: absolute; top: 16px; right: 32px; background: #222; color: #fff; border: none; padding: 8px 16px; border-radius: 20px; cursor: pointer; font-size: 0.95em; }}
                #llmSelect {{ margin-bottom: 16px; font-size: 1em; padding: 6px 12px; border-radius: 4px; border: 1px solid #ccc; }}
                .history {{ margin-top: 32px; background: #f1f8e9; border-radius: 6px; padding: 16px; }}
                .history h2 {{ margin-top: 0; font-size: 1.1em; }}
                .history-item {{ margin-bottom: 12px; border-bottom: 1px solid #e0e0e0; padding-bottom: 8px; }}
                body.dark {{ background: #181818; color: #eee; }}
                body.dark .container {{ background: #232323; box-shadow: 0 2px 8px #0006; }}
                body.dark .result {{ background: #263238; color: #cfd8dc; }}
                body.dark button {{ background: #333; color: #fff; }}
                body.dark #downloadBtn {{ background: #388e3c; color: #fff; }}
                body.dark #themeToggle {{ background: #eee; color: #222; }}
                body.dark .history {{ background: #263238; color: #cfd8dc; }}
            </style>
        </head>
        <body>
            <button id="themeToggle">Tema scuro</button>
            <div class="container">
                <h1>Team di Revisione Agenti</h1>
                <label for="llmSelect">Modello LLM:</label>
                <select id="llmSelect">
                    <option value="default">default</option>
                    <option value="mock">mock</option>
                    <option value="ollama">ollama</option>
                </select>
                <form id="reviewForm">
                    <div class="error" id="errorMsg"></div>
                    <textarea id="agentText" name="agentText" placeholder="Descrivi l'agente da revisionare..."></textarea>
                    <button type="submit" id="submitBtn">Invia</button>
                </form>
                <div class="spinner" id="spinner">Team al lavoro…</div>
                <div class="result" id="result"></div>
                <button id="downloadBtn">Scarica report</button>
                <div class="history" id="history">
                    <h2>Storico revisioni</h2>
                    <div id="historyList"></div>
                </div>
            </div>
            <script>
                const form = document.getElementById('reviewForm');
                const spinner = document.getElementById('spinner');
                const result = document.getElementById('result');
                const errorMsg = document.getElementById('errorMsg');
                const submitBtn = document.getElementById('submitBtn');
                const downloadBtn = document.getElementById('downloadBtn');
                const themeToggle = document.getElementById('themeToggle');
                const llmSelect = document.getElementById('llmSelect');
                const historyList = document.getElementById('historyList');
                let lastReport = '';
                let history = [];
                form.addEventListener('submit', async (e) => {
                    e.preventDefault();
                    errorMsg.textContent = '';
                    result.textContent = '';
                    downloadBtn.style.display = 'none';
                    const agentText = document.getElementById('agentText').value;
                    const llmModel = llmSelect.value;
                    // Validazione input: non inviare se vuoto o solo spazi
                    if (!agentText || agentText.trim().length === 0) {
                        errorMsg.textContent = 'Inserisci una descrizione valida dell\'agente.';
                        return;
                    }
                    spinner.style.display = 'block';
                    submitBtn.disabled = true;
                    try {
                        const resp = await fetch('/agent/review', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ agent: agentText, llm: llmModel })
                        });
                        const data = await resp.json();
                        if (resp.ok) {
                            const report = data.result || JSON.stringify(data);
                            result.textContent = report;
                            lastReport = report;
                            downloadBtn.style.display = 'inline-block';
                            // Aggiorna storico
                            history.unshift({ agent: agentText, llm: llmModel, result: report, ts: new Date().toLocaleString() });
                            if (history.length > 10) history.pop();
                            renderHistory();
                        } else {
                            errorMsg.textContent = data.detail || 'Errore nella revisione.';
                        }
                    } catch (err) {
                        errorMsg.textContent = 'Errore di rete o server.';
                    } finally {
                        spinner.style.display = 'none';
                        submitBtn.disabled = false;
                    }
                });
                downloadBtn.addEventListener('click', function() {
                    if (!lastReport) return;
                    const blob = new Blob([lastReport], { type: 'text/plain' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'report_revisione.txt';
                    document.body.appendChild(a);
                    a.click();
                    setTimeout(() => {
                        document.body.removeChild(a);
                        URL.revokeObjectURL(url);
                    }, 100);
                });
                themeToggle.addEventListener('click', function() {
                    const body = document.body;
                    const dark = body.classList.toggle('dark');
                    themeToggle.textContent = dark ? 'Tema chiaro' : 'Tema scuro';
                });
                function renderHistory() {
                    historyList.innerHTML = history.map(item => `
                        <div class="history-item">
                            <b>${item.ts}</b> | <span style="color:#0078d4">${item.llm}</span><br>
                            <i>${item.agent}</i><br>
                            <div style="margin-top:4px;">${item.result.replace(/\n/g, '<br>')}</div>
                        </div>
                    `).join('');
                }
            </script>
        </body>
        </html>
        """,
        status_code=200,
    )


def _save_report(user_issue: str, demo_output: str) -> str:
    """Salva il report in REPORTS_DIR e restituisce il path assoluto."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{timestamp}.txt"
    report_path = os.path.join(REPORTS_DIR, filename)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("Problema dell'utente:\n" + user_issue + "\n\n")
        f.write(demo_output)

    return report_path


@app.post("/team/analyze")
async def team_analyze(issue: str):
    """Fa analizzare un problema al team e salva il report.

    Body semplice: una stringa `issue`.
    Ritorna JSON con testo del report e info sul file salvato.
    """
    if not issue.strip():
        raise HTTPException(status_code=400, detail="'issue' non può essere vuoto")

    coordinator = _build_team()
    demo_output = coordinator.run_team_demo(issue)
    report_path = _save_report(issue, demo_output)

    return {
        "issue": issue,
        "report": demo_output,
        "report_file": os.path.basename(report_path),
    }


@app.post("/team/analyze_structured")
async def team_analyze_structured(issue: str) -> Dict[str, str]:
    """Versione strutturata dell'analisi del team.

    Ritorna un dict JSON con chiavi:
    - issue
    - requirements
    - design
    - roadmap
    - qa_feedback
    - full_report
    - report_file (nome del file salvato)
    """
    if not issue.strip():
        raise HTTPException(status_code=400, detail="'issue' non può essere vuoto")

    coordinator = _build_team()
    artifacts = coordinator.run_team_structured(issue)

    full_report = artifacts.get("full_report", "")
    report_path = _save_report(issue, full_report)

    return {
        "issue": issue,
        "requirements": artifacts.get("requirements", ""),
        "design": artifacts.get("design", ""),
        "roadmap": artifacts.get("roadmap", ""),
        "qa_feedback": artifacts.get("qa_feedback", ""),
        "full_report": full_report,
        "report_file": os.path.basename(report_path),
    }

class AgentReviewRequest(BaseModel):
    description: str

@app.post("/agent/review")
async def agent_review(request: AgentReviewRequest) -> Dict[str, str]:
    """Endpoint che fa revisionare al team un agente esistente.
    Body: JSON con campo 'description'.
    Ritorna JSON con sezioni della revisione e path del file salvato.
    """
    description = request.description
    if not description.strip():
        raise HTTPException(status_code=400, detail="'description' non può essere vuoto")

    coordinator = TeamCoordinator(TOOLS)
    coordinator.add_profile(AgentProfile(
        name="RequirementsAgent", role="requirements",
        system_prompt="Analista requisiti per agenti AI esistenti",
    ))
    coordinator.add_profile(AgentProfile(
        name="DesignAgent", role="design",
        system_prompt="Architetto di agenti AI che progetta miglioramenti strutturali",
    ))
    coordinator.add_profile(AgentProfile(
        name="QAReviewerAgent", role="qa",
        system_prompt=(
            "QA Reviewer che valuta la qualità e l'affidabilità di agenti AI "
            "e propone checklist di miglioramento pratiche",
        ), # type: ignore
    ))
    coordinator.build_agents()

    # Usa LLM locale (Ollama) o mock per la revisione
    review_text = llm_review_agent(description)
    review = {
        "issues": "Problemi individuati: ...",
        "improvements": "Miglioramenti proposti: ...",
        "risks": "Rischi: ...",
        "qa_feedback": "QA: ...",
    }
    # Puoi parsare review_text per riempire queste sezioni, oppure mostrare tutto in una.

    # Salva anche lato API, in una cartella dedicata
    reviews_dir = os.path.join(ROOT_DIR, "agent_reviews")
    os.makedirs(reviews_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"review_{timestamp}.md"
    review_path = os.path.join(reviews_dir, filename)

    try:
        with open(review_path, "w", encoding="utf-8") as f:
            f.write("# Revisione agente (API)\n\n")
            f.write("## Descrizione iniziale\n\n")
            f.write(description + "\n\n")
            f.write("## Problemi individuati\n\n")
            f.write(review.get("issues", "(nessuno)") + "\n\n")
            f.write("## Miglioramenti proposti\n\n")
            f.write(review.get("improvements", "(nessuno)") + "\n\n")
            f.write("## Rischi e failure mode\n\n")
            f.write(review.get("risks", "(nessuno)") + "\n\n")
            f.write("## QA Checklist\n\n")
            f.write(review.get("qa_feedback", "(nessuna)") + "\n")
    except Exception:
        # Non blocchiamo la risposta HTTP se il salvataggio fallisce
        review_path = ""

    return {
        "description": description,
        "issues": review.get("issues", ""),
        "improvements": review.get("improvements", ""),
        "risks": review.get("risks", ""),
        "qa_feedback": review.get("qa_feedback", ""),
        "review_file": os.path.basename(review_path) if review_path else "",
    }
    html = '''
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <title>SuperAgent - Revisione Agente</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 2em; background: #f7f7f7; }
            textarea { width: 100%; height: 180px; font-size: 1em; }
            button { padding: 0.5em 1.5em; font-size: 1em; margin-top: 1em; }
            .result { background: #fff; border-radius: 8px; padding: 1em; margin-top: 2em; box-shadow: 0 2px 8px #ccc; }
            h2 { margin-top: 1.5em; }
        </style>
    </head>
    <body>
        <h1>SuperAgent - Revisione Agente Locale</h1>
        <p>Incolla la descrizione dell'agente (scopo, prompt, tools, problemi):</p>
        <textarea id="desc" placeholder="Incolla qui la descrizione..."></textarea><br>
        <button onclick="reviewAgent()">Fai lavorare il team</button>
        <div id="result" class="result"></div>
        <script>
        async function reviewAgent() {
            const description = document.getElementById('desc').value;
            document.getElementById('result').innerHTML = '<em>Team al lavoro...</em>';
            const resp = await fetch('/agent/review', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ description })
            });
            const data = await resp.json();
            let html = '';
            html += `<h2>Problemi individuati</h2><pre>${data.issues || '(nessuno)'}</pre>`;
            html += `<h2>Miglioramenti proposti</h2><pre>${data.improvements || '(nessuno)'}</pre>`;
            html += `<h2>Rischi e failure mode</h2><pre>${data.risks || '(nessuno)'}</pre>`;
            html += `<h2>QA Checklist</h2><pre>${data.qa_feedback || '(nessuna)'}</pre>`;
            html += `<h2>File review</h2><pre>${data.review_file || '(non salvato)'}</pre>`;
            document.getElementById('result').innerHTML = html;
        }
        </script>
    </body>
    </html>
    '''
    return HTMLResponse(content=html)


@app.get("/reports", response_model=List[str])
async def list_reports():
    """Ritorna l'elenco dei file di report disponibili (nomi file)."""
    try:
        files_list = sorted(
            [f for f in os.listdir(REPORTS_DIR) if f.startswith("report_")],
            reverse=True,
        )
        return files_list
    except FileNotFoundError:
        return []


@app.get("/reports/{name}", response_class=PlainTextResponse)
async def get_report(name: str):
    """Ritorna il contenuto di un singolo report come testo plain."""
    report_path = os.path.join(REPORTS_DIR, name)
    if not os.path.isfile(report_path):
        raise HTTPException(status_code=404, detail="Report non trovato")

    with open(report_path, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/")
async def root():
    return {"status": "ok", "message": "SuperAgent Team API"}
