import threading
import time
import psutil
import subprocess
from typing import Dict

class Supervisor:
    def __init__(self, check_interval=5, restart_limit=3):
        self.agents = {}  # name -> dict{cmd, proc, restarts}
        self.check_interval = check_interval
        self.restart_limit = restart_limit
        self._running = False
        self._thread = None

    def register_agent(self, name: str, cmd: list):
        self.agents[name] = {'cmd': cmd, 'proc': None, 'restarts': 0, 'last_status': 'stopped'}

    def start(self):
        if self._running:
            return 'Supervisor already running'
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        return 'Supervisor started'

    def stop(self):
        self._running = False
        return 'Supervisor stopping'

    def _start_proc(self, name):
        info = self.agents[name]
        if info['proc'] and info['proc'].poll() is None:
            return  # already running
        try:
            p = subprocess.Popen(info['cmd'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            info['proc'] = p
            info['last_status'] = 'running'
            info['restarts'] = 0
        except Exception as e:
            info['last_status'] = f'error: {e}'

    def _monitor(self, name):
        info = self.agents[name]
        p = info.get('proc')
        if not p:
            return
        if p.poll() is None:
            info['last_status'] = 'running'
            return
        # process exited
        info['last_status'] = f'exited code {p.returncode}'
        if info['restarts'] < self.restart_limit:
            info['restarts'] += 1
            self._start_proc(name)
        else:
            info['last_status'] += ' (restart limit reached)'

    def _loop(self):
        while self._running:
            for name in list(self.agents.keys()):
                info = self.agents[name]
                if not info.get('proc'):
                    # start it
                    self._start_proc(name)
                else:
                    self._monitor(name)
            time.sleep(self.check_interval)

    def get_status(self) -> Dict:
        return {name: {'status': info['last_status'], 'restarts': info['restarts']} for (name, info) in self.agents.items()}
