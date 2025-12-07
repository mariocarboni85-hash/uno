"""
PluginManager: caricamento dinamico di plugin Python da cartella plugins/
"""
import importlib.util
import os

PLUGIN_DIR = 'SuperAgentDesktop/plugins/'

class PluginManager:
    def __init__(self):
        self.plugins = {}
        self.load_plugins()

    def load_plugins(self):
        for fname in os.listdir(PLUGIN_DIR):
            if fname.endswith('.py') and fname != '__init__.py':
                name = fname[:-3]
                path = os.path.join(PLUGIN_DIR, fname)
                spec = importlib.util.spec_from_file_location(name, path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                self.plugins[name] = module

    def get_plugin(self, name):
        return self.plugins.get(name)

    def list_plugins(self):
        return list(self.plugins.keys())
