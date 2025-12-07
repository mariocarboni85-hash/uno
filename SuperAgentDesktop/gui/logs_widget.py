"""
Visualizzazione log e task, monitoraggio agenti
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit

class LogsWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.logs = QTextEdit()
        self.logs.setReadOnly(True)
        self.logs.setPlaceholderText("Log, task e supervisione agenti...")
        layout.addWidget(self.logs)
