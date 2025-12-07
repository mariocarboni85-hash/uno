import json
import time
import jwt
import requests
import logging
from datetime import datetime
import psutil, threading

# Logging avanzato con livello e timestamp
LOG_FILE = 'logs/super_agent.log'
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def advanced_log(msg, level='info'):
    if level == 'error':
        logging.error(msg)
    elif level == 'warning':
        logging.warning(msg)
    else:
        logging.info(msg)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{level.upper()}] {msg}")

def get_auth_token():
    with open('secrets/keys.json') as f:
        keys = json.load(f)
    payload = {
        'sub': keys.get('user', 'superagent'),
        'exp': keys.get('exp', int(time.time()) + 3600)
    }
    token = jwt.encode(payload, keys['jwt_secret'], algorithm='HS256')
    return token

# Configurazioni servizi
SERVICES = {
    'executor': {'url': 'http://executor:5002/deploy', 'sandbox': 'firecracker'},
    'trainer': {'url': 'http://trainer:5006/train', 'sandbox': 'gvisor'},
    'evaluator': {'url': 'http://evaluator:5007/eval', 'sandbox': 'firecracker'}
}

LIMIT_CPU = 80  # %
LIMIT_RAM = 80  # %

# Funzione per testare chiamata JWT a tutti i servizi

# def test_jwt_services():
#     token = get_auth_token()
#     headers = {'Authorization': f'Bearer {token}'}
#     for name, service in SERVICES.items():
#         status_url = service['url'].replace('/deploy','/status').replace('/train','/status').replace('/eval','/status')
#         try:
#             r = requests.get(status_url, headers=headers, timeout=5)
#             advanced_log(f"{name} /status: {r.status_code} {r.text}")
#         except Exception as e:
#             advanced_log(f"{name} /status: errore {e}", 'error')

def monitor_resources():
    while True:
        cpu_raw = psutil.cpu_percent()
        ram_raw = psutil.virtual_memory().percent
        cpu = float(cpu_raw[0]) if isinstance(cpu_raw, list) else float(cpu_raw)
        ram = float(ram_raw[0]) if isinstance(ram_raw, list) else float(ram_raw)
        if cpu > LIMIT_CPU or ram > LIMIT_RAM:
            advanced_log(f"⚠️ Warning: High resource usage - CPU:{cpu}%, RAM:{ram}%", 'warning')
        time.sleep(5)

threading.Thread(target=monitor_resources, daemon=True).start()

if __name__ == "__main__":
    # test_jwt_services()
    pass