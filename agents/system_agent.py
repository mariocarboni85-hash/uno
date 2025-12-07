from agents.base_agent import Agent

class SystemAgent(Agent):
    def __init__(self):
        super().__init__("system")

    def run(self, task):
        # Logica di sistema estendibile
        return {"status": "ok"}
