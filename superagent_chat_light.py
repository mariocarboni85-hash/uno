import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QTabWidget, QWidget, QTextEdit, QLineEdit, QPushButton, QLabel
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
        layout.addWidget(QLabel("Chat con SuperAgent (modello Hugging Face leggero)"))
        layout.addWidget(self.output)
        layout.addWidget(self.input)
        layout.addWidget(btn_send)
        # Placeholder per upgrade futuri (es. modelli locali, OpenAI, ecc.)
        self.model_backend = "huggingface-flan-t5-small"  # Cambia qui per upgrade

    def send_message(self):
        text = self.input.text().strip()
        if text:
            self.output.append(f"Tu: {text}")
            try:
                from transformers import pipeline
                if not hasattr(self, 'hf_pipe'):
                    self.hf_pipe = pipeline("text2text-generation", model="google/flan-t5-small")
                reply = self.hf_pipe(text, max_length=128, do_sample=True)[0]['generated_text']
                self.output.append(f"SuperAgent: {reply}")
            except Exception as e:
                self.output.append(f"SuperAgent: Errore HuggingFace - {e}")
            self.input.clear()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SuperAgent - Chat Leggera")
        tabs = QTabWidget()
        tabs.addTab(ChatTab(), "Chat")
        # Placeholder: qui puoi aggiungere altre tab in futuro (Team, Log, Evoluzione, ecc.)
        self.setCentralWidget(tabs)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
