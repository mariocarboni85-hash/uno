"""
Modulo di persistenza per chat, task e log (JSON)
"""
import json
import os

DATA_PATH = 'SuperAgentDesktop/data/'
CHAT_FILE = os.path.join(DATA_PATH, 'chat_history.json')
TASK_FILE = os.path.join(DATA_PATH, 'task_history.json')
LOG_FILE = os.path.join(DATA_PATH, 'log_history.json')

os.makedirs(DATA_PATH, exist_ok=True)

def save_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_chat_history(history):
    save_json(history, CHAT_FILE)

def load_chat_history():
    return load_json(CHAT_FILE)

def save_task_history(history):
    save_json(history, TASK_FILE)

def load_task_history():
    return load_json(TASK_FILE)

def save_log_history(history):
    save_json(history, LOG_FILE)

def load_log_history():
    return load_json(LOG_FILE)
