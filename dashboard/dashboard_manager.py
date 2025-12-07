class DashboardManager:
    def __init__(self):
        self.status = {}
    def update_status(self, key, value):
        self.status[key] = value
    def get_status(self, key):
        return self.status.get(key)
    def all_status(self):
        return self.status
