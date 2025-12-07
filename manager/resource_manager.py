class ResourceManager:
    def __init__(self):
        self.resources = {}
    def add_resource(self, name, resource):
        self.resources[name] = resource
    def get_resource(self, name):
        return self.resources.get(name)
    def list_resources(self):
        return list(self.resources.keys())
