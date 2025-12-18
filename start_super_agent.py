from dashboard import app
from agent_manager import AgentManager
from scheduler import Scheduler

if __name__ == "__main__":
    print("Avvio Super Agent in produzione con Waitress...")
    manager = AgentManager()
    scheduler = Scheduler(manager)
    scheduler.start()
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
