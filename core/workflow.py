class Workflow:
    def __init__(self, steps=None):
        self.steps = steps or []
    def add_step(self, step):
        self.steps.append(step)
    def run(self):
        for step in self.steps:
            step()
