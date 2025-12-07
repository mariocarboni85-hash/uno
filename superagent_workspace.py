# DEPRECATO: Tutta la logica è stata spostata in super_agent_workspace/core/workspace_app.py
# Usa solo la nuova struttura modulare.

import os
import openai
# --- Funzione AI OpenAI ---
def query_ai_model(prompt, history=None):
    openai.api_key = os.getenv("OPENAI_API_KEY")  # oppure inserisci direttamente la chiave qui
    from openai.types.chat import (
        ChatCompletionSystemMessageParam,
        ChatCompletionUserMessageParam,
        ChatCompletionAssistantMessageParam
    )
    def to_param(msg):
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if role == "system":
            return ChatCompletionSystemMessageParam(role=role, content=content)
        elif role == "assistant":
            return ChatCompletionAssistantMessageParam(role=role, content=content)
        else:
            return ChatCompletionUserMessageParam(role=role, content=content)
    messages = [to_param({"role": "system", "content": "Sei un assistente Python."})]
    if history:
        messages += [to_param(m) for m in history]
    messages.append(to_param({"role": "user", "content": prompt}))
    # Compatibilità OpenAI >=1.0.0
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=512,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[Errore OpenAI] {e}"
from PyQt5.QtGui import QFont, QColor, QTextCharFormat, QSyntaxHighlighter
from PyQt5.QtCore import QProcess
# -------------------------------
# Evidenziazione Python (PythonHighlighter)
# -------------------------------
class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.keywords = [
            'and', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif',
            'else', 'except', 'exec', 'finally', 'for', 'from', 'global', 'if',
            'import', 'in', 'is', 'lambda', 'not', 'or', 'pass', 'print', 'raise',
            'return', 'try', 'while', 'with', 'yield', 'as', 'async', 'await'
        ]

    def highlightBlock(self, text):
        if not isinstance(text, str):
            return
        fmt_kw = QTextCharFormat()
        fmt_kw.setForeground(QColor('#c678dd'))
        fmt_comment = QTextCharFormat()
        fmt_comment.setForeground(QColor('#7f848e'))
        fmt_string = QTextCharFormat()
        fmt_string.setForeground(QColor('#98c379'))

        words = text.split()
        for word in words:
            w = word.strip('():,')
            if w in self.keywords:
                idx = text.find(w)
                if idx >= 0:
                    self.setFormat(idx, len(w), fmt_kw)

        # comments
        if '#' in text:
            idx = text.find('#')
            self.setFormat(idx, len(text) - idx, fmt_comment)

        # strings (naive)
        i1 = text.find('"')
        i2 = text.rfind('"')
        if i1 != -1 and i2 != -1 and i2 > i1:
            self.setFormat(i1, i2 - i1 + 1, fmt_string)
        i1 = text.find("'")
        i2 = text.rfind("'")
        if i1 != -1 and i2 != -1 and i2 > i1:
            self.setFormat(i1, i2 - i1 + 1, fmt_string)

import bdb
import types
LeftDockWidgetArea = 1
RightDockWidgetArea = 2
from PyQt5.QtCore import QTimer, pyqtSignal
import sys
import threading
import jedi
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QMenuBar, QAction, QFileDialog, QVBoxLayout, QWidget, QLabel,
    QTreeView, QSplitter, QHBoxLayout, QMessageBox, QInputDialog, QAbstractItemView, QPushButton, QMenu,
    QPlainTextEdit, QLineEdit, QListWidget, QFormLayout, QDialog, QDialogButtonBox, QListWidgetItem,
    QDockWidget, QListView, QGroupBox, QStackedWidget
)

# Debugger Python semplice per step, breakpoint, call stack, variabili



# --- Classe principale consolidata ---
from PyQt5.QtWidgets import QMainWindow
class SuperAgentWorkspace(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Super Agent Workspace")
        self.setGeometry(100, 100, 900, 600)
        self.logger = SuperAgentLogger()
        self.logger.log("workspace_start", {"user": os.getlogin()})
        self._chat_history = []
        self._python_ns = {}
        self._init_ui()

    def _init_ui(self):
        # Menu
        menubar = QMenuBar(self)
        file_menu = menubar.addMenu("File")
        if file_menu is not None:
            open_action = QAction("Apri...", self)
            # open_action.triggered.connect(self.open_file)  # Da implementare se serve
            file_menu.addAction(open_action)

        # --- Menu Temi ---
        theme_menu = menubar.addMenu("Tema")
        self.theme_actions = {}
        themes = [
            ("Dark", self.apply_dark_theme),
            ("Light", self.apply_light_theme),
            ("High Contrast", self.apply_high_contrast_theme),
            ("Custom .qss", self.apply_custom_qss_theme)
        ]
        if theme_menu is not None:
            for name, func in themes:
                action = QAction(name, self)
                action.triggered.connect(func)
                theme_menu.addAction(action)
                self.theme_actions[name] = action
        self.setMenuBar(menubar)

        # Layout principale moderno con QStackedWidget e sidebar
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Sidebar di navigazione
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(140)
        self.sidebar.addItem("Editor")
        self.sidebar.addItem("Chat")
        self.sidebar.addItem("Debug")
        self.sidebar.addItem("Impostazioni")
        main_layout.addWidget(self.sidebar)

        # QStackedWidget per le viste
        self.stacked = QStackedWidget()
        main_layout.addWidget(self.stacked)

        # --- Vista Editor ---
        editor_page = QWidget()
        editor_layout = QVBoxLayout()
        editor_page.setLayout(editor_layout)
        # Barra ricerca globale
        search_hbox = QHBoxLayout()
        self.search_input = QLineEdit()
        search_hbox.addWidget(self.search_input)
        self.search_btn = QPushButton("Cerca")
        search_hbox.addWidget(self.search_btn)
        editor_layout.addLayout(search_hbox)
        # Editor avanzato
        self.editor = EditorAvanzato()
        editor_layout.addWidget(self.editor)
        # Pulsanti lint/format
        lint_format_hbox = QHBoxLayout()
        self.lint_btn = QPushButton("Lint")
        self.lint_btn.clicked.connect(self.lint_editor_code)
        lint_format_hbox.addWidget(self.lint_btn)
        self.format_btn = QPushButton("Formatta")
        self.format_btn.clicked.connect(self.format_editor_code)
        lint_format_hbox.addWidget(self.format_btn)
        editor_layout.addLayout(lint_format_hbox)
        # Risultati lint
        self.lint_results = QLabel("")
        editor_layout.addWidget(self.lint_results)
        self.stacked.addWidget(editor_page)

        # --- Vista Chat ---
        chat_page = QWidget()
        chat_layout = QVBoxLayout()
        chat_page.setLayout(chat_layout)
        self.chat_display = QPlainTextEdit()
        self.chat_display.setReadOnly(True)
        chat_layout.addWidget(QLabel("Chat AI:"))
        chat_layout.addWidget(self.chat_display)
        # Terminale reale con QProcess
        self.terminal_output = QPlainTextEdit()
        self.terminal_output.setReadOnly(True)
        self.terminal_input = QLineEdit()
        self.terminal_input.setPlaceholderText("Comando shell...")
        chat_layout.addWidget(QLabel("Terminale:"))
        chat_layout.addWidget(self.terminal_output)
        chat_layout.addWidget(self.terminal_input)
        # Pulsante esecuzione codice
        self.execute_button = QPushButton("Esegui codice")
        self.execute_button.clicked.connect(self.execute_code)
        chat_layout.addWidget(self.execute_button)
        self.stacked.addWidget(chat_page)

        # --- Vista Debug ---
        debug_page = QWidget()
        debug_layout = QVBoxLayout()
        debug_page.setLayout(debug_layout)
        self.breakpoint_list = QListWidget()
        self.breakpoint_list.setSelectionMode(QAbstractItemView.SingleSelection)
        debug_layout.addWidget(QLabel("Breakpoint:"))
        debug_layout.addWidget(self.breakpoint_list)
        step_hbox = QHBoxLayout()
        self.btn_step_in = QPushButton("Step In")
        self.btn_step_out = QPushButton("Step Out")
        self.btn_continue = QPushButton("Continua")
        # self.btn_step_in.clicked.connect(self.step_in)  # Da implementare
        # self.btn_step_out.clicked.connect(self.step_out)  # Da implementare
        # self.btn_continue.clicked.connect(self.continue_debug)  # Da implementare
        step_hbox.addWidget(self.btn_step_in)
        step_hbox.addWidget(self.btn_step_out)
        step_hbox.addWidget(self.btn_continue)
        debug_layout.addLayout(step_hbox)
        self.callstack_list = QListWidget()
        debug_layout.addWidget(QLabel("Call Stack:"))
        debug_layout.addWidget(self.callstack_list)
        self.vars_list = QListWidget()
        debug_layout.addWidget(QLabel("Variabili:"))
        debug_layout.addWidget(self.vars_list)
        self.stacked.addWidget(debug_page)

        # --- Vista Impostazioni (placeholder) ---
        settings_page = QWidget()
        settings_layout = QVBoxLayout()
        settings_page.setLayout(settings_layout)
        settings_layout.addWidget(QLabel("Impostazioni e preferenze (in sviluppo)"))
        self.stacked.addWidget(settings_page)

        # Sidebar navigation logic
        self.sidebar.currentRowChanged.connect(self.stacked.setCurrentIndex)
        self.sidebar.setCurrentRow(0)

        # Temi di default
        self.apply_dark_theme()

    # --- Chat AI avanzata ---
    def ai_response(self, message):
        if not hasattr(self, '_chat_history'):
            self._chat_history = []
        if not hasattr(self, '_python_ns'):
            self._python_ns = {}
        msg = message.strip()
        # Comandi speciali
        if msg.lower().startswith("/templates"):
            templates = self.list_templates() if hasattr(self, 'list_templates') else []
            if templates:
                result = "Template disponibili: " + ", ".join(templates)
            else:
                result = "Nessun template trovato in /templates."
            self._chat_history.append({'role': 'assistant', 'content': result})
            self.save_chat_history_json()
            self.save_chat_history_md()
            return result
        if msg.lower().startswith("/genera agente"):
            import shlex
            parts = shlex.split(msg)
            if len(parts) >= 4 and hasattr(self, 'generate_agent_from_template'):
                template = parts[2]
                agent_name = parts[3]
                variables = {}
                for p in parts[4:]:
                    if '=' in p:
                        k, v = p.split('=', 1)
                        variables[k] = v
                result = self.generate_agent_from_template(template, agent_name, variables)
            else:
                result = "Uso: /genera agente <template> <NomeAgente> [chiave=val ...]"
            self._chat_history.append({'role': 'assistant', 'content': result})
            self.save_chat_history_json()
            self.save_chat_history_md()
            return result
        # --- Integrazione AI: chiama OpenAI se non comando speciale ---
        self._chat_history.append({'role': 'user', 'content': message})
        self.save_chat_history_json()
        self.save_chat_history_md()
        # Prepara history per OpenAI (solo ultimi 10 messaggi)
        history = [
            {'role': m['role'], 'content': m['content']}
            for m in self._chat_history[-10:] if m['role'] in ('user', 'assistant')
        ]
        # Conversione per OpenAI >=1.0.0: ogni messaggio deve essere ChatCompletionMessageParam
        ai_reply = query_ai_model(message, history=history)
        self._chat_history.append({'role': 'assistant', 'content': ai_reply})
        self.save_chat_history_json()
        self.save_chat_history_md()
        return ai_reply

    # (Altri metodi consolidati: save_chat_history_json, save_chat_history_md, list_templates, generate_agent_from_template, ecc.)

# --- Fine consolidamento ---

    def _init_ui(self):
        # Menu
        menubar = QMenuBar()
        file_menu = menubar.addMenu("File")
        if file_menu is not None:
            open_action = QAction("Apri...", self)
            open_action.triggered.connect(self.open_file)
            file_menu.addAction(open_action)

        # --- Menu Temi ---
        theme_menu = menubar.addMenu("Tema")
        self.theme_actions = {}
        themes = [
            ("Dark", self.apply_dark_theme),
            ("Light", self.apply_light_theme),
            ("High Contrast", self.apply_high_contrast_theme),
            ("Custom .qss", self.apply_custom_qss_theme)
        ]
        if theme_menu is not None:
            for name, func in themes:
                action = QAction(name, self)
                action.triggered.connect(func)
                theme_menu.addAction(action)
                self.theme_actions[name] = action

        self.setMenuBar(menubar)
    # --- Temi grafici ---
    def apply_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #2b2b2b; }
            QLabel { color: #ffffff; }
            QTreeView, QPlainTextEdit, QTextEdit, QListWidget { background-color: #1e1e1e; color: #ffffff; }
            QPushButton { background-color: #0078d4; color: #ffffff; }
            QPushButton:hover { background-color: #106ebe; }
            QMenuBar { background-color: #333333; color: #ffffff; }
            QStatusBar { background-color: #333333; color: #ffffff; }
        """)

    def apply_light_theme(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #f5f5f5; }
            QLabel { color: #222222; }
            QTreeView, QPlainTextEdit, QTextEdit, QListWidget { background-color: #ffffff; color: #222222; }
            QPushButton { background-color: #e0e0e0; color: #222222; }
            QPushButton:hover { background-color: #cccccc; }
            QMenuBar { background-color: #e0e0e0; color: #222222; }
            QStatusBar { background-color: #e0e0e0; color: #222222; }
        """)

    def apply_high_contrast_theme(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #000000; }
            QLabel { color: #ffff00; font-weight: bold; }
            QTreeView, QPlainTextEdit, QTextEdit, QListWidget { background-color: #000000; color: #ffff00; }
            QPushButton { background-color: #ffff00; color: #000000; font-weight: bold; }
            QPushButton:hover { background-color: #ffea00; }
            QMenuBar { background-color: #000000; color: #ffff00; }
            QStatusBar { background-color: #000000; color: #ffff00; }
        """)

    def apply_custom_qss_theme(self):
        from PyQt5.QtWidgets import QFileDialog
        path, _ = QFileDialog.getOpenFileName(self, "Seleziona file .qss", "", "QSS Files (*.qss)")
        if path:
            with open(path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())

        # Layout principale
        main_layout = QHBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Splitter principale
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(main_splitter)

        # Colonna sinistra: venv e plugin
        left_layout = QVBoxLayout()
        self.venv_sidebar = VenvSidebar()
        left_layout.addWidget(QLabel("Gestione venv:"))
        left_layout.addWidget(self.venv_sidebar)
        self.plugin_manager = PluginManager(logger=self.logger)
        self.plugin_manager.run_all()
        self.plugin_list_widget = PluginListWidget(self.plugin_manager)
        left_layout.addWidget(QLabel("Gestione plugin:"))
        left_layout.addWidget(self.plugin_list_widget)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        main_splitter.addWidget(left_widget)

        # Colonna destra: chat, terminale, esecuzione codice
        right_layout = QVBoxLayout()
        self.chat_display = QPlainTextEdit()
        self.chat_display.setReadOnly(True)
        right_layout.addWidget(QLabel("Chat AI:"))
        right_layout.addWidget(self.chat_display)
        self.terminal_output = QPlainTextEdit()
        self.terminal_output.setReadOnly(True)
        right_layout.addWidget(QLabel("Terminale:"))
        right_layout.addWidget(self.terminal_output)
        self.execute_button = QPushButton("Esegui codice")
        self.execute_button.clicked.connect(self.execute_code)
        right_layout.addWidget(self.execute_button)
        right_widget = QWidget()
        right_widget.setLayout(right_layout)
        main_splitter.addWidget(right_widget)

        # --- Colonna centrale: Editor avanzato + controlli + ricerca ---
        editor_vbox = QVBoxLayout()
        # Barra ricerca globale
        search_hbox = QHBoxLayout()
        self.search_input = QLineEdit()
        search_hbox.addWidget(self.search_input)
        self.search_btn = QPushButton("Cerca")
        search_hbox.addWidget(self.search_btn)
        editor_vbox.addLayout(search_hbox)
        # Editor avanzato
        self.editor = EditorAvanzato()
        editor_vbox.addWidget(self.editor)
        # Pulsanti lint/format
        lint_format_hbox = QHBoxLayout()
        self.lint_btn = QPushButton("Lint")
        self.lint_btn.clicked.connect(self.lint_editor_code)
        lint_format_hbox.addWidget(self.lint_btn)
        self.format_btn = QPushButton("Formatta")
        self.format_btn.clicked.connect(self.format_editor_code)
        lint_format_hbox.addWidget(self.format_btn)
        editor_vbox.addLayout(lint_format_hbox)
        # Risultati lint
        self.lint_results = QLabel("")
        editor_vbox.addWidget(self.lint_results)
        # Widget centrale
        editor_widget = QWidget()
        editor_widget.setLayout(editor_vbox)
        main_splitter.addWidget(editor_widget)

        # --- Debug Sidebar stile VSCode ---
        self.debug_dock = QDockWidget("Debug")
        # self.debug_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)  # Disabilitato per compatibilità
        debug_widget = QWidget()
        debug_layout = QVBoxLayout()
        # Lista breakpoint
        self.breakpoint_list = QListWidget()
        self.breakpoint_list.setSelectionMode(QAbstractItemView.SingleSelection)
        debug_layout.addWidget(QLabel("Breakpoint:"))
        debug_layout.addWidget(self.breakpoint_list)
        # Controlli step
        step_hbox = QHBoxLayout()
        self.btn_step_in = QPushButton("Step In")
        self.btn_step_out = QPushButton("Step Out")
        self.btn_continue = QPushButton("Continua")
        self.btn_step_in.clicked.connect(self.step_in)
        self.btn_step_out.clicked.connect(self.step_out)
        self.btn_continue.clicked.connect(self.continue_debug)
        step_hbox.addWidget(self.btn_step_in)
        step_hbox.addWidget(self.btn_step_out)
        step_hbox.addWidget(self.btn_continue)
        debug_layout.addLayout(step_hbox)
        # Call stack
        debug_layout.addWidget(QLabel("Call Stack:"))
        self.callstack_list = QListWidget()
        debug_layout.addWidget(self.callstack_list)
        # Variabili live
        debug_layout.addWidget(QLabel("Variabili:"))
        self.vars_list = QListWidget()
        debug_layout.addWidget(self.vars_list)
        debug_widget.setLayout(debug_layout)
        self.debug_dock.setWidget(debug_widget)
        # self.addDockWidget(Qt.LeftDockWidgetArea, self.debug_dock)  # Disabilitato per compatibilità
        # Gestione breakpoint click su margine editor
        if self.editor is not None and hasattr(self.editor, 'viewport'):
            viewport = self.editor.viewport()
            if viewport is not None:
                viewport.installEventFilter(self)  # Attivo il filtro eventi per breakpoint
        self.breakpoints = set()

    def eventFilter(self, obj, event):
        # Click sul margine sinistro dell'editor per breakpoint
        if obj == self.editor.viewport() and event.type() == event.MouseButtonPress:
            pos = event.pos()
            if pos.x() < 30:  # margine sinistro
                cursor = self.editor.cursorForPosition(pos)
                line = cursor.blockNumber() + 1
                if line in self.breakpoints:
                    self.breakpoints.remove(line)
                else:
                    self.breakpoints.add(line)
                self.update_breakpoint_list()
                return True
        return QMainWindow.eventFilter(self, obj, event)

    def update_breakpoint_list(self):
        self.breakpoint_list.clear()
        for line in sorted(self.breakpoints):
            self.breakpoint_list.addItem(f"Linea {line}")

    def start_debug(self):
        code = self.editor.toPlainText()
        # self.debugger = SimpleDebugger(self.on_debug_update)  # Rimosso: SimpleDebugger non più definito
        for line in self.breakpoints:
            self.debugger.set_break("<editor>", line)
        g = {}
        # Disabilita i pulsanti durante l'esecuzione
        self.btn_step_in.setEnabled(True)
        self.btn_step_out.setEnabled(True)
        self.btn_continue.setEnabled(True)
        self.debugger.run_code(code, g)

    def on_debug_update(self, dbg):
        self.callstack_list.clear()
        for frame, _ in dbg.stack:
            self.callstack_list.addItem(f"{frame.f_code.co_name} @ {frame.f_lineno}")
        self.vars_list.clear()
        for k, v in dbg.locals.items():
            self.vars_list.addItem(f"{k} = {v}")
        # Se il debugger ha terminato, disabilita i pulsanti
        if not dbg.frame:
            self.btn_step_in.setEnabled(False)
            self.btn_step_out.setEnabled(False)
            self.btn_continue.setEnabled(False)

    def step_in(self):
        if hasattr(self, 'debugger') and self.btn_step_in.isEnabled():
            self.debugger.set_step()

    def step_out(self):
        if hasattr(self, 'debugger') and self.btn_step_out.isEnabled():
            frame = getattr(self.debugger, 'frame', None)
            if frame is not None:
                self.debugger.set_return(frame)

    def continue_debug(self):
        if hasattr(self, 'debugger') and self.btn_continue.isEnabled():
            self.debugger.set_continue()

    def lint_editor_code(self):
        self.editor.lint_code()

    def format_editor_code(self):
        self.editor.format_code()

    def show_lint_results(self, result):
        self.lint_results.setText(result)



class EditorAvanzato(QPlainTextEdit):
    lintResult = pyqtSignal(str)
    formatResult = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.completion_list = QListWidget(self)
        self.completion_list.hide()
        self.textChanged.connect(self.schedule_autocomplete)
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.show_completions)
        self.completion_list.itemClicked.connect(self.insert_completion)
        self.setFont(QFont('Consolas', 11))
        self.highlighter = PythonHighlighter(self.document())

    def lint_code(self):
        code = self.toPlainText()
        def run_lint():
            result = ""
            try:
                proc = subprocess.Popen([
                    sys.executable, '-m', 'pylsp', '--check', '--stdin'
                ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                out, err = proc.communicate(code, timeout=10)
                result = out + err
            except Exception as e:
                result = str(e)
            self.lintResult.emit(result)
        threading.Thread(target=run_lint, daemon=True).start()

    # def _init_ui(self):
        # Menu
        menubar = QMenuBar()
        file_menu = menubar.addMenu("File")
        if file_menu is not None:
            open_action = QAction("Apri...", self)
            open_action.triggered.connect(self.open_file)
            file_menu.addAction(open_action)

        # --- Menu Temi ---
        theme_menu = menubar.addMenu("Tema")
        self.theme_actions = {}
        themes = [
            ("Dark", self.apply_dark_theme),
            ("Light", self.apply_light_theme),
            ("High Contrast", self.apply_high_contrast_theme),
            ("Custom .qss", self.apply_custom_qss_theme)
        ]
        if theme_menu is not None:
            for name, func in themes:
                action = QAction(name, self)
                action.triggered.connect(func)
                theme_menu.addAction(action)
                self.theme_actions[name] = action

        self.setMenuBar(menubar)

        # --- Layout moderno con QStackedWidget e sidebar ---
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Sidebar di navigazione
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(140)
        self.sidebar.addItem("Editor")
        self.sidebar.addItem("Chat")
        self.sidebar.addItem("Debug")
        self.sidebar.addItem("Impostazioni")
        main_layout.addWidget(self.sidebar)

        # QStackedWidget per le viste
        self.stacked = QStackedWidget()
        main_layout.addWidget(self.stacked)

        # --- Vista Editor ---
        editor_page = QWidget()
        editor_layout = QVBoxLayout()
        editor_page.setLayout(editor_layout)
        # Barra ricerca globale
        search_hbox = QHBoxLayout()
        self.search_input = QLineEdit()
        search_hbox.addWidget(self.search_input)
        self.search_btn = QPushButton("Cerca")
        search_hbox.addWidget(self.search_btn)
        editor_layout.addLayout(search_hbox)
        # Editor avanzato
        self.editor = EditorAvanzato()
        editor_layout.addWidget(self.editor)
        # Pulsanti lint/format
        lint_format_hbox = QHBoxLayout()
        self.lint_btn = QPushButton("Lint")
        self.lint_btn.clicked.connect(self.lint_editor_code)
        lint_format_hbox.addWidget(self.lint_btn)
        self.format_btn = QPushButton("Formatta")
        self.format_btn.clicked.connect(self.format_editor_code)
        lint_format_hbox.addWidget(self.format_btn)
        editor_layout.addLayout(lint_format_hbox)
        # Risultati lint
        self.lint_results = QLabel("")
        editor_layout.addWidget(self.lint_results)
        self.stacked.addWidget(editor_page)

        # --- Vista Chat ---
        chat_page = QWidget()
        chat_layout = QVBoxLayout()
        chat_page.setLayout(chat_layout)
        self.chat_display = QPlainTextEdit()
        self.chat_display.setReadOnly(True)
        chat_layout.addWidget(QLabel("Chat AI:"))
        chat_layout.addWidget(self.chat_display)
        # Terminale reale con QProcess
        self.terminal_output = QPlainTextEdit()
        self.terminal_output.setReadOnly(True)
        self.terminal_input = QLineEdit()
        self.terminal_input.setPlaceholderText("Comando shell...")
        chat_layout.addWidget(QLabel("Terminale:"))
        chat_layout.addWidget(self.terminal_output)
        chat_layout.addWidget(self.terminal_input)
        self.qprocess = QProcess()
        self.qprocess.readyReadStandardOutput.connect(self.on_process_stdout)
        self.qprocess.readyReadStandardError.connect(self.on_process_stderr)
        self.terminal_input.returnPressed.connect(self.on_terminal_command)
        self.execute_button = QPushButton("Esegui codice")
        self.execute_button.clicked.connect(self.execute_code)
        chat_layout.addWidget(self.execute_button)
        self.stacked.addWidget(chat_page)

    def on_terminal_command(self):
        cmd = self.terminal_input.text().strip()
        if not cmd:
            return
        self.terminal_output.appendPlainText(f"> {cmd}")
        self.qprocess.start(cmd)
        self.terminal_input.clear()

    def on_process_stdout(self):
        data = self.qprocess.readAllStandardOutput().data().decode()
        self.terminal_output.appendPlainText(data)

    def on_process_stderr(self):
        data = self.qprocess.readAllStandardError().data().decode()
        self.terminal_output.appendPlainText(data)

        # --- Vista Debug ---
        debug_page = QWidget()
        debug_layout = QVBoxLayout()
        debug_page.setLayout(debug_layout)
        self.breakpoint_list = QListWidget()
        self.breakpoint_list.setSelectionMode(QAbstractItemView.SingleSelection)
        debug_layout.addWidget(QLabel("Breakpoint:"))
        debug_layout.addWidget(self.breakpoint_list)
        step_hbox = QHBoxLayout()
        self.btn_step_in = QPushButton("Step In")
        self.btn_step_out = QPushButton("Step Out")
        self.btn_continue = QPushButton("Continua")
        self.btn_step_in.clicked.connect(self.step_in)
        self.btn_step_out.clicked.connect(self.step_out)
        self.btn_continue.clicked.connect(self.continue_debug)
        step_hbox.addWidget(self.btn_step_in)
        step_hbox.addWidget(self.btn_step_out)
        step_hbox.addWidget(self.btn_continue)
        debug_layout.addLayout(step_hbox)
        self.callstack_list = QListWidget()
        debug_layout.addWidget(QLabel("Call Stack:"))
        debug_layout.addWidget(self.callstack_list)
        self.vars_list = QListWidget()
        debug_layout.addWidget(QLabel("Variabili:"))
        debug_layout.addWidget(self.vars_list)
        self.stacked.addWidget(debug_page)

        # --- Vista Impostazioni (placeholder) ---
        settings_page = QWidget()
        settings_layout = QVBoxLayout()
        settings_page.setLayout(settings_layout)
        settings_layout.addWidget(QLabel("Impostazioni e preferenze (in sviluppo)"))
        self.stacked.addWidget(settings_page)

        # Sidebar navigation logic
        self.sidebar.currentRowChanged.connect(self.stacked.setCurrentIndex)
        self.sidebar.setCurrentRow(0)

    def schedule_autocomplete(self):
        self.timer.start(200)

    def show_completions(self):
        cursor = self.textCursor()
        code = self.toPlainText()
        script = jedi.Script(code, path="<editor>")
        try:
            completions = script.complete(line=cursor.blockNumber()+1, column=cursor.columnNumber())
        except Exception:
            completions = []
        if completions:
            self.completion_list.clear()
            for c in completions:
                item = QListWidgetItem(c.name)
                self.completion_list.addItem(item)
            rect = self.cursorRect()
            self.completion_list.setGeometry(rect.x()+self.mapToGlobal(rect.topLeft()).x(),
                                             rect.y()+self.mapToGlobal(rect.topLeft()).y()+20, 200, 120)
            self.completion_list.setCurrentRow(0)
            self.completion_list.show()
        else:
            self.completion_list.hide()

    def insert_completion(self, item):
        if not item:
            return
        cursor = self.textCursor()
        cursor.select(cursor.WordUnderCursor)
        cursor.removeSelectedText()
        cursor.insertText(item.text())
        self.setTextCursor(cursor)
        self.completion_list.hide()
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import subprocess
class TerminalThread(QThread):
    output_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, command, shell=True):
        super().__init__()
        self.command = command
        self.shell = shell

    def run(self):
        try:
            proc = subprocess.Popen(self.command, shell=self.shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if proc.stdout:
                for line in proc.stdout:
                    self.output_signal.emit(line)
            if proc.stderr:
                for line in proc.stderr:
                    self.error_signal.emit(line)
        except Exception as e:
            self.error_signal.emit(str(e))
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileSystemModel

class FileExplorer(QTreeView):
    def __init__(self, parent=None, root_path=None):
        super().__init__(parent)
        self.fs_model = QFileSystemModel()
        self.fs_model.setRootPath(root_path or "")
        self.setModel(self.fs_model)
        self.setRootIndex(self.fs_model.index(root_path or ""))
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setEditTriggers(QAbstractItemView.EditKeyPressed | QAbstractItemView.SelectedClicked)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.open_context_menu)
        self.setHeaderHidden(False)

    def open_context_menu(self, position):
        index = self.indexAt(position)
        if not index.isValid():
            return
        menu = QMenu(self)
        file_path = self.fs_model.filePath(index)
        rename_action = QAction("Rinomina", self)
        rename_action.triggered.connect(lambda: self.rename_item(index))
        delete_action = QAction("Elimina", self)
        delete_action.triggered.connect(lambda: self.delete_item(index))
        menu.addAction(rename_action)
        menu.addAction(delete_action)
        global_pos = self.mapToGlobal(position)
        menu.exec_(global_pos)

    def rename_item(self, index):
        old_name = self.fs_model.fileName(index)
        file_path = self.fs_model.filePath(index)
        new_name, ok = QInputDialog.getText(self, "Rinomina", f"Nuovo nome per '{old_name}':")
        if ok and new_name:
            import os
            new_path = os.path.join(os.path.dirname(file_path), new_name)
            try:
                os.rename(file_path, new_path)
            except Exception as e:
                QMessageBox.warning(self, "Errore", f"Impossibile rinominare: {e}")
            self.fs_model.layoutChanged.emit()

    def delete_item(self, index):
        file_path = self.fs_model.filePath(index)
        import os, shutil
        reply = QMessageBox.question(self, "Elimina", f"Vuoi eliminare '{file_path}'?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                else:
                    os.remove(file_path)
            except Exception as e:
                QMessageBox.warning(self, "Errore", f"Impossibile eliminare: {e}")
            self.fs_model.layoutChanged.emit()

from tools.venv_manager import list_venvs, create_venv, delete_venv, get_venv_info, install_package

class VenvSidebar(QWidget):
    # Costruttore unico già presente, rimuovo duplicato

    def refresh(self):
        self.venv_list.clear()
        envs = list_venvs()
        for env in envs:
            self.venv_list.addItem(env['name'])

    def create_venv(self):
        name, ok = QInputDialog.getText(self, "Nuovo venv", "Nome ambiente:")
        if ok and name:
            result = create_venv(name)
            msg = result.get('message') or result.get('error')
            if self.logger:
                self.logger.log("venv_create", {"name": name, "result": msg})
            QMessageBox.information(self, "Crea venv", msg)
            self.refresh()

    def delete_selected(self):
        item = self.venv_list.currentItem()
        if item:
            name = item.text()
            result = delete_venv(name)
            msg = result.get('message') or result.get('error')
            if self.logger:
                self.logger.log("venv_delete", {"name": name, "result": msg})
            QMessageBox.information(self, "Elimina venv", msg)
            self.refresh()

    def show_info(self):
        item = self.venv_list.currentItem()
        if item:
            name = item.text()
            info = get_venv_info(name)
            dlg = QDialog(self)
            dlg.setWindowTitle(f"Info venv: {name}")
            form = QFormLayout(dlg)
            for k, v in info.items():
                form.addRow(str(k), QLabel(str(v)))
            btns = QDialogButtonBox(QDialogButtonBox.Ok)
            btns.accepted.connect(dlg.accept)
            form.addWidget(btns)
            dlg.setLayout(form)
            dlg.exec_()

    def install_package(self):
        item = self.venv_list.currentItem()
        if item:
            name = item.text()
            pkg, ok = QInputDialog.getText(self, "Installa pacchetto", "Nome pacchetto:")
            if ok and pkg:
                result = install_package(name, pkg)
                msg = result.get('output') or result.get('error')
                if self.logger:
                    self.logger.log("venv_install_package", {"name": name, "package": pkg, "result": msg})
                QMessageBox.information(self, "Installa pacchetto", msg)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Super Agent Workspace")
        self.setGeometry(100, 100, 900, 600)
        self._init_ui()
        self.logger = SuperAgentLogger()
        if self.logger:
            self.logger.log("workspace_start", {"user": os.getlogin()})

    def _init_ui(self):
        # Menu
        menubar = QMenuBar(self)
        file_menu = menubar.addMenu("File")
        if file_menu is not None:
            open_action = QAction("Apri...", self)
            open_action.triggered.connect(self.open_file)
            # Layout principale
            main_layout = QHBoxLayout()
            central_widget = QWidget()
            central_widget.setLayout(main_layout)
            self.setCentralWidget(central_widget)

            # Splitter principale
            main_splitter = QSplitter(Qt.Orientation.Horizontal)
            main_layout.addWidget(main_splitter)

            # --- Colonna centrale: Editor avanzato + controlli + ricerca ---
            editor_vbox = QVBoxLayout()
            # Barra ricerca globale
            search_hbox = QHBoxLayout()
            self.search_input = QLineEdit(self)
            self.search_input.setPlaceholderText("Cerca in tutti i file .py...")
            self.search_btn = QPushButton("Cerca", self)
            self.search_btn.clicked.connect(self.global_search)
            search_hbox.addWidget(self.search_input)
            search_hbox.addWidget(self.search_btn)
            editor_vbox.addLayout(search_hbox)

            editor_controls = QHBoxLayout()
            self.lint_btn = QPushButton("Lint", self)
            self.lint_btn.clicked.connect(self.lint_editor_code)
            self.format_btn = QPushButton("Formatta", self)
            self.format_btn.clicked.connect(self.format_editor_code)
            editor_controls.addWidget(self.lint_btn)
            editor_controls.addWidget(self.format_btn)
            editor_vbox.addLayout(editor_controls)

            self.editor = EditorAvanzato(self)
            self.editor.lintResult.connect(self.show_lint_results)
            self.editor.formatResult.connect(self.show_lint_results)
            editor_vbox.addWidget(self.editor)
            self.lint_results = QLabel("")
            self.lint_results.setStyleSheet("color: orange; background: #222; padding: 2px;")
            editor_vbox.addWidget(self.lint_results)

            # Lista risultati ricerca
            self.search_results = QListWidget(self)
            self.search_results.itemClicked.connect(self.open_search_result)
            editor_vbox.addWidget(self.search_results)

            editor_widget = QWidget()
            editor_widget.setLayout(editor_vbox)
            main_splitter.addWidget(editor_widget)

            # --- Colonna sinistra: File Explorer, venv, plugin ---
            left_layout = QVBoxLayout()
            self.file_explorer = FileExplorer(self, root_path=".")
            self.file_explorer.setMinimumWidth(220)
            left_layout.addWidget(QLabel("File Explorer:"))
            left_layout.addWidget(self.file_explorer)
            self.venv_sidebar = VenvSidebar()
            left_layout.addWidget(QLabel("Gestione venv:"))
            left_layout.addWidget(self.venv_sidebar)
            self.plugin_manager = PluginManager(logger=self.logger)
            self.plugin_manager.run_all()
            self.plugin_list_widget = PluginListWidget(self.plugin_manager, self)
            left_layout.addWidget(QLabel("Gestione plugin:"))
            left_layout.addWidget(self.plugin_list_widget)
            left_widget = QWidget()
            left_widget.setLayout(left_layout)
            main_splitter.addWidget(left_widget)

            # --- Colonna destra: Chat, terminale, esecuzione codice ---
            right_layout = QVBoxLayout()
            self.chat_display = QPlainTextEdit(self)
            self.chat_display.setReadOnly(True)
            right_layout.addWidget(QLabel("Chat AI:"))
            right_layout.addWidget(self.chat_display)
            self.terminal_output = QPlainTextEdit(self)
            self.terminal_output.setReadOnly(True)
            right_layout.addWidget(QLabel("Terminale:"))
            right_layout.addWidget(self.terminal_output)
            self.execute_button = QPushButton("Esegui codice", self)
            self.execute_button.clicked.connect(self.execute_code)
            right_layout.addWidget(self.execute_button)
            right_widget = QWidget()
            right_widget.setLayout(right_layout)
            main_splitter.addWidget(right_widget)

    def lint_editor_code(self):
        self.editor.lint_code()

    def format_editor_code(self):
        self.editor.format_code()

    def show_lint_results(self, result):
        self.lint_results.setText(result)

        # Plugin manager e lista plugin
        self.plugin_manager = PluginManager(logger=self.logger)
        self.plugin_manager.run_all()
        self.plugin_list_widget = PluginListWidget(self.plugin_manager, self)

        # Stile
        self.setStyleSheet("""
            QMainWindow { background-color: #2b2b2b; }
            QLabel { color: #ffffff; }
            QTreeView, QPlainTextEdit, QTextEdit, QListWidget { background-color: #1e1e1e; color: #ffffff; }
            QPushButton { background-color: #0078d4; color: #ffffff; }
            QPushButton:hover { background-color: #106ebe; }
            QMenuBar { background-color: #333333; color: #ffffff; }
            QStatusBar { background-color: #333333; color: #ffffff; }
        """)

        # Terminal thread
        self.terminal_thread = TerminalThread("python -u -i")
        self.terminal_thread.output_signal.connect(self.append_terminal_output)
        self.terminal_thread.error_signal.connect(self.append_terminal_output)
        self.terminal_thread.start()

    def append_terminal_output(self, text):
        self.terminal_output.appendPlainText(text)
        if self.logger:
            self.logger.log("terminal_output", {"output": text})

    def append_terminal_error(self, text):
        self.terminal_output.appendPlainText(f"[Errore] {text}")
        if self.logger:
            self.logger.log("terminal_error", {"error": text})

    def execute_code(self):
        cursor = self.chat_display.textCursor()
        cursor.select(cursor.Document)
        code = cursor.selectedText()
        if code:
            self.terminal_thread = TerminalThread(f"python -c \"{code}\"")
            self.terminal_thread.output_signal.connect(self.append_terminal_output)
            self.terminal_thread.error_signal.connect(self.append_terminal_output)
            self.terminal_thread.start()

    def save_chat_history(self, filename="chat_history.txt"):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.chat_display.toPlainText())

    def save_chat_history_json(self, filename="chat_history.json"):
        if hasattr(self, '_chat_history'):
            import json
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self._chat_history, f, indent=2, ensure_ascii=False)

    def save_chat_history_md(self, filename="chat_history.md"):
        if hasattr(self, '_chat_history'):
            with open(filename, "w", encoding="utf-8") as f:
                for m in self._chat_history:
                    role = m['role']
                    content = m['content']
                    f.write(f"**{role}**: {content}\n\n")

    # --- Chat AI avanzata ---
    def ai_response(self, message):
        # Memoria del contesto (persistente per la sessione)
        if not hasattr(self, '_chat_history'):
            self._chat_history = []  # lista di dict: {role: 'user'|'assistant', 'content': ...}
        if not hasattr(self, '_python_ns'):
            self._python_ns = {}

        # Comandi speciali
        msg = message.strip()
        if msg.lower().startswith("/templates"):
            templates = self.list_templates()
            if templates:
                result = "Template disponibili: " + ", ".join(templates)
            else:
                result = "Nessun template trovato in /templates."
            self._chat_history.append({'role': 'assistant', 'content': result})
            self.save_chat_history_json()
            self.save_chat_history_md()
            return result
        if msg.lower().startswith("/genera agente"):
            # Uso: /genera agente <template> <NomeAgente> [chiave1=val1 chiave2=val2 ...]
            import shlex
            parts = shlex.split(msg)
            if len(parts) >= 4:
                template = parts[2]
                agent_name = parts[3]
                variables = {}
                for p in parts[4:]:
                    if '=' in p:
                        k, v = p.split('=', 1)
                        variables[k] = v
                result = self.generate_agent_from_template(template, agent_name, variables)
            else:
                result = "Uso: /genera agente <template> <NomeAgente> [chiave=val ...]"
            self._chat_history.append({'role': 'assistant', 'content': result})
            self.save_chat_history_json()
            self.save_chat_history_md()
            return result
        if msg.lower() in ('/help', 'help', '?'):
            help_text = (
                "Comandi disponibili:\n"
                "- python: <codice> — esegui codice Python isolato\n"
                "- suggerisci file — suggerisce file Python nella cartella\n"
                "- costruisci agente base — crea una classe BaseAgent\n"
                "- /context — mostra il contesto chat\n"
                "- /clear — cancella la chat\n"
                "- /save — salva la chat in chat_history.txt\n"
                "- /exportmd — esporta la chat in chat_history.md\n"
                "- /help — mostra questo aiuto\n"
            )
            self._chat_history.append({'role': 'assistant', 'content': help_text})
            self.save_chat_history_json()
            self.save_chat_history_md()
            return help_text
        if msg.lower() in ('/clear',):
            self._chat_history = []
            self.chat_display.clear()
            self.save_chat_history_json()
            self.save_chat_history_md()
            return "Chat cancellata."
        if msg.lower() in ('/context',):
            ctx = '\n'.join([f"{m['role']}: {m['content']}" for m in self._chat_history[-10:]])
            self._chat_history.append({'role': 'assistant', 'content': ctx})
            self.save_chat_history_json()
            self.save_chat_history_md()
            return ctx
        if msg.lower() in ('/save',):
            self.save_chat_history()
            self.save_chat_history_json()
            self.save_chat_history_md()
            return "Storico chat salvato in chat_history.txt/json/md."
        if msg.lower() in ('/exportmd',):
            self.save_chat_history_md()
            return "Storico chat esportato in chat_history.md."

        # Aggiungi messaggio utente al contesto
        self._chat_history.append({'role': 'user', 'content': message})
        self.save_chat_history_json()
        self.save_chat_history_md()

        # Esecuzione isolata di codice Python
        if msg.lower().startswith("python:"):
            code = msg[len("python:"):].strip()
            import io, contextlib
            output = io.StringIO()
            try:
                with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
                    exec(code, self._python_ns)
                result = output.getvalue()
            except Exception as e:
                result = f"Errore nell'esecuzione del codice: {e}"
            self._chat_history.append({'role': 'assistant', 'content': result})
            self.save_chat_history_json()
            self.save_chat_history_md()
            return result

        # Comando: suggerimenti file-aware (esempio base)
        if msg.lower().startswith("suggerisci file"):
            import os
            pyfiles = [f for f in os.listdir('.') if f.endswith('.py')]
            result = "File Python disponibili: " + ", ".join(pyfiles)
            self._chat_history.append({'role': 'assistant', 'content': result})
            self.save_chat_history_json()
            self.save_chat_history_md()
            return result

        # Comando: costruisci agente base
        if msg.lower().startswith("costruisci agente base"):
            agent_code = (
                "class BaseAgent:\n"
                "    def __init__(self, name):\n"
                "        self.name = name\n"
                "    def act(self):\n"
                "        print(f'Agente {self.name} in azione!')\n"
            )
            try:
                exec(agent_code, self._python_ns)
                result = "Agente base costruito."
            except Exception as e:
                result = f"Errore nella costruzione agente: {e}"
            self._chat_history.append({'role': 'assistant', 'content': result})
            self.save_chat_history_json()
            self.save_chat_history_md()
            return result

        # Suggerimenti automatici (demo): se l'utente chiede "come..." o "mostra..."
        if msg.lower().startswith("come ") or msg.lower().startswith("mostra "):
            suggestion = "[Suggerimento] Vuoi vedere un esempio di codice Python? Scrivi: python: print('Ciao!')"
            self._chat_history.append({'role': 'assistant', 'content': suggestion})
            self.save_chat_history_json()
            self.save_chat_history_md()
            return suggestion

        # Placeholder: integrazione LLM (demo)
        context = '\n'.join([f"{m['role']}: {m['content']}" for m in self._chat_history[-10:]])
        result = f"[AI] (demo) Ho ricevuto: '{message}'.\nContesto recente:\n{context}"
        self._chat_history.append({'role': 'assistant', 'content': result})
        self.save_chat_history_json()
        self.save_chat_history_md()
        return result

import importlib.util
import json
import os

class PluginManager:
    def __init__(self, plugins_dir="plugins", logger=None):
        self.plugins_dir = plugins_dir
        self.plugins = []
        self.logger = logger
        self.load_plugins()

    def load_plugins(self):
        manifest_path = os.path.join(self.plugins_dir, "manifest.json")
        if not os.path.exists(manifest_path):
            return
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        entry = manifest.get("entry", "main.py")
        entry_path = os.path.join(self.plugins_dir, entry)
        if os.path.exists(entry_path):
            spec = importlib.util.spec_from_file_location("plugin_module", entry_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                self.plugins.append({"manifest": manifest, "module": module})
                if self.logger:
                    self.logger.log("plugin_loaded", {"name": manifest.get("name"), "entry": entry})

    def run_all(self):
        for plugin in self.plugins:
            if hasattr(plugin["module"], "run"):
                plugin["module"].run()
                if self.logger:
                    self.logger.log("plugin_run", {"name": plugin["manifest"].get("name")})

class PluginListWidget(QWidget):
    def __init__(self, plugin_manager, parent=None):
        super().__init__(parent)
        self.plugin_manager = plugin_manager
        self.vlayout = QVBoxLayout()
        self.setLayout(self.vlayout)
        self.label = QLabel("Plugin caricati:")
        self.vlayout.addWidget(self.label)
        self.list_widget = QListWidget()
        self.vlayout.addWidget(self.list_widget)
        self.refresh()

    def refresh(self):
        self.list_widget.clear()
        for plugin in self.plugin_manager.plugins:
            name = plugin["manifest"].get("name", "Sconosciuto")
            version = plugin["manifest"].get("version", "?")
            self.list_widget.addItem(f"{name} v{version}")


import datetime
import logging
import json
from logging.handlers import RotatingFileHandler

class SuperAgentLogger:
    def __init__(self, log_path_json="superagent_log.json", log_path_txt="superagent.log"):
        self.log_path_json = log_path_json
        self.log_path_txt = log_path_txt
        self._ensure_log()
        self.logger = logging.getLogger("SuperAgent")
        self.logger.setLevel(logging.DEBUG)
        # File handler rotativo
        file_handler = RotatingFileHandler(self.log_path_txt, maxBytes=512*1024, backupCount=3, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_fmt = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(file_fmt)
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_fmt = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_fmt)
        # Evita duplicati
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def _ensure_log(self):
        if not os.path.exists(self.log_path_json):
            with open(self.log_path_json, "w", encoding="utf-8") as f:
                f.write("[]")

    def log(self, action, details=None, level="info"):
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "action": action,
            "details": details or {}
        }
        # Log su file JSON (compatibilità)
        try:
            with open(self.log_path_json, "r", encoding="utf-8") as f:
                data = json.load(f)
            data.append(entry)
            with open(self.log_path_json, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"[SuperAgentLogger] Errore log JSON: {e}")
        # Log avanzato su file e console
        msg = f"{action} | {details if details else ''}"
        try:
            if level == "debug":
                self.logger.debug(msg)
            elif level == "warning":
                self.logger.warning(msg)
            elif level == "error":
                self.logger.error(msg)
            else:
                self.logger.info(msg)
        except Exception as e:
            print(f"[SuperAgentLogger] Errore log avanzato: {e}")
