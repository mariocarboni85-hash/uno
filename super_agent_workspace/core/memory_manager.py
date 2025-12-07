import json
from pathlib import Path
from typing import List, Dict

class MemoryManager:
    def __init__(self, base_dir: Path = Path('.')):
        self.base = base_dir / '.workspace_memory'
        self.base.mkdir(parents=True, exist_ok=True)
        self.memfile = self.base / 'memory.json'
        if not self.memfile.exists():
            self._data = {'tasks': [], 'logs': [], 'notes': []}
            self._save()
        else:
            self._load()

    def _load(self):
        with open(self.memfile, 'r', encoding='utf-8') as f:
            self._data = json.load(f)

    def _save(self):
        with open(self.memfile, 'w', encoding='utf-8') as f:
            json.dump(self._data, f, indent=2)

    # Tasks API
    def add_task(self, task: Dict):
        task['id'] = len(self._data['tasks']) + 1
        self._data['tasks'].append(task)
        self._save()
        return task

    def list_tasks(self, status: str = None) -> List[Dict]:
        if status is None:
            return self._data['tasks']
        return [t for t in self._data['tasks'] if t.get('status') == status]

    def update_task(self, task_id: int, **kwargs):
        for t in self._data['tasks']:
            if t.get('id') == task_id:
                t.update(kwargs)
                self._save()
                return t
        raise KeyError('task not found')

    # Logs
    def push_log(self, log: Dict):
        self._data['logs'].append(log)
        self._save()
        return log

    def summary(self):
        return {
            'tasks': len(self._data['tasks']),
            'logs': len(self._data['logs']),
            'notes': len(self._data['notes'])
        }
