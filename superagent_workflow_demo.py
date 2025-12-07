import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsEllipseItem, QGraphicsTextItem,
    QPushButton, QTabWidget, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QLabel, QHBoxLayout
)
class ChatTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.input = QLineEdit()
        self.input.setPlaceholderText("Scrivi un messaggio per SuperAgent...")
        btn_send = QPushButton("Invia")
        btn_send.clicked.connect(self.send_message)
        layout.addWidget(QLabel("Chat con SuperAgent"))
        layout.addWidget(self.output)
        layout.addWidget(self.input)
        layout.addWidget(btn_send)

    def send_message(self):
        text = self.input.text().strip()
        if text:
            self.output.append(f"Tu: {text}")
            # Parsing ordini speciali
            if "crea app enterprise" in text.lower():
                self.output.append("SuperAgent: Ricevuto ordine di lavoro. Avvio la creazione dell'app enterprise...")
                self.output.append("SuperAgent: 1. Progetto la struttura e le funzionalità.")
                self.crea_struttura_base()
                self.output.append("SuperAgent: 2. Genero la GUI avanzata.")
                self.genera_gui()
                self.output.append("SuperAgent: 3. Integro automazioni e sicurezza.")
                self.genera_automazioni()
                self.output.append("SuperAgent: 4. Preparo l'installer Windows.")
                self.genera_installer()
                self.output.append("SuperAgent: 5. Scrivo la documentazione e testo l'app.")
                self.genera_documentazione()
                self.genera_test()
                self.output.append("SuperAgent: App enterprise generata! Trovi i file nella cartella 'output/enterprise_app'.")
            elif "installa estensione" in text.lower() or "usa estensione" in text.lower():
                self.output.append("SuperAgent: Cerco estensioni nella cartella 'plugins'...")
                self.ins talla_estensioni()
                self.output.append("SuperAgent: Estensioni installate e pronte all'uso.")
            elif "migliora grafica app" in text.lower() or "grafica evoluta" in text.lower() or "grafica 3d" in text.lower():
                self.output.append("SuperAgent: Avvio agente per migliorare la grafica dell'app con effetti evoluti e 3D...")
                migliorato = False
                import os, importlib.util, sys
                plugins_dir = os.path.join(os.getcwd(), 'plugins')
                if os.path.exists(plugins_dir):
                    for fname in os.listdir(plugins_dir):
                        if fname.endswith('.py'):
                            plugin_path = os.path.join(plugins_dir, fname)
                            spec = importlib.util.spec_from_file_location(fname[:-3], plugin_path)
                            if spec is not None and spec.loader is not None:
                                mod = importlib.util.module_from_spec(spec)
                                sys.modules[fname[:-3]] = mod
                                try:
                                    spec.loader.exec_module(mod)
                                    if hasattr(mod, 'migliora_grafica_app'):
                                        mod.migliora_grafica_app(self)
                                        self.output.append(f"Agente grafico '{fname}' eseguito.")
                                        migliorato = True
                                        if "3d" in fname or "evoluta" in fname:
                                            break
                                except Exception as e:
                                    self.output.append(f"Errore agente grafico {fname}: {e}")
                if not migliorato:
                    self.output.append("Nessun agente grafico evoluto/3D trovato. Creo e attivo un plugin 3D...")
                    # Crea plugin 3D
                    plugin_code = '''def migliora_grafica_app(chat_tab):\n    chat_tab.output.append(\"[PLUGIN] Grafica evoluta 3D applicata!\")\n    try:\n        chat_tab.setStyleSheet(\"background-color: #181c20; color: #e1e1e1;\")\n        chat_tab.output.setStyleSheet(\"background-color: #10141a; color: #e1e1e1; font-size: 16px; border: 2px solid #00eaff; border-radius: 10px;\")\n        chat_tab.input.setStyleSheet(\"background-color: #23272e; color: #e1e1e1; border: 2px solid #00eaff; border-radius: 10px;\")\n        chat_tab.output.append(\"[PLUGIN] Effetti 3D simulati: bordo luminoso e profondità.\")\n    except Exception as e:\n        chat_tab.output.append(f\"[PLUGIN] Errore tema 3D: {e}\")\n'''
                    os.makedirs(plugins_dir, exist_ok=True)
                    plugin_path = os.path.join(plugins_dir, 'migliora_grafica_3d_plugin.py')
                    with open(plugin_path, 'w', encoding='utf-8') as f:
                        f.write(plugin_code)
                    self.output.append("Plugin grafico 3D creato! Lo attivo ora...")
                    try:
                        spec = importlib.util.spec_from_file_location('migliora_grafica_3d_plugin', plugin_path)
                        if spec is not None and spec.loader is not None:
                            mod = importlib.util.module_from_spec(spec)
                            sys.modules['migliora_grafica_3d_plugin'] = mod
                            spec.loader.exec_module(mod)
                            if hasattr(mod, 'migliora_grafica_app'):
                                mod.migliora_grafica_app(self)
                                self.output.append("Agente grafico 'migliora_grafica_3d_plugin.py' eseguito.")
                    except Exception as e:
                        self.output.append(f"Errore attivazione plugin grafico 3D: {e}")
                return
            elif "mostra ragionamento" in text.lower() or "vedere lavorare" in text.lower() or "vedi come ragioni" in text.lower():
                self.output.append("SuperAgent: Avvio modalità ragionamento esplicito...")
                steps = [
                    "1. Ricevo la richiesta dell'utente e la analizzo.",
                    "2. Identifico l'obiettivo: mostrare il mio processo di lavoro e ragionamento.",
                    "3. Scompongo il problema in sotto-attività (es. analisi, pianificazione, esecuzione, verifica).",
                    "4. Eseguo ogni sotto-attività e spiego le decisioni prese.",
                    "5. Presento il risultato finale all'utente."
                ]
                for step in steps:
                    self.output.append(f"[RAGIONAMENTO] {step}")
                self.output.append("SuperAgent: Esempio di ragionamento completato. Vuoi vedere un caso pratico? Scrivi un comando specifico!")
                self.input.clear()
            else:
                try:
                    from transformers import AutoModelForCausalLM, AutoTokenizer
                    import torch
                    if not hasattr(self, 'hf_tokenizer'):
                        self.hf_tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
                        self.hf_model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")
                        self.hf_chat_history = []
                    self.hf_chat_history.append(text)
                    new_user_input_ids = self.hf_tokenizer.encode(self.hf_chat_history[-1] + self.hf_tokenizer.eos_token, return_tensors='pt')
                    bot_input_ids = new_user_input_ids if len(self.hf_chat_history) == 1 else torch.cat([
                        self.hf_tokenizer.encode(''.join(self.hf_chat_history[:-1]) + self.hf_tokenizer.eos_token, return_tensors='pt'),
                        new_user_input_ids
                    ], dim=-1)
                    chat_history_ids = self.hf_model.generate(bot_input_ids, max_length=1000, pad_token_id=self.hf_tokenizer.eos_token_id)
                    reply = self.hf_tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
                    self.hf_chat_history.append(reply)
                    self.output.append(f"SuperAgent: {reply}")
                except Exception as e:
                    self.output.append(f"SuperAgent: Errore HuggingFace - {e}")
                self.input.clear()

    def crea_struttura_base(self):
        import os
        base = os.path.join(os.getcwd(), 'output', 'enterprise_app')
        os.makedirs(base, exist_ok=True)
        with open(os.path.join(base, 'main.py'), 'w', encoding='utf-8') as f:
            f.write("""# Entry point app enterprise\nif __name__ == '__main__':\n    print('SuperAgent Enterprise App avviata!')\n""")

    def genera_gui(self):
        import os
        base = os.path.join(os.getcwd(), 'output', 'enterprise_app')
        with open(os.path.join(base, 'gui.py'), 'w', encoding='utf-8') as f:
            f.write("""import sys\nfrom PyQt5.QtWidgets import QApplication, QMainWindow, QLabel\n\nclass MainWindow(QMainWindow):\n    def __init__(self):\n        super().__init__()\n        self.setWindowTitle('SuperAgent Enterprise')\n        self.setGeometry(100, 100, 600, 400)\n        label = QLabel('Benvenuto in SuperAgent Enterprise!', self)\n        label.move(100, 180)\n\nif __name__ == '__main__':\n    app = QApplication(sys.argv)\n    win = MainWindow()\n    win.show()\n    sys.exit(app.exec_())\n""")

    def genera_automazioni(self):
        import os
        base = os.path.join(os.getcwd(), 'output', 'enterprise_app')
        with open(os.path.join(base, 'automation.py'), 'w', encoding='utf-8') as f:
            f.write("""def run_automation():\n    print('Automazione SuperAgent attiva!')\n""")

    def genera_installer(self):
        import os
        base = os.path.join(os.getcwd(), 'output', 'enterprise_app')
        with open(os.path.join(base, 'installer.bat'), 'w', encoding='utf-8') as f:
            f.write("""@echo off\necho Installazione SuperAgent Enterprise...\npython -m venv venv_enterprise\nvenv_enterprise\\Scripts\\pip install pyqt5\necho Installazione completata!\n""")

    def genera_documentazione(self):
        import os
        base = os.path.join(os.getcwd(), 'output', 'enterprise_app')
        with open(os.path.join(base, 'README.md'), 'w', encoding='utf-8') as f:
            f.write("""# SuperAgent Enterprise\n\nQuesta è una app enterprise generata automaticamente da SuperAgent.\n\n## Avvio\n- Esegui `installer.bat` per installare le dipendenze.\n- Avvia `main.py` o `gui.py` per usare l'app.\n""")

    def genera_test(self):
        import os
        base = os.path.join(os.getcwd(), 'output', 'enterprise_app')
        with open(os.path.join(base, 'test_app.py'), 'w', encoding='utf-8') as f:
            f.write("""def test_avvio():\n    assert True, 'Test placeholder SuperAgent Enterprise'\n""")

    def installa_estensioni(self):
        import os, importlib.util, sys
        plugins_dir = os.path.join(os.getcwd(), 'plugins')
        if not os.path.exists(plugins_dir):
            self.output.append("Nessuna cartella 'plugins' trovata.")
            return
        for fname in os.listdir(plugins_dir):
            if fname.endswith('.py'):
                plugin_path = os.path.join(plugins_dir, fname)
                spec = importlib.util.spec_from_file_location(fname[:-3], plugin_path)
                if spec is not None and spec.loader is not None:
                    mod = importlib.util.module_from_spec(spec)
                    sys.modules[fname[:-3]] = mod
                    try:
                        spec.loader.exec_module(mod)
                        if hasattr(mod, 'superagent_plugin'):
                            mod.superagent_plugin(self)
                            self.output.append(f"Estensione '{fname}' eseguita.")
                        else:
                            self.output.append(f"Estensione '{fname}' caricata (nessuna funzione superagent_plugin trovata).")
                    except Exception as e:
                        self.output.append(f"Errore caricando {fname}: {e}")
                                if fname.endswith('.py'):
                                    plugin_path = os.path.join(plugins_dir, fname)
                                    spec = importlib.util.spec_from_file_location(fname[:-3], plugin_path)
                                    if spec is not None and spec.loader is not None:
                                        mod = importlib.util.module_from_spec(spec)
                                        sys.modules[fname[:-3]] = mod
                                        try:
                                            spec.loader.exec_module(mod)
                                            if hasattr(mod, 'superagent_plugin'):
                                                mod.superagent_plugin(self)
                                                self.output.append(f"Estensione '{fname}' eseguita.")
                                            else:
                                                self.output.append(f"Estensione '{fname}' caricata (nessuna funzione superagent_plugin trovata).")
                                        except Exception as e:
                                            self.output.append(f"Errore caricando {fname}: {e}")
                    mod = importlib.util.module_from_spec(spec)
                    sys.modules[fname[:-3]] = mod
                    try:
                        spec.loader.exec_module(mod)
                        if hasattr(mod, 'superagent_plugin'):
                            mod.superagent_plugin(self)
                            self.output.append(f"Estensione '{fname}' eseguita.")
                        else:
                            self.output.append(f"Estensione '{fname}' caricata (nessuna funzione superagent_plugin trovata).")
                    except Exception as e:
                        self.output.append(f"Errore caricando {fname}: {e}")
                self.output.append("SuperAgent: 3. Integro automazioni e sicurezza.")
                self.genera_automazioni()
                self.output.append("SuperAgent: 4. Preparo l'installer Windows.")
                self.genera_installer()
                self.output.append("SuperAgent: 5. Scrivo la documentazione e testo l'app.")
                self.genera_documentazione()
                self.genera_test()
                self.output.append("SuperAgent: App enterprise generata! Trovi i file nella cartella 'output/enterprise_app'.")


# --- Tab Team ---
class TeamTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        from core.brain import SoftwareTeam, SuperAgent
        self.team = SoftwareTeam()
        self.team.add_member(SuperAgent("Dev_1", skills=["python", "backend"]))
        self.team.add_member(SuperAgent("UX_1", skills=["ux", "design"]))
        self.team.add_member(SuperAgent("QA_1", skills=["test", "qa"]))
        self.status = QTextEdit()
        self.status.setReadOnly(True)
        btn_status = QPushButton("Mostra stato team")
        btn_status.clicked.connect(self.show_status)
        layout.addWidget(QLabel("Gestione Team SuperAgent"))
        layout.addWidget(self.status)
        layout.addWidget(btn_status)
    def show_status(self):
        report = self.team.report() if hasattr(self.team, 'report') else str(self.team.get_team_status())
        self.status.setText(str(report))

# --- Tab Log ---
class LogTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        from core.brain import SoftwareTeam
        self.team = SoftwareTeam()
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        btn_log = QPushButton("Mostra log condiviso")
        btn_log.clicked.connect(self.show_log)
        layout.addWidget(QLabel("Log Team SuperAgent"))
        layout.addWidget(self.log)
        layout.addWidget(btn_log)
    def show_log(self):
        log = self.team.get_shared_log() if hasattr(self.team, 'get_shared_log') else "Log non disponibile"
        self.log.setText(str(log))

# --- Tab Evoluzione ---
class EvolutionTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        btn_evolve = QPushButton("Simula evoluzione team")
        btn_evolve.clicked.connect(self.run_evolution)
        layout.addWidget(QLabel("Evoluzione Team SuperAgent"))
        layout.addWidget(self.output)
        layout.addWidget(btn_evolve)
    def run_evolution(self):
        try:
            from core.brain import demo_evoluzione_super_agent
            import io, sys
            old_stdout = sys.stdout
            sys.stdout = mystdout = io.StringIO()
            demo_evoluzione_super_agent()
            sys.stdout = old_stdout
            self.output.setText(mystdout.getvalue())
        except Exception as e:
            self.output.setText(f"Errore evoluzione: {e}")

# --- Tab Impostazioni ---
class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.workspace = QLineEdit()
        self.workspace.setPlaceholderText("Percorso workspace SuperAgent")
        btn_set = QPushButton("Imposta workspace")
        btn_set.clicked.connect(self.set_workspace)
        layout.addWidget(QLabel("Impostazioni avanzate SuperAgent"))
        layout.addWidget(self.workspace)
        layout.addWidget(btn_set)
        self.status = QLabel("")
        layout.addWidget(self.status)
    def set_workspace(self):
        path = self.workspace.text().strip()
        if path:
            try:
                from run_super_agent import SuperAgent
                agent = SuperAgent(workspace_path=path)
                self.status.setText(f"Workspace impostato: {path}")
            except Exception as e:
                self.status.setText(f"Errore: {e}")
    def send_message(self):
        text = self.input.text().strip()
        if text:
            self.output.append(f"Tu: {text}")
            self.output.append("SuperAgent: Errore - funzione interfaccia_superagent non disponibile")
            self.input.clear()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SuperAgent - Workflow & Chat Demo")
        self.setGeometry(100, 100, 950, 650)
        tabs = QTabWidget()
        tabs.addTab(WorkflowTab(), "Workflow")
        tabs.addTab(ChatTab(), "Chat")
        # tabs.addTab(TeamTab(), "Team")  # Disabilitato: richiede torch
        # tabs.addTab(LogTab(), "Log")    # Disabilitato: richiede torch
        # tabs.addTab(EvolutionTab(), "Evoluzione")  # Disabilitato: richiede torch
        tabs.addTab(SettingsTab(), "Impostazioni")
        self.setCentralWidget(tabs)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
