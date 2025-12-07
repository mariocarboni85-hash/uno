class Automation:
    def __init__(self):
        self.actions = []
    def add_action(self, action):
        self.actions.append(action)
    def execute(self):
        for action in self.actions:
            action()
