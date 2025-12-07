
import sys, os, importlib.util
current = os.path.abspath(os.path.dirname(__file__))
while not os.path.exists(os.path.join(current, 'utils', 'jwt_utils.py')):
    parent = os.path.dirname(current)
    if parent == current:
        raise FileNotFoundError('utils/jwt_utils.py not found in any parent directory')
    current = parent
jwt_utils_path = os.path.join(current, 'utils', 'jwt_utils.py')
spec = importlib.util.spec_from_file_location('jwt_utils', jwt_utils_path)
jwt_utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(jwt_utils)
require_jwt = jwt_utils.require_jwt
from flask import Flask, request, jsonify, render_template_string, g
import requests, json, os
import json

app = Flask(__name__)
@app.route('/notifications/config', methods=['GET', 'POST'])
def notifications_config():
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../config/notifications.json'))
    if request.method == 'POST':
        data = request.json
        with open(config_path, 'w') as f:
            json.dump(data, f, indent=2)
        return jsonify({'status': 'updated'})
    else:
        if os.path.exists(config_path):
            with open(config_path) as f:
                config = json.load(f)
        else:
            config = {}
        return jsonify(config)

# Lista dei servizi da monitorare
SERVICES = [
    {'name': 'executor', 'url': 'http://localhost:5001/status'},
    {'name': 'trainer', 'url': 'http://localhost:5002/status'},
    {'name': 'evaluator', 'url': 'http://localhost:5003/status'},
    {'name': 'deployer', 'url': 'http://localhost:5004/status'},
    {'name': 'env_builder', 'url': 'http://localhost:5005/status'},
]

@app.route('/dashboard')
@require_jwt
def dashboard():
    results = []
    for s in SERVICES:
        try:
            r = requests.get(s['url'], headers={'Authorization': request.headers.get('Authorization')}, timeout=2)
            data = r.json()
            results.append({
                'service': s['name'],
                'status': data.get('status','offline'),
                'user': data.get('jwt_user','-'),
                'error': None
            })
        except Exception as e:
            results.append({'service': s['name'], 'status': 'offline', 'user': '-', 'error': str(e)})

    template = """
    <html><head><title>Super Agent Dashboard</title></head><body>
    <h1>Super Agent Dashboard</h1>
    <p>Utente: {{ user }}</p>
    <table border=1><tr><th>Servizio</th><th>Status</th><th>Utente token</th><th>Error</th></tr>
    {% for r in results %}
    <tr>
      <td>{{ r.service }}</td>
      <td>{{ r.status }}</td>
      <td>{{ r.user if r.user else '-' }}</td>
      <td>{{ r.error if r.error else '-' }}</td>
    </tr>
    {% endfor %}
    </table>
    </body></html>
    """
    return render_template_string(template, results=results, user=g.jwt_payload.get('sub'))

@app.route('/status')
@require_jwt
def status():
    REMOTE_DEVICES = [
            {"name": "Device1", "url": "http://192.168.1.20:5500", "api_key": "MASTER_SLAVE_KEY"}
    ]

    @app.route('/dashboard/remote')
    @require_jwt
    def dashboard_remote():
            remote_results = []
            for d in REMOTE_DEVICES:
                    try:
                            headers = {"Authorization": f"Bearer {d['api_key']}"}
                            r = requests.get(f"{d['url']}/task/status", headers=headers, timeout=3)
                            data = r.json()
                            remote_results.append({
                                    'device': d['name'],
                                    'url': d['url'],
                                    'tasks': data.get('tasks',[]),
                                    'error': None
                            })
                    except Exception as e:
                            remote_results.append({'device': d['name'], 'url': d['url'], 'tasks': [], 'error': str(e)})

            template = """
            <html><head><title>Super Agent Remote Devices</title></head><body>
            <h1>Stato dispositivi remoti</h1>
            <table border=1><tr><th>Device</th><th>URL</th><th>Tasks</th><th>Error</th></tr>
            {% for r in remote_results %}
            <tr>
                <td>{{ r.device }}</td>
                <td>{{ r.url }}</td>
                <td>
                    {% if r.tasks %}
                        <ul>
                        {% for t in r.tasks %}
                            <li>{{ t }}</li>
                        {% endfor %}
                        </ul>
                    {% else %}-{% endif %}
                </td>
                <td>{{ r.error if r.error else '-' }}</td>
            </tr>
            {% endfor %}
            </table>
            <p><a href='/dashboard'>Torna alla dashboard</a></p>
            </body></html>
            """
            return render_template_string(template, remote_results=remote_results)
    return jsonify({'status':'ok','service':'dashboard','jwt_user': g.jwt_payload.get('sub')})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5020))
    app.run(host='0.0.0.0', port=port)
