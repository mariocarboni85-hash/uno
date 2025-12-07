def _run_unix_limited(cmd, timeout, mem_limit_mb=256, cpu_seconds=5):
    try:
        import resource
        def preexec():
            try:
                resource.setrlimit(resource.RLIMIT_CPU, (cpu_seconds, cpu_seconds+1))
            except (AttributeError, ValueError):
                pass
            try:
                mem_bytes = mem_limit_mb * 1024 * 1024
                resource.setrlimit(resource.RLIMIT_AS, (mem_bytes, mem_bytes))
            except (AttributeError, ValueError):
                pass
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=preexec, text=True)
    except ImportError:
        # resource non disponibile, fallback senza limiti
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        out, err = proc.communicate(timeout=timeout)
        return out + ("\n" + err if err else "")
    except subprocess.TimeoutExpired:
        proc.kill()
        return f"[TIMEOUT after {timeout}s]"

def _run_windows_limited(cmd, timeout):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        out, err = proc.communicate(timeout=timeout)
        return out + ("\n" + err if err else "")
    except subprocess.TimeoutExpired:
        proc.kill()
        return f"[TIMEOUT after {timeout}s]"
import threading
import time
from pathlib import Path
from super_agent_workspace.core.job_queue import JobQueue, JobWorker
from super_agent_workspace.core.memory_manager import MemoryManager
# sandbox opzionale: implementare run_in_sandbox se serve

import subprocess
import tempfile
import os
import sys
import platform

def run_in_sandbox(code: str, timeout: int=10, mem_limit_mb:int=256, cpu_seconds:int=5):
    # write code to temp file and execute with python interpreter
    tf = tempfile.NamedTemporaryFile('w', delete=False, suffix='.py')
    tf.write(code)
    tf.flush(); tf.close()
    cmd = [sys.executable, tf.name]
    try:
        if platform.system().lower() != 'windows':
            out = _run_unix_limited(cmd, timeout, mem_limit_mb=mem_limit_mb, cpu_seconds=cpu_seconds)
        else:
            out = _run_windows_limited(cmd, timeout)
    finally:
        try:
            os.unlink(tf.name)
        except:
            pass
    return out

class AutoPilot:
    """
    AutoPilot: riceve tasks (o genera piani), li mette in job queue e supervisiona l'esecuzione.
    """

    def __init__(self, job_queue: JobQueue, memory: MemoryManager, poll=2.0):
        self.job_queue = job_queue
        self.memory = memory
        self.poll = poll
        self._planner_thread = None
        self._running = False

    def start(self):
        if self._running:
            return "AutoPilot already running"
        self._running = True
        # start worker(s)
        self.worker = JobWorker(self.job_queue, self._execute_job)
        self.worker.start()
        self._planner_thread = threading.Thread(target=self._planner_loop, daemon=True)
        self._planner_thread.start()
        return "AutoPilot started"

    def stop(self):
        self._running = False
        if hasattr(self, 'worker'):
            self.worker.stop()
        return "AutoPilot stopped"

    def _planner_loop(self):
        while self._running:
            # simple planner: if memory has pending tasks, push them
            pending = self.memory.list_tasks(status='pending')
            for t in pending:
                payload = t.copy()
                self.job_queue.push(payload, priority=t.get('priority',50), max_attempts= t.get('max_attempts',3))
                # mark memory task as queued
                self.memory.update_task(t['id'], status='queued')
            time.sleep(self.poll)

    def _execute_job(self, payload: dict):
        """
        Handler executed by JobWorker. Payload describes an action:
        type: 'run_code' / 'run_script' / 'generate_agent' / 'install_pkg'
        """
        typ = payload.get('type')
        if typ == 'run_code':
            code = payload.get('code','')
            # run in sandbox with limits
            out = run_in_sandbox(code=code, timeout=10)
            return out
        if typ == 'run_script':
            path = payload.get('path')
            if not path:
                return 'No script path provided'
            if not isinstance(path, str):
                path = str(path)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    code = f.read()
            except Exception as e:
                return f'Error opening script: {e}'
            return run_in_sandbox(code=code, timeout=30)
        if typ == 'generate_agent':
            name = payload.get('payload', {}).get('name','agent_auto')
            # use template to generate file (simple)
            tpl = (Path.cwd() / 'templates' / 'agent_template.py')
            target = Path.cwd() / 'agents' / f'{name}.py'
            target.parent.mkdir(parents=True, exist_ok=True)
            with open(tpl, 'r', encoding='utf-8') as fr, open(target, 'w', encoding='utf-8') as fw:
                content = fr.read().replace('generated_agent', name)
                fw.write(content)
            return f'Agent {name} generated at {target}'
        # fallback
        return {'status':'unknown task', 'payload': payload}
