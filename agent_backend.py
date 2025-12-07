import sqlite3
import threading
import time


# Database setup
DB_PATH = 'superagent_ecosystem.db'
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS agents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    status TEXT,
    last_task TEXT,
    last_result TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')

# Tabella utenti
c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')

# Tabella notifiche
c.execute('''CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    message TEXT,
    read INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')

# Tabella plugin
c.execute('''CREATE TABLE IF NOT EXISTS plugins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    description TEXT,
    enabled INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')
def send_notification(user_id, message):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO notifications (user_id, message) VALUES (?, ?)', (user_id, message))
    conn.commit()
    conn.close()

def get_notifications(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, message, read, created_at FROM notifications WHERE user_id=?', (user_id,))
    notes = c.fetchall()
    conn.close()
    return notes

def load_plugins():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT name, description, enabled FROM plugins WHERE enabled=1')
    plugins = c.fetchall()
    conn.close()
    return plugins

def add_plugin(name, description):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('INSERT INTO plugins (name, description) VALUES (?, ?)', (name, description))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
conn.commit()
conn.close()

def register_user(username, password, role='user'):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, password, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, role FROM users WHERE username=? AND password=?', (username, password))
    user = c.fetchone()
    conn.close()
    if user:
        return {'id': user[0], 'role': user[1]}
    return None

class Agent:
    def __init__(self, name):
        self.name = name
        self.status = 'Ready'
        self.last_task = None
        self.last_result = None
        self.save_to_db()
    def save_to_db(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO agents (name, status) VALUES (?, ?)', (self.name, self.status))
        conn.commit()
        conn.close()
    def run_task(self, task):
        self.last_task = task
        self.status = 'Working'
        result = None
        try:
            if task == 'ping':
                time.sleep(1)
                result = f'{self.name}: pong'
            elif task == 'wait':
                time.sleep(2)
                result = f'{self.name}: done waiting'
            else:
                result = f'{self.name}: unknown task'
        except Exception as e:
            result = f'{self.name}: error {e}'
        self.last_result = result
        self.status = 'Ready'
        self.update_db()
        return result
    def update_db(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('UPDATE agents SET status=?, last_task=?, last_result=? WHERE name=?',
                  (self.status, self.last_task, self.last_result, self.name))
        conn.commit()
        conn.close()

# Example: create and run agents
if __name__ == '__main__':
    agent1 = Agent('Alpha')
    agent2 = Agent('Beta')
    print(agent1.run_task('ping'))
    print(agent2.run_task('wait'))
    print(agent1.run_task('unknown'))
