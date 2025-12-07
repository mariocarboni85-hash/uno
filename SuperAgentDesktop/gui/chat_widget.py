"""
Chat AI collegata agli agenti Software Engineer e App Builder
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton

class ChatWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.input = QLineEdit()
        self.input.setPlaceholderText("Invia un messaggio agli agenti...")
        self.send_btn = QPushButton("Invia")
        self.send_btn.clicked.connect(self.send_message)
        layout.addWidget(self.chat_display)
        layout.addWidget(self.input)
        layout.addWidget(self.send_btn)

    def send_message(self):
        text = self.input.text().strip()
        if text:
            self.chat_display.append(f"Utente: {text}")
            # Qui si collega agli agenti AI (Software Engineer, App Builder)
            self.chat_display.append(f"SuperAgent: [Risposta simulata]")
            self.input.clear()
