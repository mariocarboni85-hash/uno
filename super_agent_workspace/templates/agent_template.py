
# Template base per agenti

class BaseAgent:
    def __init__(self, name):
        self.name = name
    def act(self):
        print(f"Agente {self.name} in azione!")

class AgentBase:
    def __init__(self, name=None):
        self.name = name
    def handle(self, task):
        return f"AgentBase: gestito task {task}"
