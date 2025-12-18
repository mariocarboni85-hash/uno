import os
import sys
from datetime import datetime
import threading
from typing import Any, Dict, List, Optional

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import jwt
import logging
import gzip
import shutil
import glob
from logging.handlers import TimedRotatingFileHandler
import uuid
import time
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from agent import uno
from core.brain import (
    assign_task_to_team,
    get_team_status,
    shared_knowledge,
    team,
)
from core.meta_engineer import MetaEngineerOrchestrator
from core.planner import create_plan
from core.team import AgentProfile, TeamCoordinator
from tools import browser, files, shell
from tools.files import extract_zip, perform_file_action
from tools.llm import call_llm
from tools.shell import install_program


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(ROOT_DIR, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

TOOLS = {
    "shell": shell.run,
    "files_write": files.write_file,
    "files_read": files.read_file,
    "list_dir": files.list_dir,
    "browser": browser.fetch,
}

app = FastAPI()

# Logger
logger = logging.getLogger("uno.api")
if not logger.handlers:
    h = logging.StreamHandler()
    fmt = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")
    h.setFormatter(fmt)
    logger.addHandler(h)
logger.setLevel(logging.INFO)

# Audit logger (file)
logs_dir = Path(ROOT_DIR) / 'logs'
logs_dir.mkdir(parents=True, exist_ok=True)
audit_logger = logging.getLogger('uno.audit')
if not audit_logger.handlers:
    class CompressingTimedRotatingFileHandler(TimedRotatingFileHandler):
        """TimedRotatingFileHandler that gzips rotated logs."""
        def doRollover(self):
            try:
                super().doRollover()
            except Exception:
                # If base rollover fails, don't crash the app
                return

            # Compress the most recent rotated file (exclude already .gz files)
            try:
                candidates = [f for f in glob.glob(self.baseFilename + ".*") if not f.endswith('.gz') and f != self.baseFilename]
                if not candidates:
                    return
                latest = max(candidates, key=lambda p: os.path.getmtime(p))
                gz_path = latest + '.gz'
                with open(latest, 'rb') as f_in, gzip.open(gz_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
                try:
                    os.remove(latest)
                except Exception:
                    pass
            except Exception:
                # best-effort compression; swallow errors
                pass

    ah = CompressingTimedRotatingFileHandler(str(logs_dir / 'audit.log'), when='midnight', interval=1, backupCount=30, encoding='utf-8')
    afmt = logging.Formatter('%(asctime)s %(message)s')
    ah.setFormatter(afmt)
    audit_logger.addHandler(ah)
audit_logger.setLevel(logging.INFO)


# Middleware per X-Request-ID
# Simple in-memory rate limiter per IP (requests per minute)
RATE_LIMIT_PER_MIN = int(os.environ.get('RATE_LIMIT_PER_MIN', '60'))
_rate_store: dict = {}


@app.middleware("http")
async def add_request_id_and_rate_limit(request: Request, call_next):
    req_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    request.state.request_id = req_id

    # Rate limiting by client IP (X-Forwarded-For or client.host)
    client_ip = request.client.host if request.client else 'unknown'
    now = int(time.time())
    window = now // 60
    key = f"{client_ip}:{window}"
    count = _rate_store.get(key, 0)
    if count >= RATE_LIMIT_PER_MIN:
        audit_logger.info(f"{req_id} RATE_LIMIT_EXCEEDED ip={client_ip} path={request.url.path}")
        return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})
    _rate_store[key] = count + 1

    response = await call_next(request)
    response.headers["X-Request-ID"] = req_id

    # Audit log: method, path, status, user (if any)
    try:
        user = getattr(request.state, 'user', None)
        user_id = None
        if user:
            user_id = user.get('sub') or user.get('username') or user.get('id')
        audit_logger.info(f"{req_id} {request.method} {request.url.path} status={response.status_code} ip={client_ip} user={user_id}")
    except Exception:
        audit_logger.info(f"{req_id} {request.method} {request.url.path} status={response.status_code} ip={client_ip}")

    return response

# CORS: permetti richieste locali per sviluppo (restringere in produzione)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monta la build frontend (se presente) per servire SPA static
STATIC_DIR = os.path.join(ROOT_DIR, "frontend_build")
if os.path.isdir(STATIC_DIR):
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

vit_orchestrator = MetaEngineerOrchestrator()

# JWT / role-based auth
security = HTTPBearer()

def decode_jwt_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def get_current_user(creds: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    token = creds.credentials
    return decode_jwt_token(token)

def require_role(role: str):
    def _require(user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        roles = user.get("roles") or user.get("role") or []
        if isinstance(roles, str):
            roles = [roles]
        if role not in roles:
            raise HTTPException(status_code=403, detail="Forbidden: insufficient role")
        return user
    return _require


class AgentReviewRequest(BaseModel):
    description: str


class VitCommandRequest(BaseModel):
    directive: str
    goal: str
    priority: str = "standard"
    context: Optional[Dict[str, Any]] = None


class VitCommandResponse(BaseModel):
    command_id: str
    directive: str
    goal: str
    status: str
    priority: str
    artifacts: List[Dict[str, Any]]
    shared_memory: List[Dict[str, Any]]
    started_at: str
    finished_at: Optional[str]


class RunRequest(BaseModel):
    goal: str
    max_steps: int = 5

# Endpoint mock per /api/run
@app.post("/api/run")
async def api_run(request: Request, payload: RunRequest, _user: Dict[str, Any] = Depends(require_role('vit'))):
    """Avvia un run dell'agente in background (non blocca la request).

    In produzione si dovrebbe gestire la coda dei job e persistere lo stato.
    """
    req_id = getattr(request.state, 'request_id', 'unknown')
    user_id = _user.get('sub') or _user.get('username') or _user.get('id')
    logger.info(f"[{req_id}] POST /api/run by {user_id} payload={payload.dict()}")

    def _run_agent(goal: str, max_steps: int):
        try:
            a = uno()
            a.run(goal, max_steps)
            logger.info(f"[{req_id}] background run completed for goal={goal}")
        except Exception as e:
            logger.error(f"[{req_id}] background run error: {e}")

    try:
        threading.Thread(target=_run_agent, args=(payload.goal, payload.max_steps), daemon=True).start()
        logger.info(f"[{req_id}] accepted run request")
        return {"status": "accepted", "goal": payload.goal, "max_steps": payload.max_steps}
    except Exception as e:
        logger.error(f"[{req_id}] failed to start background run: {e}")
        raise HTTPException(status_code=500, detail="Failed to start run")

# Endpoint mock per /api/scan_apps
@app.get("/api/scan_apps")
async def api_scan_apps():
    # Risposta mock: lista di app trovate
    return {"apps": [
        {"name": "App1", "status": "running"},
        {"name": "App2", "status": "stopped"}
    ]}

# Endpoint mock per /api/me
@app.get("/api/me")
async def api_me():
    # Risposta mock: dati utente demo
    return {"username": "demo", "roles": ["user", "admin"]}
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
async def team_knowledge(request: Request, _user: Dict[str, Any] = Depends(require_role('vit'))):
    req_id = getattr(request.state, 'request_id', 'unknown')
    user_id = _user.get('sub') or _user.get('username') or _user.get('id')
    try:
        data = await request.json()
        info = data.get('info')
        agent = data.get('agent')
        logger.info(f"[{req_id}] POST /team/knowledge by {user_id} -> agent={agent} info={info}")
        if not info or not agent:
            return {"error": "Info o agente mancante"}
        # Trova agente e aggiorna memoria
        for a in team:
            if a.name == agent:
                a.add_knowledge(info)
                logger.info(f"[{req_id}] memory updated for agent={agent}")
                return {"result": "Memoria aggiornata"}
        logger.error(f"[{req_id}] agent not found: {agent}")
        return {"error": "Agente non trovato"}
    except Exception as e:
        logger.error(f"[{req_id}] /team/knowledge error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
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
        content="""
        <html>
        <head>
            <title>uno Dashboard</title>
            <link rel='icon' href='/favicon.ico'>
            <style>
                body { font-family: Arial, sans-serif; background: #f7f7f7; margin: 0; padding: 0; }
                .container { max-width: 900px; margin: 40px auto; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px #0001; padding: 32px; }
                h1 { text-align: center; }
                .agent-block { border: 1px solid #e0e0e0; border-radius: 6px; margin-bottom: 24px; padding: 16px; background: #f5f5f5; }
                .agent-title { font-weight: bold; font-size: 1.1em; margin-bottom: 8px; }
                .log, .conflicts, .tasks { margin-bottom: 8px; }
                .conflict { color: #d32f2f; }
                .task { color: #1976d2; }
                #newTaskForm, #newGoalForm { margin: 24px 0; text-align: center; }
                #newTaskInput, #newGoalInput { width: 60%; font-size: 1em; padding: 6px; border-radius: 4px; border: 1px solid #ccc; }
                #assignBtn, #goalBtn { background: #388e3c; color: #fff; border: none; padding: 8px 20px; border-radius: 4px; cursor: pointer; font-size: 1em; margin-left: 8px; }
                #llmSelect { font-size: 1em; padding: 6px 12px; border-radius: 4px; border: 1px solid #ccc; margin-left: 8px; }
                .knowledge-block { background: #e3f2fd; border-radius: 6px; padding: 12px; margin-bottom: 16px; }
                .plan-block { background: #f1f8e9; border-radius: 6px; padding: 12px; margin-bottom: 16px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>uno Dashboard</h1>
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
@app.get("/team/status")
async def team_status():
    return get_team_status()

@app.post("/team/assign")
async def team_assign(request: Request, _user: Dict[str, Any] = Depends(require_role('vit'))):
    req_id = getattr(request.state, 'request_id', 'unknown')
    user_id = _user.get('sub') or _user.get('username') or _user.get('id')
    try:
        data = await request.json()
        task = data.get('task')
        logger.info(f"[{req_id}] POST /team/assign by {user_id} task={task}")
        if not task:
            return {"error": "Task mancante"}
        agent_name = assign_task_to_team(task)
        logger.info(f"[{req_id}] task assigned to {agent_name}")
        return {"assigned_to": agent_name}
    except Exception as e:
        logger.error(f"[{req_id}] /team/assign error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
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

@app.get("/ui/agent-review")
async def agent_review_ui():
    """Serve una pagina HTML locale per revisionare agenti con il team."""
    html = '''
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <title>uno - Revisione Agente</title>
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
        <h1>uno - Revisione Agente Locale</h1>
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


@app.post("/vit/commands", response_model=VitCommandResponse)
async def vit_command(request: Request, payload: VitCommandRequest, _user: Dict[str, Any] = Depends(require_role('vit'))):
    """Permette a vit di lanciare un workflow completo del meta ingegnere."""
    req_id = getattr(request.state, 'request_id', 'unknown')
    user_id = _user.get('sub') or _user.get('username') or _user.get('id')
    logger.info(f"[{req_id}] POST /vit/commands by {user_id} directive={payload.directive} goal={payload.goal}")
    try:
        result = vit_orchestrator.run_command(
            directive=payload.directive,
            goal=payload.goal,
            priority=payload.priority,
            vit_context=payload.context,
        )
        logger.info(f"[{req_id}] vit command executed: {result.get('command_id')}")
        return result
    except Exception as e:
        logger.error(f"[{req_id}] /vit/commands error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/vit/commands", response_model=List[VitCommandResponse])
async def list_vit_commands(limit: int = 5):
    """Restituisce gli ultimi workflow eseguiti per vit."""

    return vit_orchestrator.list_runs(limit)


@app.get("/vit/commands/{command_id}", response_model=VitCommandResponse)
async def vit_command_status(command_id: str):
    """Restituisce i dettagli di un comando vit specifico."""

    result = vit_orchestrator.get_run(command_id)
    if not result:
        raise HTTPException(status_code=404, detail="Comando vit non trovato")
    return result

"""HTTP API per il team di uno, basata su FastAPI.

Endpoint principali:
- POST /team/analyze: il team analizza un problema e salva il report.
- GET  /reports: lista dei report disponibili.
- GET  /reports/{name}: contenuto di un report.
"""

# Legge la chiave segreta JWT da variabile d'ambiente (obbligatoria in produzione)
try:
    JWT_SECRET = os.environ["JWT_SECRET"]
except KeyError:
    raise RuntimeError("Environment variable JWT_SECRET not set. Set JWT_SECRET in the environment before starting the app.")

JWT_ALGORITHM = "HS256"



# Endpoint di login mock per compatibilità test
@app.post("/api/login")
async def api_login(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    # Logica mock: accetta qualsiasi username/password non vuoti
    if not username or not password:
        return JSONResponse(status_code=400, content={"detail": "Username e password richiesti"})
    # Genera un token JWT mock
    token = jwt.encode({"sub": username}, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}
try:
    import ollama
except ImportError:
    ollama = None


def _build_team() -> TeamCoordinator:
    coordinator = TeamCoordinator(TOOLS)
    coordinator.add_profile(AgentProfile(
        name="RequirementsAgent", role="requirements",
        system_prompt="Analista requisiti per problemi software complessi",
    ))
    coordinator.add_profile(AgentProfile(
        name="DesignAgent", role="design",
        system_prompt="Architetto software che produce soluzioni modulari",
    ))
    coordinator.add_profile(AgentProfile(
        name="ProductOwner", role="product_owner",
        system_prompt="PO che crea roadmap sintetiche e priorità",
    ))
    coordinator.add_profile(AgentProfile(
        name="QAAgent", role="qa",
        system_prompt="QA senior che identifica rischi e test",
    ))
    coordinator.build_agents()
    return coordinator


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
