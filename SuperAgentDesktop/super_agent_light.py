"""
Super Agent Light: versione semplificata per PC con risorse limitate
- Esegue solo un task alla volta
- Nessun loop infinito
- Funzioni ridotte al minimo
"""
from orchestrator.job_queue import JobQueue
from agents.software_engineer_agent import SoftwareEngineerAgent
from agents.app_builder_agent import AppBuilderAgent
from supervisor.supervisor import Supervisor

# --- Configurazione ---
job_queue = JobQueue()
supervisor = Supervisor()
software_agent = SoftwareEngineerAgent()
app_agent = AppBuilderAgent()
supervisor.register_agent(software_agent)
supervisor.register_agent(app_agent)

# --- Funzione per aggiungere task ---
def add_task(task):
    job_queue.add_task(task)
    print(f"[TASK] Aggiunto: {task}")

# --- Funzione principale ---
def main():
    print("Super Agent Light avviato.")
    task = job_queue.get_next_task()
    if task:
        print(f"[ESECUZIONE] {task}")
        if task.get('type') == 'generate_software':
            result = software_agent.handle_task(task['payload'])
            print(f"[SoftwareEngineerAgent] {result}")
        elif task.get('type') == 'generate_app':
            result = app_agent.build_app(task['payload'])
            print(f"[AppBuilderAgent] {result}")
        else:
            print(f"[IGNORATO] Tipo task non gestito: {task.get('type')}")
    else:
        print("Nessun task in coda.")

if __name__ == "__main__":
    # Esempio: aggiunta task demo
    add_task({"type": "generate_software", "payload": {"name": "CRM", "backend": "FastAPI"}})
    main()
