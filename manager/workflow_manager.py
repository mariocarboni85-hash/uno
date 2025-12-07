class WorkflowManager:
    def __init__(self):
        self.workflows = []
    def add_workflow(self, workflow):
        self.workflows.append(workflow)
    def list_workflows(self):
        return self.workflows
