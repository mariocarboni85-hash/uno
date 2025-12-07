"""
Finestra principale con toolbar, chat, editor, log e supervisione agenti
"""
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QSplitter
from gui.editor_widget import EditorWidget
from gui.chat_widget import ChatWidget
from gui.logs_widget import LogsWidget
from gui.persistence import (
    save_chat_history, load_chat_history,
    save_log_history, load_log_history
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Super Agent Workspace")
        self.resize(1200, 800)
        # UI avanzata: tema chiaro/scuro
        self.is_dark = False
        self.toggle_theme_action = self.menuBar().addAction("Tema chiaro/scuro")
        self.toggle_theme_action.triggered.connect(self.toggle_theme)

    def toggle_theme(self):
        if self.is_dark:
            self.setStyleSheet("")
            self.is_dark = False
        else:
            self.setStyleSheet("QWidget { background-color: #232629; color: #f0f0f0; }")
            self.is_dark = True

    # Ricerca nella chat
    def search_in_chat(self, query):
        results = []
        for line in self.chat.chat_display.toPlainText().split('\n'):
            if query.lower() in line.lower():
                results.append(line)
        return results

    # Cronologia messaggi (già gestita da persistenza)
    def show_chat_history(self):
        history = self.chat.chat_display.toPlainText()
        self.chat.chat_display.append("--- CRONOLOGIA ---\n" + history)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Super Agent Workspace")
        self.resize(1200, 800)
        # Importa componenti core
        from supervisor.supervisor import Supervisor
        from orchestrator.job_queue import JobQueue
        from orchestrator.pipeline_manager import PipelineManager
        from agents.software_engineer_agent import SoftwareEngineerAgent
        from agents.app_builder_agent import AppBuilderAgent

        self.supervisor = Supervisor()
        self.job_queue = JobQueue()
        self.software_agent = SoftwareEngineerAgent()
        self.app_builder = AppBuilderAgent()
        self.supervisor.register_agent(self.software_agent)
        self.supervisor.register_agent(self.app_builder)
        self.pipeline_manager = PipelineManager()

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        splitter = QSplitter()
        self.editor = EditorWidget()
        self.chat = ChatWidget()
        self.logs = LogsWidget()
        splitter.addWidget(self.editor)
        splitter.addWidget(self.chat)
        splitter.addWidget(self.logs)
        layout.addWidget(splitter)
        self.setCentralWidget(central_widget)

        # Carica storico chat e log
        for msg in load_chat_history():
            self.chat.chat_display.append(msg)
        for log in load_log_history():
            self.logs.logs.append(log)

        # Collega chat agli agenti e log
        self.chat.send_btn.clicked.connect(self.handle_chat_message)

    def closeEvent(self, event):
        # Salva storico chat e log alla chiusura
        chat_history = self.chat.chat_display.toPlainText().split('\n')
        save_chat_history(chat_history)
        log_history = self.logs.logs.toPlainText().split('\n')
        save_log_history(log_history)
        event.accept()

    def handle_chat_message(self):
        text = self.chat.input.text().strip()
        if not text:
            return
        self.chat.chat_display.append(f"Utente: {text}")
        # Comandi pipeline
        if text.lower().startswith('!pipeline crea '):
            # Esempio: !pipeline crea demo agent=AppBuilderAgent action=build_app params={"specs":"demo"}
            try:
                parts = text.split(' ', 2)
                name = parts[2].split(' ')[0]
                steps = []
                for step_str in parts[2].split(' ')[1:]:
                    if '=' in step_str:
                        k, v = step_str.split('=', 1)
                        if k == 'agent':
                            step = {'agent': v}
                        elif k == 'action':
                            step['action'] = v
                        elif k == 'params':
                            import json
                            step['params'] = json.loads(v)
                        steps.append(step)
                self.pipeline_manager.add_pipeline(name, steps)
                self.chat.chat_display.append(f"SuperAgent: Pipeline '{name}' creata.")
            except Exception as e:
                self.chat.chat_display.append(f"Errore creazione pipeline: {e}")
            self.chat.input.clear()
            return
        if text.lower().startswith('!pipeline lista'):
            pipelines = self.pipeline_manager.list_pipelines()
            self.chat.chat_display.append(f"Pipeline disponibili: {pipelines}")
            self.chat.input.clear()
            return
        if text.lower().startswith('!pipeline esegui '):
            name = text.split(' ', 2)[2]
            agent_map = {
                'SoftwareEngineerAgent': self.software_agent,
                'AppBuilderAgent': self.app_builder
            }
            self.pipeline_manager.run_pipeline(
                name,
                agent_map,
                chat_callback=self.chat.chat_display.append,
                log_callback=self.logs.logs.append
            )
            self.chat.input.clear()
            return
        # Task agli agenti
        if "app" in text.lower():
            result = self.app_builder.build_app(text)
            self.chat.chat_display.append(f"AppBuilderAgent: {result}")
            self.logs.logs.append(f"Task app: {text}")
        elif "refactor" in text.lower() or "codice" in text.lower():
            result = self.software_agent.handle_task(text)
            self.chat.chat_display.append(f"SoftwareEngineerAgent: {result}")
            self.logs.logs.append(f"Task software: {text}")
        else:
            self.chat.chat_display.append("SuperAgent: [Comando non riconosciuto]")
        self.chat.input.clear()
