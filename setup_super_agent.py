"""
Script di setup per Super Agent Workspace
- Crea la struttura di cartelle principale
- Verifica/crea requirements.txt
- Opzionale: inizializza file di configurazione e log
"""
import os

folders = [
    'SuperAgentDesktop/gui',
    'SuperAgentDesktop/agents',
    'SuperAgentDesktop/engines',
    'SuperAgentDesktop/sandbox',
    'SuperAgentDesktop/supervisor',
    'SuperAgentDesktop/orchestrator',
    'SuperAgentDesktop/templates/project_templates',
    'SuperAgentDesktop/plugins',
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"Cartella creata/verificata: {folder}")

# Crea requirements.txt se non esiste
req_path = 'requirements.txt'
if not os.path.exists(req_path):
    with open(req_path, 'w') as f:
        f.write('PyQt5\nrequests\n')
    print("Creato requirements.txt di base.")
else:
    print("requirements.txt già presente.")

# Crea file di configurazione base se non esiste
config_path = 'SuperAgentDesktop/config.ini'
if not os.path.exists(config_path):
    with open(config_path, 'w') as f:
        f.write('[DEFAULT]\nlog_level=INFO\n')
    print("Creato config.ini di base.")
else:
    print("config.ini già presente.")

# Crea file di log vuoto se non esiste
log_path = 'SuperAgentDesktop/logs.txt'
if not os.path.exists(log_path):
    with open(log_path, 'w') as f:
        f.write('')
    print("Creato logs.txt vuoto.")
else:
    print("logs.txt già presente.")

print("Setup Super Agent Workspace completato.")
