"""
File: super_agent_valutazione.py
Descrizione: Esempio completo di utilizzo di Super Agent Workspace per valutazione da parte di ChatGPT. Include pipeline di sviluppo software, orchestrazione agenti e interfaccia chat.
"""

from super_agent_workspace.core.workspace_app import SuperAgentWorkspace
from super_agent_workspace.core.supervisor import Supervisor
from super_agent_workspace.core.memory_manager import MemoryManager
from super_agent_workspace.core.autopilot import AutoPilot
from super_agent_workspace.core.job_queue import JobQueue
from SuperAgentDesktop.agents.software_engineer_agent import SoftwareEngineerAgent
from PyQt5.QtWidgets import QApplication
import sys
import requests
from concurrent.futures import ThreadPoolExecutor

# Notifiche
import json
import os
try:
    import openai
except ModuleNotFoundError:
    import subprocess
    subprocess.run(["pip", "install", "openai"])
    import openai
from utils.notifications import notify_desktop, notify_email, notify_webhook


def main():
    try:
        print("DEBUG: Creo QApplication")
        app = QApplication(sys.argv)
        print("DEBUG: Creo MemoryManager")
        memory = MemoryManager()
        print("DEBUG: Creo JobQueue")
        job_queue = JobQueue()
        print("DEBUG: Creo Supervisor")
        supervisor = Supervisor()
        print("DEBUG: Creo AutoPilot")
        autopilot = AutoPilot(job_queue, memory)
        print("DEBUG: Creo SoftwareEngineerAgent")
        software_engineer = SoftwareEngineerAgent()

        # Registrazione agenti (esempio: nome e comando)
        print("DEBUG: Registro agenti nel supervisor")
        supervisor.register_agent('software_engineer', ['python', 'software_engineer_agent.py'])
        supervisor.start()

        print("DEBUG: Creo SuperAgentWorkspace")
        window = SuperAgentWorkspace()
        print("DEBUG: Finestra creata, la mostro")
        window.show()
        print("Super Agent Workspace avviato. Usa la chat per testare pipeline e task di sviluppo software.")
    except Exception as e:
        import traceback
        print("Errore durante l'avvio della GUI:", e)
        traceback.print_exc()

    # Lettura preferenze notifiche
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'notifications.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            notif_config = json.load(f)
    except Exception as e:
        print(f"Errore lettura config notifiche: {e}")
        notif_config = {}

    # Esempio: invio notifica su evento di successo/errore
    def send_notification(event, message):
        if notif_config.get('events', {}).get(event, False):
            if notif_config.get('desktop', False):
                notify_desktop("Super Agent", message)
            if notif_config.get('email', False):
                email_addr = notif_config.get('email_address', '')
                if email_addr:
                    notify_email("Super Agent - Notifica", message, email_addr)
            if notif_config.get('webhook', False):
                webhook_url = notif_config.get('webhook_url', '')
                if webhook_url:
                    notify_webhook(webhook_url, message)

    # Esempio di utilizzo: task completato
    send_notification('task_success', 'Pipeline completata con successo!')

    # Invio notifica remota al completamento task
    remote_url = notif_config.get('remote_url', 'https://superagent-dashboard.example.com')
    api_key = notif_config.get('api_key', 'API_KEY_SUPER_AGENT')
    task = {'name': 'Pipeline', 'status': 'success'}
    # notify_remote(task, remote_url, api_key)  # disabilitato per evitare errore

    # Invio task a dispositivi remoti
    # send_task_remote(task)  # disabilitato per evitare errore

    # Esempio: esecuzione parallela di una lista di task
    # task_list = [ ... ]  # Definisci la lista dei task da processare
    # for task in task_list:
    #     executor.submit(run_task, task)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

# --- CORREZIONE FUNZIONE SEND_TASK_REMOTE ---
REMOTE_DEVICES = [
    {"url": "http://192.168.1.20:5500", "api_key": "MASTER_SLAVE_KEY"}
]

def send_task_remote(task):
    for device in REMOTE_DEVICES:
        headers = {"Authorization": f"Bearer {device['api_key']}"}
        try:
            resp = requests.post(f"{device['url']}/task/add", json=task, headers=headers, timeout=10)
            if resp.status_code == 200:
                print(f"Task inviato a {device['url']} con successo.")
            else:
                print(f"Errore invio task a {device['url']}: {resp.status_code} - {resp.text}")
        except Exception as e:
            print(f"Errore invio task a {device['url']}: {e}")

# --- CORREZIONE NOTIFY_REMOTE ---
def notify_remote(task, remote_url, api_key):
    payload = {
        "title": f"Task {task['name']}",
        "message": f"Stato: {task['status']}",
        "email": "utente@example.com",
        "webhook_url": "https://api.telegram.org/botTOKEN/sendMessage?chat_id=CHAT_ID"
    }
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        resp = requests.post(f"{remote_url}/notification/send", json=payload, headers=headers)
        if resp.status_code == 200:
            print("Notifica remota inviata correttamente.")
        else:
            print(f"Errore invio notifica remota: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"Errore connessione remota: {e}")

# --- CORREZIONE USO NOTIFY_REMOTE E SEND_TASK_REMOTE ---
# Esempio di utilizzo: task completato
# task = {'name': 'Pipeline', 'status': 'success'}
# remote_url = 'http://192.168.1.20:5500'
# api_key = 'MASTER_SLAVE_KEY'
# notify_remote(task, remote_url, api_key)
# send_task_remote(task)

# --- CORREZIONE ESECUZIONE PARALLELA TASK ---
executor = ThreadPoolExecutor(max_workers=5)

def run_task(task):
    schedule_task(task)

def schedule_task(task):
    print(f"Task schedulato: {task}")
    # Qui va la logica reale di scheduling

# task_list = [ ... ]
# for task in task_list:
#     executor.submit(run_task, task)
