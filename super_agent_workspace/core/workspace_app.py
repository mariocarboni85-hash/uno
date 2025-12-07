print("DEBUG: Inizio workspace_app.py - prima degli import")
from agents.app_builder_agent import AppBuilderAgent
from engines.code_generator import CodeGenerator
from engines.project_architect import ProjectArchitect
from engines.build_engine import BuildEngine
from engines.ui.ux_generator import UIUXGenerator
from engines.apk_builder import APKBuilder
from engines.apple_builder import AppleBuilder
from engines.desktop_builder import DesktopBuilder
from engines.web_builder import WebBuilder
from supervisor.app_build_supervisor import AppBuildSupervisor
from super_agent_workspace.core.operational_agent import OperationalAgent
from super_agent_workspace.core.memory_manager import MemoryManager
from super_agent_workspace.core.job_queue import JobQueue
from super_agent_workspace.core.autopilot import AutoPilot
from super_agent_workspace.core.supervisor import Supervisor
import os
from PyQt5.QtGui import QFont, QColor, QTextCharFormat, QSyntaxHighlighter
from PyQt5.QtCore import QProcess, QTimer, pyqtSignal, Qt, QThread
from PyQt5.QtWidgets import *
import logging
import json
from logging.handlers import RotatingFileHandler
import sys
import threading
import jedi
import importlib.util
import datetime

# --- Classe principale SuperAgentWorkspace (placeholder minimal se non presente) ---
class SuperAgentWorkspace(QMainWindow):
	def __init__(self):
		print("DEBUG: Inizio costruttore SuperAgentWorkspace")
		super().__init__()
		self.setWindowTitle("Super Agent Workspace")
		# Import automatico moduli critici
		self.critical_modules = {}
		for mod in ['openai', 'numpy', 'torch', 'psutil', 'matplotlib', 'scipy', 'jedi', 'plyer', 'zstandard', 'requests', 'pyjwt']:
			self.critical_modules[mod] = OperationalAgent().safe_import(mod)
		# Tema scuro moderno
		dark_stylesheet = """
			QMainWindow { background-color: #232629; }
			QWidget { background-color: #232629; color: #e0e0e0; }
			QPlainTextEdit, QLineEdit { background-color: #181a1b; color: #e0e0e0; border: 1px solid #444; }
			QLabel { color: #e0e0e0; font-weight: bold; }
			QPushButton { background-color: #2d2f31; color: #e0e0e0; border-radius: 6px; padding: 6px 16px; font-weight: bold; }
			QPushButton:hover { background-color: #3a3d40; }
		"""
		self.setStyleSheet(dark_stylesheet)
		# Inizializza memoria, job queue, autopilot e supervisor
		self.memory = MemoryManager()
		self.job_queue = JobQueue()
		self.autopilot = AutoPilot(self.job_queue, self.memory)
		self.supervisor = Supervisor()
		# Registra agenti/engine reali nel Supervisor
		self.supervisor.register_agent('app_builder_agent', ['python', 'agents/app_builder_agent.py'])
		self.supervisor.register_agent('code_generator', ['python', 'engines/code_generator.py'])
		self.supervisor.register_agent('project_architect', ['python', 'engines/project_architect.py'])
		self.supervisor.register_agent('build_engine', ['python', 'engines/build_engine.py'])
		self.supervisor.register_agent('ui_ux_generator', ['python', 'engines/ui/ux_generator.py'])
		self.supervisor.register_agent('apk_builder', ['python', 'engines/apk_builder.py'])
		self.supervisor.register_agent('apple_builder', ['python', 'engines/apple_builder.py'])
		self.supervisor.register_agent('desktop_builder', ['python', 'engines/desktop_builder.py'])
		self.supervisor.register_agent('web_builder', ['python', 'engines/web_builder.py'])
		self.supervisor.register_agent('app_build_supervisor', ['python', 'supervisor/app_build_supervisor.py'])
		# Istanzia agenti e supervisore specifici per app building
		self.app_builder_agent = AppBuilderAgent(self.job_queue, self.memory)
		self.app_supervisor = AppBuildSupervisor()
		self.app_supervisor.register_agent('app_builder', ['python','agents/app_builder_agent.py'])
		self.app_supervisor.start()
		# Istanzia l'agente operativo
		self.operational_agent = OperationalAgent(app_ref=self)
		# UI reale: layout verticale con chat e pulsanti autopilot
		central = QWidget()
		main_layout = QVBoxLayout()
		# Titolo
		title = QLabel("SuperAgent - Chat & Controllo")
		title.setAlignment(Qt.AlignCenter)
		title.setStyleSheet("font-size: 20px; margin-bottom: 12px;")
		main_layout.addWidget(title)
		# Chat
		self.chat_display = QPlainTextEdit()
		self.chat_display.setReadOnly(True)
		self.chat_display.setPlaceholderText("Qui appariranno i messaggi e le risposte dell'agente...")
		main_layout.addWidget(self.chat_display)
		# Input
		input_layout = QHBoxLayout()
		self.chat_input = QLineEdit()
		self.chat_input.setPlaceholderText("Scrivi un comando o una domanda...")
		self.chat_input.returnPressed.connect(self._on_chat_enter)
		input_layout.addWidget(self.chat_input)
		main_layout.addLayout(input_layout)
		# Pulsanti
		btns = QHBoxLayout()
		self.btn_start_ap = QPushButton("▶ AutoPilot")
		self.btn_stop_ap = QPushButton("■ Stop AutoPilot")
		self.btn_start_sup = QPushButton("▶ Supervisor")
		self.btn_stop_sup = QPushButton("■ Stop Supervisor")
		self.btn_status_sup = QPushButton("ℹ Supervisor Status")
		self.btn_start_ap.clicked.connect(self.start_autopilot)
		self.btn_stop_ap.clicked.connect(self.stop_autopilot)
		self.btn_start_sup.clicked.connect(self.start_supervisor)
		self.btn_stop_sup.clicked.connect(self.stop_supervisor)
		self.btn_status_sup.clicked.connect(self.show_supervisor_status)
		btns.addWidget(self.btn_start_ap)
		btns.addWidget(self.btn_stop_ap)
		btns.addWidget(self.btn_start_sup)
		btns.addWidget(self.btn_stop_sup)
		btns.addWidget(self.btn_status_sup)
		main_layout.addLayout(btns)
		central.setLayout(main_layout)
		self.setCentralWidget(central)
		print("DEBUG: Fine costruttore SuperAgentWorkspace")
	def start_supervisor(self):
		resp = self.supervisor.start()
		self.append_chat("system", resp)

	def stop_supervisor(self):
		resp = self.supervisor.stop()
		self.append_chat("system", resp)

	def show_supervisor_status(self):
		status = self.supervisor.get_status()
		self.append_chat("system", f"Supervisor status: {status}")

	def _on_chat_enter(self):
		text = self.chat_input.text().strip()
		vbox = QVBoxLayout()
		self.chat_display = QPlainTextEdit()
		self.chat_display.setReadOnly(True)
		self.chat_input = QLineEdit()
		self.chat_input.returnPressed.connect(self._on_chat_enter)
		vbox.addWidget(QLabel("Chat"))
		vbox.addWidget(self.chat_display)
		vbox.addWidget(self.chat_input)
		# Pulsanti AutoPilot e Supervisor
		btns = QHBoxLayout()
		self.btn_start_ap = QPushButton("Start AutoPilot")
		self.btn_stop_ap = QPushButton("Stop AutoPilot")
		self.btn_start_sup = QPushButton("Start Supervisor")
		self.btn_stop_sup = QPushButton("Stop Supervisor")
		self.btn_status_sup = QPushButton("Supervisor Status")
		self.btn_start_ap.clicked.connect(self.start_autopilot)
		self.btn_stop_ap.clicked.connect(self.stop_autopilot)
		self.btn_start_sup.clicked.connect(self.start_supervisor)
		self.btn_stop_sup.clicked.connect(self.stop_supervisor)
		self.btn_status_sup.clicked.connect(self.show_supervisor_status)
		btns.addWidget(self.btn_start_ap)
		btns.addWidget(self.btn_stop_ap)
		btns.addWidget(self.btn_start_sup)
		btns.addWidget(self.btn_stop_sup)
		btns.addWidget(self.btn_status_sup)
		vbox.addLayout(btns)
		central.setLayout(vbox)
		self.setCentralWidget(central)

	def _on_chat_enter(self):
		text = self.chat_input.text()
		if text.lower() == '!autopilot start':
			self.start_autopilot()
			self.chat_input.clear()
			return
		if text.lower() == '!autopilot stop':
			self.stop_autopilot()
			self.chat_input.clear()
			return
		if text.lower() == '!pipeline prenotazioni':
			self.memory.add_task({
				'type': 'generate_app',
				'platforms': ['ios', 'android'],
				'domain': 'gestione prenotazioni ristorante',
				'status': 'pending'
			})
			self.memory.add_task({
				'type': 'show_architecture',
				'target': 'app',
				'status': 'pending'
			})
			self.memory.add_task({
				'type': 'build',
				'platform': 'android',
				'status': 'pending'
			})
			self.memory.add_task({
				'type': 'build',
				'platform': 'ios',
				'status': 'pending'
			})
			self.append_chat('system', 'Pipeline prenotazioni avviata: generazione app, architettura e build!')
			self.chat_input.clear()
			return
		# Altrimenti passa all'agente operativo
		reasoning = self.operational_agent.get_reasoning(text)
		if reasoning:
			self.append_chat("RAGIONAMENTO", reasoning)
		response = self.operational_agent.handle_message(text)
		self.append_chat("AGENTE", response)
		self.chat_input.clear()
	# Mostra ragionamento logico in chat
	def show_reasoning(self, reasoning):
		self.append_chat("RAGIONAMENTO", reasoning)

	def start_supervisor(self):
		resp = self.supervisor.start()
		self.append_chat("system", resp)

	def stop_supervisor(self):
		resp = self.supervisor.stop()
		self.append_chat("system", resp)

	def show_supervisor_status(self):
		status = self.supervisor.get_status()
		self.append_chat("system", f"Supervisor status: {status}")

	def on_user_message(self, user_message):
		response = self.operational_agent.handle_message(user_message)
		self.append_chat("AGENTE", response)

	def append_chat(self, sender, message):
		if hasattr(self, 'chat_display'):
			self.chat_display.appendPlainText(f"{sender}: {message}")

	# Controllo AutoPilot da UI o script
	def start_autopilot(self):
		resp = self.autopilot.start()
		self.append_chat("system", resp)

	def stop_autopilot(self):
		resp = self.autopilot.stop()
		self.append_chat("system", resp)
		# ...existing code...
