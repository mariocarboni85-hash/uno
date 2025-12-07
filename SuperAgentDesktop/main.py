"""
Entry point dell'app desktop Super Agent Workspace
"""
import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow


def main():
    import argparse
    import time
    parser = argparse.ArgumentParser(description="Super Agent Desktop")
    parser.add_argument('--light', action='store_true', help='Avvia in modalità leggera')
    parser.add_argument('--headless', action='store_true', help='Avvia in modalità headless avanzata')
    args = parser.parse_args()

    if args.light:
        # ================================
        # SUPER AGENT - VERSIONE LEGGERA
        # Core minimale per test locale
        # ================================
        class SuperAgentLite:
            def __init__(self):
                self.name = "Super Agent LITE"
                self.version = "1.0"
                self.status = "idle"

            def info(self):
                return {
                    "name": self.name,
                    "version": self.version,
                    "status": self.status
                }

            def run(self):
                print("🔵 Avvio Super Agent LITE...")
                self.status = "running"
                time.sleep(0.5)
                print("✅ Super Agent LITE avviato (modalità leggera).")

            def process(self, user_input: str):
                user_input = user_input.lower()
                if "ciao" in user_input:
                    return "Ciao Mario! Sono la versione leggera di Super Agent."
                elif "stato" in user_input:
                    return f"Sto funzionando in modalità LITE. RAM minima."
                elif "help" in user_input:
                    return "Posso rispondere a comandi semplici. In modalità LITE non uso AI pesante."
                else:
                    return "Non posso gestire questo comando in modalità LITE. Avvia la versione completa."

        agent = SuperAgentLite()
        agent.run()
        while True:
            try:
                user_input = input("\nTu ➜ ")
                if user_input.lower() in ["exit", "quit", "esci"]:
                    print("🔴 Chiusura Super Agent LITE...")
                    break
                response = agent.process(user_input)
                print("SuperAgent ➜", response)
            except KeyboardInterrupt:
                print("\n🔴 Terminato.")
                break
    elif args.headless:
        # ================================
        # SUPER AGENT - VERSIONE HEADLESS
        # Prompt interattivo avanzato
        # ================================
        class SuperAgentHeadless:
            def __init__(self):
                self.name = "Super Agent HEADLESS"
                self.version = "2.0"
                self.status = "idle"

            def info(self):
                return {
                    "name": self.name,
                    "version": self.version,
                    "status": self.status
                }

            def run(self):
                print("🟣 Avvio Super Agent HEADLESS...")
                self.status = "running"
                time.sleep(0.5)
                print("✅ Super Agent HEADLESS avviato (modalità avanzata, senza GUI).")

            def process(self, user_input: str):
                user_input = user_input.lower()
                if "crea app" in user_input:
                    return "App creata con i parametri forniti (simulazione headless)."
                elif "blocca_call" in user_input:
                    return "Funzione blocco chiamate attivata (headless)."
                elif "info" in user_input:
                    return f"{self.name} v{self.version} - Stato: {self.status}"
                elif "help" in user_input:
                    return "Comandi avanzati disponibili: crea app, blocca_call, info, help, exit."
                else:
                    return "Comando non riconosciuto in modalità HEADLESS."

        agent = SuperAgentHeadless()
        agent.run()
        while True:
            try:
                user_input = input("\nTu ➜ ")
                if user_input.lower() in ["exit", "quit", "esci"]:
                    print("🔴 Chiusura Super Agent HEADLESS...")
                    break
                response = agent.process(user_input)
                print("SuperAgent ➜", response)
            except KeyboardInterrupt:
                print("\n🔴 Terminato.")
                break
    else:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    main()
