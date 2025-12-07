import time
import threading

class Scheduler:
    def __init__(self, manager):
        self.manager = manager
        self.running = False

    def start(self):
        self.running = True
        t = threading.Thread(target=self.loop, daemon=True)
        t.start()

    def stop(self):
        self.running = False

    def loop(self):
        while self.running:
            # Esegui task periodici, workflow multi-step, automazioni
            self.manager.run_task("system", {"action": "check"})
            time.sleep(10)
