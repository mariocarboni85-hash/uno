class TeamManager:
    def __init__(self):
        self.team = []
    def add_agent(self, agent):
        self.team.append(agent)
    def remove_agent(self, agent):
        self.team.remove(agent)
    def list_agents(self):
        return self.team
