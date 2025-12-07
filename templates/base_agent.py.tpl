class BaseAgent:
    def __init__(self, name):
        self.name = name
    def act(self):
        print(f"Agente {self.name} in azione!")
