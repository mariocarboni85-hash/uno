# Modulo di auto-risoluzione dipendenze per Super Agent
import subprocess
import sys
import importlib
import logging

# Log delle azioni
logging.basicConfig(filename='superagent_autodeps.log', level=logging.INFO)

# Lista dei pacchetti da monitorare
REQUIRED_PACKAGES = [
    'flask',
    'flask_jwt_extended',
    'psutil',
    'requests',
    'numpy',
    'torch'
]

def check_and_install(package):
    try:
        importlib.import_module(package)
        logging.info(f"Pacchetto già presente: {package}")
    except ImportError:
        logging.info(f"Pacchetto mancante: {package}. Installazione...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', package])
        try:
            importlib.import_module(package)
            logging.info(f"Installazione riuscita: {package}")
        except ImportError:
            logging.error(f"Installazione fallita: {package}")

if __name__ == '__main__':
    for pkg in REQUIRED_PACKAGES:
        check_and_install(pkg)
    print("Controllo dipendenze completato. Vedi superagent_autodeps.log per dettagli.")
