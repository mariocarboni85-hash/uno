class AppBuildSupervisor:
    def __init__(self):
        self.agents = {}
    def register_agent(self, name, cmd):
        self.agents[name] = cmd
    def start(self):
        return "Supervisor avviato"
    def stop(self):
        return "Supervisor fermato"
    def get_status(self):
        return f"Agenti registrati: {list(self.agents.keys())}"