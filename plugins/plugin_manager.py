class PluginManager:
    def __init__(self):
        self.plugins = []
    def load_plugin(self, plugin):
        self.plugins.append(plugin)
    def list_plugins(self):
        return self.plugins
