from agents.base_agent import Agent

class NotifierAgent(Agent):
    def __init__(self):
        super().__init__("notifier")

    def run(self, task):
        # Logica di notifica estendibile
        return {"status": "notifica inviata"}
