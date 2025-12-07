class TaskScheduler:
    def __init__(self):
        self.tasks = []
    def add_task(self, task):
        self.tasks.append(task)
    def get_next_task(self):
        if self.tasks:
            return self.tasks.pop(0)
        return None
    def list_tasks(self):
        return self.tasks
