import os
import sys
import psutil
import platform
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

bp = Blueprint('system_agent', __name__)

# Scansione applicazioni installate (Windows, Mac, Linux)
@bp.route('/api/scan_apps', methods=['GET'])
@jwt_required()
def scan_apps():
    system = platform.system()
    apps = []
    if system == 'Windows':
        # Cerca eseguibili nelle cartelle Program Files
        for root in [os.environ.get('ProgramFiles'), os.environ.get('ProgramFiles(x86)')]:
            if root and os.path.exists(root):
                for dirpath, dirnames, filenames in os.walk(root):
                    for f in filenames:
                        if f.lower().endswith('.exe'):
                            apps.append(os.path.join(dirpath, f))
    elif system == 'Darwin':
        # Mac: cerca .app in /Applications
        for dirpath, dirnames, filenames in os.walk('/Applications'):
            for d in dirnames:
                if d.endswith('.app'):
                    apps.append(os.path.join(dirpath, d))
    elif system == 'Linux':
        # Linux: cerca binari in /usr/bin
        for f in os.listdir('/usr/bin'):
            apps.append(os.path.join('/usr/bin', f))
    return jsonify({'system': system, 'apps': apps})

# Avvia applicazione
@bp.route('/api/start_app', methods=['POST'])
@jwt_required()
def start_app():
    data = request.get_json()
    path = data.get('path')
    try:
        if platform.system() == 'Windows':
            os.startfile(path)
        else:
            import subprocess
            subprocess.Popen([path])
        return jsonify({'status': 'started', 'path': path})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Chiudi applicazione (per PID)
@bp.route('/api/kill_app', methods=['POST'])
@jwt_required()
def kill_app():
    data = request.get_json()
    pid = data.get('pid')
    try:
        p = psutil.Process(pid)
        p.terminate()
        return jsonify({'status': 'terminated', 'pid': pid})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Lista processi attivi
@bp.route('/api/list_processes', methods=['GET'])
@jwt_required()
def list_processes():
    procs = []
    for p in psutil.process_iter(['pid', 'name', 'exe']):
        procs.append(p.info)
    return jsonify({'processes': procs})

# Log azioni e apprendimento continuo (mock)
@bp.route('/api/log_action', methods=['POST'])
@jwt_required()
def log_action():
    data = request.get_json()
    action = data.get('action')
    result = data.get('result')
    # Qui si può salvare su file/database
    print(f"LOG: {action} -> {result}")
    return jsonify({'status': 'logged'})

# Sicurezza: autorizzazione accesso (mock)
@bp.route('/api/authorize', methods=['POST'])
@jwt_required()
def authorize():
    data = request.get_json()
    app = data.get('app')
    allow = data.get('allow', True)
    # Qui si può gestire whitelist/blacklist
    print(f"Autorizzazione: {app} -> {allow}")
    return jsonify({'status': 'updated', 'app': app, 'allow': allow})

    # Endpoint di login per ottenere un token JWT

    # Gestione utenti demo
    USERS = {"admin": "adminpass", "user": "userpass"}
    from flask_jwt_extended import create_access_token, get_jwt_identity

    @bp.route('/api/login', methods=['POST'])
    def login():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if username in USERS and USERS[username] == password:
            access_token = create_access_token(identity=username)
            log_action_data = {"action": "login", "result": f"user {username} login"}
            print(f"LOG: {log_action_data}")
            return jsonify(access_token=access_token), 200
        return jsonify({'msg': 'Credenziali errate'}), 401

    # Endpoint demo per vedere l'identità utente autenticato
    @bp.route('/api/me', methods=['GET'])
    @jwt_required()
    def me():
        user = get_jwt_identity()
        return jsonify({"user": user})

    # Avvio diretto dell'app Flask
    if __name__ == "__main__":
        from flask import Flask
        app = Flask(__name__)
        app.config["JWT_SECRET_KEY"] = "super-secret-key"  # Sostituisci con una chiave sicura
        from flask_jwt_extended import JWTManager
        jwt = JWTManager(app)
        app.register_blueprint(bp)
        app.run(host="0.0.0.0", port=5000, debug=True)