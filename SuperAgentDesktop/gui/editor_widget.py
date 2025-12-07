"""
Editor Python con evidenziazione sintassi
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit

class EditorWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Scrivi o incolla codice Python qui...")
        layout.addWidget(self.editor)
