from agent_backend import send_notification, get_notifications, add_plugin, load_plugins
# --- API notifiche ---
@app.post("/notifications/send")
def api_send_notification(user_id: int = Form(...), message: str = Form(...)):
    send_notification(user_id, message)
    return {"success": True}

@app.get("/notifications/{user_id}")
def api_get_notifications(user_id: int):
    notes = get_notifications(user_id)
    return {"notifications": notes}

# --- API plugin ---
@app.post("/plugins/add")
def api_add_plugin(name: str = Form(...), description: str = Form(...)):
    ok = add_plugin(name, description)
    return {"success": ok}

@app.get("/plugins")
def api_load_plugins():
    plugins = load_plugins()
    return {"plugins": plugins}
from fastapi import FastAPI, Form
import sqlite3
from agent_backend import Agent, register_user, login_user

app = FastAPI()
DB_PATH = 'superagent_ecosystem.db'

@app.get("/agents")
def get_agents():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, name, status, last_task, last_result, created_at FROM agents')
    agents = [
        {
            "id": row[0],
            "name": row[1],
            "status": row[2],
            "last_task": row[3],
            "last_result": row[4],
            "created_at": row[5]
        }
        for row in c.fetchall()
    ]
    conn.close()
    return {"agents": agents}

@app.post("/agents/{name}/task")
def run_agent_task(name: str, task: str = Form(...)):
    agent = Agent(name)
    result = agent.run_task(task)
    return {"result": result}

# --- API utenti ---
@app.post("/users/register")
def api_register_user(username: str = Form(...), password: str = Form(...), role: str = Form('user')):
    ok = register_user(username, password, role)
    return {"success": ok}

@app.post("/users/login")
def api_login_user(username: str = Form(...), password: str = Form(...)):
    user = login_user(username, password)
    if user:
        return {"success": True, "user": user}
    return {"success": False}

# Per avviare: uvicorn agent_api:app --reload
