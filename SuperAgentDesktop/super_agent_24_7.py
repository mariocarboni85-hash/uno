"""
Super Agent 24/7: produzione autonoma continua di software e app
- Loop infinito di esecuzione task
- Monitoraggio automatico agenti
- Sandbox per sicurezza
- Generazione build desktop e mobile
- Logs e supervisione attiva
"""
import time
from orchestrator.job_queue import JobQueue
from agents.software_engineer_agent import SoftwareEngineerAgent
from agents.app_builder_agent import AppBuilderAgent
from supervisor.supervisor import Supervisor
from sandbox.secure_sandbox import run_code_in_sandbox

# --- Configurazione ---
job_queue = JobQueue()
supervisor = Supervisor()
software_agent = SoftwareEngineerAgent()
app_agent = AppBuilderAgent()
supervisor.register_agent(software_agent)
supervisor.register_agent(app_agent)

# --- Funzione per aggiungere task live ---
def add_task(task):
    job_queue.add_task(task)
    print(f"[TASK] Aggiunto: {task}")

# --- Loop di produzione continua ---
def main_loop():
    print("Super Agent 24/7 avviato. CTRL+C per uscire.")
    while True:
        task = job_queue.get_next_task()
        if task:
            print(f"[ESECUZIONE] {task}")
            if task.get('type') == 'generate_software':
                result = software_agent.handle_task(task['payload'])
                print(f"[SoftwareEngineerAgent] {result}")
            elif task.get('type') == 'generate_app':
                result = app_agent.build_app(task['payload'])
                print(f"[AppBuilderAgent] {result}")
            elif task.get('type') == 'run_code':
                code = task['payload'].get('code', '')
                output, error = run_code_in_sandbox(code)
                print(f"[SANDBOX OUTPUT] {output}\n[ERROR] {error}")
            else:
                print(f"[IGNORATO] Tipo task non gestito: {task.get('type')}")
        else:
            time.sleep(2)

if __name__ == "__main__":
    # Esempio: aggiunta task demo
    add_task({"type": "generate_software", "payload": {"name": "CRM", "backend": "FastAPI"}})
    add_task({"type": "generate_app", "payload": {"name": "CRM App", "platforms": ["android", "ios"]}})
    add_task({"type": "run_code", "payload": {"code": "print('Hello from sandbox!')"}})
    main_loop()
