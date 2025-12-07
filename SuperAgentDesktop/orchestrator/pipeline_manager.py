"""
PipelineManager: gestione pipeline di task autonome e configurabili
"""
import json
import os

PIPELINE_FILE = 'SuperAgentDesktop/data/pipelines.json'

class PipelineManager:
    def __init__(self):
        self.pipelines = self.load_pipelines()

    def load_pipelines(self):
        if not os.path.exists(PIPELINE_FILE):
            return {}
        with open(PIPELINE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_pipelines(self):
        with open(PIPELINE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.pipelines, f, ensure_ascii=False, indent=2)

    def add_pipeline(self, name, steps):
        self.pipelines[name] = steps
        self.save_pipelines()

    def get_pipeline(self, name):
        return self.pipelines.get(name, [])

    def list_pipelines(self):
        return list(self.pipelines.keys())

    def run_pipeline(self, name, agent_map, chat_callback=None, log_callback=None):
        steps = self.get_pipeline(name)
        for step in steps:
            agent_name = step.get('agent')
            action = step.get('action')
            params = step.get('params', {})
            agent = agent_map.get(agent_name)
            if agent and hasattr(agent, action):
                result = getattr(agent, action)(**params)
                if chat_callback:
                    chat_callback(f"{agent_name}: {result}")
                if log_callback:
                    log_callback(f"Pipeline {name} - {agent_name}.{action}: {result}")
