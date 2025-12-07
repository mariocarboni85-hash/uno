class Agent:
    def __init__(self, name):
        self.name = name
        self.memory = []
        self.plugins = []

    def run(self, task):
        raise NotImplementedError

    def add_plugin(self, plugin):
        self.plugins.append(plugin)

    def remember(self, info):
        self.memory.append(info)

    def get_memory(self):
        return self.memory

class BaseAgent(Agent):
    def __init__(self):
        self.name = 'BaseAgent'
    def run(self, input_data):
        # Logica base agente
        return f'Agente BaseAgent attivo. Input: {input_data}'
