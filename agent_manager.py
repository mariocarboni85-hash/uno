from agents.notifier_agent import NotifierAgent
from agents.system_agent import SystemAgent

class AgentManager:
    def __init__(self):
        self.agents = {
            "notifier": NotifierAgent(),
            "system": SystemAgent()
        }
        self.context_memory = []
        self.plugins = []

    def run_task(self, agent, task):
        if agent in self.agents:
            result = self.agents[agent].run(task)
            self.context_memory.append((agent, task, result))
            return result
        return {"error": "agente non trovato"}

    def add_plugin(self, plugin):
        self.plugins.append(plugin)
        for agent in self.agents.values():
            agent.add_plugin(plugin)

    def get_context_memory(self):
        return self.context_memory
