class Dispatcher:
    def __init__(self, app_ref=None, memory=None):
        self.app = app_ref
        self.memory = memory

    def dispatch(self, text):
        # Esempio: parsing semplice per task queue o intent
        if text.lower().startswith('aggiungi task'):
            if self.memory:
                task = {'type': 'user', 'payload': {'text': text}, 'status': 'pending'}
                self.memory.add_task(task)
                return 'Task aggiunto in memoria.'
            return 'Memory manager non disponibile.'
        # Altri intent o fallback
        return f"Comando ricevuto: {text} (nessuna azione specifica)"
