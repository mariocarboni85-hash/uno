"""
Supervisor: monitora agenti, task e log
"""
class Supervisor:
    def __init__(self):
        self.agents = []
        self.logs = []

    def register_agent(self, agent):
        self.agents.append(agent)
        self.logs.append(f"Agente registrato: {agent.name}")

    def log(self, message):
        self.logs.append(message)
