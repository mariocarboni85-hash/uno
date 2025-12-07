
# Auto-risoluzione dipendenze
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import auto_resolve_dependencies
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'superagent-secret-key'
jwt = JWTManager(app)

from chat_superagent_api import bp as chat_superagent_bp
app.register_blueprint(chat_superagent_bp)
from system_agent_api import bp as system_agent_bp
app.register_blueprint(system_agent_bp)
from graphic_web_api import bp as graphic_web_bp
app.register_blueprint(graphic_web_bp)
from watchdog_agent import bp as watchdog_agent_bp
app.register_blueprint(watchdog_agent_bp)
from distributed_jobs import start_distributed_training, get_job_status, list_jobs
## API job distribuiti

# Avvia un job distribuito
@app.route('/api/distributed_jobs', methods=['POST'])
@jwt_required()
def create_distributed_job():
    data = request.get_json()
    agent_id = data.get('agent_id')
    config = data.get('config', {})
    job_id = start_distributed_training(agent_id, config)
    return jsonify({'job_id': job_id}), 201

# Lista tutti i job distribuiti
@app.route('/api/distributed_jobs', methods=['GET'])
@jwt_required()
def get_distributed_jobs():
    return jsonify(list_jobs())

# Stato di un job specifico
@app.route('/api/distributed_jobs/<job_id>', methods=['GET'])
@jwt_required()
def get_distributed_job_status(job_id):
    job = get_job_status(job_id)
    if job:
        return jsonify(job)
    return jsonify({'msg': 'Job non trovato'}), 404
# Super Agent Dashboard - Backend
# Flask app entrypoint

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'superagent-secret-key'
jwt = JWTManager(app)

# Health check
@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'message': 'Super Agent Dashboard Backend attivo'})

# Login endpoint (mock)
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # Semplice mock: accetta qualsiasi username/password
    if username and password:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify({'msg': 'Credenziali mancanti'}), 401

# API agenti (mock)
@app.route('/api/agents', methods=['GET'])
@jwt_required()
def get_agents():
    agents = [
        {'id': 1, 'name': 'Agent Alpha', 'status': 'active'},
        {'id': 2, 'name': 'Agent Beta', 'status': 'idle'}
    ]
    return jsonify(agents)

# API task (mock)
@app.route('/api/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    tasks = [
        {'id': 101, 'agent_id': 1, 'type': 'training', 'status': 'running'},
        {'id': 102, 'agent_id': 2, 'type': 'simulation', 'status': 'completed'}
    ]
    return jsonify(tasks)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
