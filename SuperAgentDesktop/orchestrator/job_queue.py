"""
JobQueue: gestisce task autonomi e pipeline
"""
class JobQueue:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def get_next_task(self):
        return self.tasks.pop(0) if self.tasks else None
