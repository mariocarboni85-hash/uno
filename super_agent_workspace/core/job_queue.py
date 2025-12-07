import sqlite3
import threading
import time
import json
from typing import Any, Dict, Optional

DB = 'orchestrator/jobs.db'

class JobQueue:
    def __init__(self, db_path=DB):
        import os
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        self.db_path = db_path
        self._init_db()
        self.lock = threading.Lock()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            priority INTEGER DEFAULT 50,
            status TEXT DEFAULT 'pending',
            created_ts REAL,
            attempts INTEGER DEFAULT 0,
            max_attempts INTEGER DEFAULT 3,
            payload TEXT
        )
        ''')
        conn.commit()
        conn.close()

    def push(self, payload: Dict[str, Any], priority:int=50, max_attempts:int=3):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('INSERT INTO jobs (priority, status, created_ts, attempts, max_attempts, payload) VALUES (?,?,?,?,?,?)',
                  (priority, 'pending', time.time(), 0, max_attempts, json.dumps(payload)))
        conn.commit()
        conn.close()

    def pop(self) -> Optional[Dict]:
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            # pick highest priority, oldest
            c.execute("SELECT id, priority, status, created_ts, attempts, max_attempts, payload FROM jobs WHERE status='pending' ORDER BY priority ASC, created_ts ASC LIMIT 1")
            row = c.fetchone()
            if not row:
                conn.close()
                return None
            job_id = row[0]
            c.execute("UPDATE jobs SET status='running' WHERE id=?", (job_id,))
            conn.commit()
            conn.close()
            return {'id': row[0], 'priority': row[1], 'status': row[2], 'created_ts': row[3], 'attempts': row[4], 'max_attempts': row[5], 'payload': json.loads(row[6])}

    def mark_done(self, job_id:int):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("UPDATE jobs SET status='done' WHERE id=?", (job_id,))
        conn.commit(); conn.close()

    def mark_failed(self, job_id:int):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("UPDATE jobs SET status='failed' WHERE id=?", (job_id,))
        conn.commit(); conn.close()

    def increment_attempt(self, job_id:int):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("UPDATE jobs SET attempts = attempts + 1 WHERE id=?", (job_id,))
        conn.commit(); conn.close()

    def requeue_if_needed(self, job):
        if job['attempts'] + 1 < job['max_attempts']:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("UPDATE jobs SET status='pending', attempts=? WHERE id=?", (job['attempts']+1, job['id']))
            conn.commit(); conn.close()
        else:
            self.mark_failed(job['id'])

# Worker thread that processes jobs using a handler function
class JobWorker(threading.Thread):
    def __init__(self, queue:JobQueue, handler, poll_interval=1.0):
        super().__init__(daemon=True)
        self.queue = queue
        self.handler = handler
        self.poll_interval = poll_interval
        self._stopped = False

    def run(self):
        while not self._stopped:
            job = self.queue.pop()
            if job:
                try:
                    result = self.handler(job['payload'])
                    self.queue.mark_done(job['id'])
                except Exception as e:
                    # retry logic
                    self.queue.increment_attempt(job['id'])
                    self.queue.requeue_if_needed(job)
            else:
                time.sleep(self.poll_interval)

    def stop(self):
        self._stopped = True
