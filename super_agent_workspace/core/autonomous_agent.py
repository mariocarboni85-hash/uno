import os
import time
import json
import threading
from collections import deque
from super_agent_workspace.core.operational_agent import OperationalAgent
from super_agent_workspace.core.job_queue import JobQueue, JobWorker


class AutonomousAgent(OperationalAgent):
    def __init__(self, app_ref=None, memory=None, interval=5, job_db_path=None):
        super().__init__(app_ref=app_ref)
        self.memory = memory
        self.interval = interval
        self._running = False
        self._thread = None
        self.plan_history = deque(maxlen=200)
        # Job queue integration
        db_path = job_db_path or os.path.join(os.getcwd(), 'orchestrator', 'jobs.db')
        self.job_queue = JobQueue(db_path=db_path)
        self.job_worker = JobWorker(self.job_queue, self._handle_job)

    def start(self):
        if self._running:
            return 'Autonomous agent already running'
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        # Start job worker
        if not self.job_worker.is_alive():
            self.job_worker.start()
        return 'Autonomous agent started'

    def stop(self):
        self._running = False
        self.job_worker.stop()
        return 'Autonomous agent stopping'

    def _loop(self):
        while self._running:
            try:
                obs = self.observe()
                plan = self.plan(obs)
                self.plan_history.append(plan)
                result = self.execute_plan(plan)
                self.verify(plan, result)
            except Exception as e:
                print('Autonomous error', e)
            time.sleep(self.interval)

    def observe(self):
        ctx = {
            'cwd': os.getcwd(),
            'open_files': self.app.list_open_files() if self.app else [],
            'venvs': self.app.venv_manager.list_venvs() if self.app and hasattr(self.app, 'venv_manager') else []
        }
        if self.memory:
            ctx['memory_summary'] = self.memory.summary() if hasattr(self.memory, 'summary') else None
        return ctx

    def plan(self, context):
        # Se ci sono task in memoria, aggiungili anche alla job queue
        pending = []
        if self.memory and hasattr(self.memory, 'list_tasks'):
            pending = self.memory.list_tasks(status='pending')
            for t in pending:
                # Push solo se non già in coda (semplificato: by id)
                self.job_queue.push({'type': t.get('type'), 'payload': t.get('payload')})
        # Se la coda ha job, non pianificare altro
        job = self.job_queue.pop()
        if job:
            return {'action': 'work_job', 'job': job}
        return {'action': 'health_check'}

    def execute_plan(self, plan):
        a = plan.get('action')
        if a == 'work_job':
            job = plan.get('job')
            return self._handle_job(job['payload'])
        if a == 'work_task':
            task = plan.get('task')
            if task.get('type') == 'generate_agent':
                name = task.get('payload', {}).get('name', 'autogen')
                return self.generate_agent(f'crea un agente {name}')
            return f'No handler for task {task}'
        if a == 'health_check':
            return self.run_shell('echo running health check && python -m py_compile .')
        return 'no-op'

    def _handle_job(self, payload):
        # Gestione payload di job: esempio per 'generate_agent'
        if payload.get('type') == 'generate_agent':
            name = payload.get('payload', {}).get('name', 'autogen')
            return self.generate_agent(f'crea un agente {name}')
        # Altri tipi di job custom
        return f"Job eseguito: {payload}"

    def verify(self, plan, result):
        rec = {'plan': plan, 'result': str(result), 'ts': time.time()}
        if self.memory and hasattr(self.memory, 'push_log'):
            self.memory.push_log(rec)
        print('Plan executed:', rec)
