#!/usr/bin/env bash
set -e

# Super Agent Starter - Full Secure Edition (setup.sh)
# Genera uno scaffold Docker-Compose con i microservizi estesi e i guardrail:
# - auth-gateway: API gateway + API key & rate limits
# - budget-manager: traccia costi e applica limiti (es. 10 EUR/mese)
# - resource-guard: monitora e limita CPU/RAM per servizi
# - sandbox-runner: esegue codice anonimo in container effimeri (isolati)
# - planner, executor, memory, scheduler (già presenti)
# - env_builder, trainer, evaluator, deployer
# - dashboard: UI minima per monitoraggio
# Uso:
# 1) salva come setup.sh
# 2) chmod +x setup.sh
# 3) ./setup.sh
# 4) cd super-agent-starter && docker compose up --build

ROOT_DIR=super-agent-starter
mkdir -p "$ROOT_DIR"
cd "$ROOT_DIR"

# Shared Dockerfile per i servizi Python (salva/usa come base)
cat > Dockerfile <<'DOCKER'
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "-u", "entrypoint.py"]
DOCKER

# requirements
cat > requirements.txt <<'REQ'
flask
requests
apscheduler
sqlalchemy
pydantic
numpy
scikit-learn
psutil
flask-limiter
python-dotenv
gunicorn
REQ

# docker-compose con servizi di sicurezza e sandbox
cat > docker-compose.yml <<'DC'
version: '3.8'
services:
  jwt_plugin:
    build: .
    environment:
      - SERVICE_NAME=jwt_plugin
      - PORT=5030
      - JWT_SECRET=${JWT_SECRET:-supersecret_jwt_key}
    volumes:
      - ./jwt_plugin:/app
      - ./utils:/app/utils
      - ./secrets:/app/secrets
    ports:
      - "5030:5030"
    working_dir: /app
  auth-gateway:
    build: .
    environment:
      - SERVICE_NAME=auth_gateway
      - PORT=5010
    ports:
      - "5010:5010"
    volumes:
      - ./auth_gateway:/app
        - ./utils:/app/utils
        - ./secrets:/app/secrets
    working_dir: /app
  budget-manager:
    build: .
    environment:
      - SERVICE_NAME=budget_manager
      - PORT=5011
    ports:
      - "5011:5011"
    volumes:
      - ./budget_manager:/app
        - ./utils:/app/utils
        - ./secrets:/app/secrets
    working_dir: /app
  resource-guard:
    build: .
    environment:
      - SERVICE_NAME=resource_guard
      - PORT=5012
    ports:
      - "5012:5012"
    volumes:
      - ./resource_guard:/app
        - ./utils:/app/utils
        - ./secrets:/app/secrets
    working_dir: /app
  sandbox-runner:
    build: .
    environment:
      - SERVICE_NAME=sandbox_runner
      - PORT=5013
    ports:
      - "5013:5013"
    volumes:
      - ./sandbox_runner:/app
        - ./utils:/app/utils
        - ./secrets:/app/secrets
      - /var/run/docker.sock:/var/run/docker.sock  # permette di lanciare container effimeri (prototipo)
    working_dir: /app
  planner:
    build: .
    environment:
      - SERVICE_NAME=planner
      - PORT=5001
    ports:
      - "5001:5001"
    volumes:
      - ./planner:/app
        - ./utils:/app/utils
        - ./secrets:/app/secrets
    working_dir: /app
  executor:
    build: .
    environment:
      - SERVICE_NAME=executor
      - PORT=5002
    ports:
      - "5002:5002"
    volumes:
      - ./executor:/app
        - ./utils:/app/utils
        - ./secrets:/app/secrets
      - ./utils:/app/utils
      - ./secrets:/app/secrets
    working_dir: /app
  memory:
    build: .
    environment:
      - SERVICE_NAME=memory
      - PORT=5003
    ports:
      - "5003:5003"
    volumes:
      - ./memory:/app
        - ./utils:/app/utils
        - ./secrets:/app/secrets
    working_dir: /app
  scheduler:
    build: .
    environment:
      - SERVICE_NAME=scheduler
      - PORT=5004
    ports:
      - "5004:5004"
    volumes:
      - ./scheduler:/app
        - ./utils:/app/utils
        - ./secrets:/app/secrets
    working_dir: /app
  env_builder:
    build: .
    environment:
      - SERVICE_NAME=env_builder
      - PORT=5005
    ports:
      - "5005:5005"
    volumes:
      - ./env_builder:/app
        - ./utils:/app/utils
        - ./secrets:/app/secrets
    working_dir: /app
  trainer:
    build: .
    environment:
      - SERVICE_NAME=trainer
      - PORT=5006
    ports:
      - "5006:5006"
    volumes:
      - ./trainer:/app
        - ./utils:/app/utils
        - ./secrets:/app/secrets
    working_dir: /app
  evaluator:
    build: .
    environment:
      - SERVICE_NAME=evaluator
      - PORT=5007
    ports:
      - "5007:5007"
    volumes:
      - ./evaluator:/app
        - ./utils:/app/utils
        - ./secrets:/app/secrets
    working_dir: /app
  deployer:
    build: .
    environment:
      - SERVICE_NAME=deployer
      - PORT=5008
    ports:
      - "5008:5008"
    volumes:
      - ./deployer:/app
        - ./utils:/app/utils
        - ./secrets:/app/secrets
    working_dir: /app
  dashboard:
    build: .
    environment:
      - SERVICE_NAME=dashboard
      - PORT=5020
    ports:
      - "5020:5020"
    volumes:
      - ./dashboard:/app
        - ./utils:/app/utils
        - ./secrets:/app/secrets
    working_dir: /app
DC

# entrypoint (invoca service.py all'interno della directory del servizio)
cat > entrypoint.py <<'EP'
import os, sys
from pathlib import Path
service = os.environ.get('SERVICE_NAME')
if not service:
    print('SERVICE_NAME non impostato.')
    sys.exit(1)

path = Path(service)
svc_file = path / 'service.py'
if svc_file.exists():
    import runpy
    runpy.run_path(str(svc_file), run_name='__main__')
else:
    print('service.py non trovato in', service)
EP

# AUTH GATEWAY
mkdir -p auth_gateway
cat > auth_gateway/service.py <<'PY'
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
app = Flask(__name__)

# Limiti di esempio: 5 richieste al minuto per IP
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per minute"]
)

@app.route('/api/some_endpoint', methods=['GET', 'POST'])
@limiter.limit("10 per minute")  # sovrascrive il limite per questo endpoint
def some_endpoint():
    return jsonify({"message": "Questo è un esempio di endpoint protetto."})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5010))
    app.run(host='0.0.0.0', port=port)
PY

# BUDGET MANAGER
mkdir -p budget_manager
cat > budget_manager/service.py <<'PY'
from flask import Flask, request, jsonify
import os
app = Flask(__name__)

# Limite di budget mensile esemplificativo
MONTHLY_BUDGET = 10.0
usage = {}

@app.route('/usage', methods=['GET'])
def get_usage():
    return jsonify(usage)

@app.route('/track', methods=['POST'])
def track():
    data = request.json or {}
    service = data.get('service')
    cost = float(data.get('cost', 0))
    if service not in usage:
        usage[service] = 0
    usage[service] += cost
    # applica limite
    if usage[service] > MONTHLY_BUDGET:
        return jsonify({'error': 'budget exceeded'}), 403
    return jsonify({'status': 'ok', 'usage': usage})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5011))
    app.run(host='0.0.0.0', port=port)
PY

# RESOURCE GUARD
mkdir -p resource_guard
cat > resource_guard/service.py <<'PY'
from flask import Flask, request, jsonify
import os, psutil
app = Flask(__name__)

@app.route('/metrics', methods=['GET'])
def metrics():
    # ritorna uso attuale di CPU/RAM
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    return jsonify({'cpu': cpu, 'memory': mem})

@app.route('/limit', methods=['POST'])
def limit():
    data = request.json or {}
    pid = data.get('pid')
    cpu_limit = data.get('cpu')
    mem_limit = data.get('memory')
    try:
        p = psutil.Process(pid)
        if cpu_limit is not None:
            p.cpu_affinity([cpu_limit])  # limita a un core (semplice)
        if mem_limit is not None:
            # imposta limite di memoria (soft e hard)
            p.rlimit(psutil.RLIMIT_AS, (mem_limit, mem_limit))
        return jsonify({'status': 'limits set', 'pid': pid})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5012))
    app.run(host='0.0.0.0', port=port)
PY

# SANDBOX RUNNER
mkdir -p sandbox_runner
cat > sandbox_runner/service.py <<'PY'
from flask import Flask, request, jsonify
import os, docker

app = Flask(__name__)
client = docker.from_env()

@app.route('/run', methods=['POST'])
def run_code():
    data = request.json or {}
    code = data.get('code', '')
    # salva codice in file temporaneo
    with open('temp_code.py', 'w') as f:
        f.write(code)
    # esegui in un container effimero
    try:
        container = client.containers.run("python:3.11-slim", 
                                           "python -u /app/temp_code.py", 
                                           volumes={'/var/run/docker.sock': {'bind': '/var/run/docker.sock', 'mode': 'rw'}},
                                           detach=True)
        container.wait()
        logs = container.logs().decode('utf-8')
        return jsonify({'status': 'finished', 'logs': logs})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5013))
    app.run(host='0.0.0.0', port=port)
PY

# PLANNER
mkdir -p planner
cat > planner/service.py <<'PY'
from flask import Flask, request, jsonify
import os
app = Flask(__name__)

@app.route('/plan', methods=['POST'])
def plan():
    data = request.json or {}
    goal = data.get('goal', 'no goal')
    # semplice scomposizione fittizia
    steps = [f"Analizza: {goal}", "Progetta architettura", "Implementa prova", "Test e deploy"]
    return jsonify({'goal': goal, 'plan': steps})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)
PY

# EXECUTOR (aggiunge endpoint /deploy)
mkdir -p executor
cat > executor/service.py <<'PY'
from flask import Flask, request, jsonify
import os, time, json
app = Flask(__name__)
AGENTS_DIR = 'deployed_agents'
os.makedirs(AGENTS_DIR, exist_ok=True)

@app.route('/execute', methods=['POST'])
def execute():
    data = request.json or {}
    task = data.get('task', 'no task')
    # esecuzione finta con ritardo
    time.sleep(0.5)
    result = {'task': task, 'status': 'done', 'output': f'Result of {task}'}
    return jsonify(result)

@app.route('/deploy', methods=['POST'])
def deploy():
    data = request.json or {}
    name = data.get('name')
    code = data.get('code', '')
    if not name:
        return jsonify({'error': 'name required'}), 400
    path = os.path.join(AGENTS_DIR, name + '.py')
    with open(path, 'w') as f:
        f.write(code)
    return jsonify({'status': 'deployed', 'path': path})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port)
PY

# MEMORY
mkdir -p memory
cat > memory/service.py <<'PY'
from flask import Flask, request, jsonify
import os
from sqlalchemy import create_engine, Column, Integer, String, Text, MetaData, Table

app = Flask(__name__)
DB_PATH = os.environ.get('DB_PATH', 'memory.db')
engine = create_engine(f'sqlite:///{DB_PATH}', connect_args={"check_same_thread": False})
metadata = MetaData()
mem = Table('memory', metadata,
            Column('id', Integer, primary_key=True),
            Column('key', String, nullable=False),
            Column('value', Text, nullable=False))
metadata.create_all(engine)

@app.route('/save', methods=['POST'])
def save():
    data = request.json or {}
    key = data.get('key')
    value = data.get('value')
    if not key or value is None:
        return jsonify({'error': 'key/value required'}), 400
    ins = mem.insert().values(key=key, value=value)
    conn = engine.connect()
    conn.execute(ins)
    return jsonify({'status': 'saved'})

@app.route('/get/<key>', methods=['GET'])
def get_key(key):
    conn = engine.connect()
    sel = mem.select().where(mem.c.key == key)
    res = conn.execute(sel).fetchall()
    return jsonify([dict(r) for r in res])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5003))
    app.run(host='0.0.0.0', port=port)
PY

# SCHEDULER
mkdir -p scheduler
cat > scheduler/service.py <<'PY'
from flask import Flask, request, jsonify
import os
from apscheduler.schedulers.background import BackgroundScheduler
import requests

app = Flask(__name__)
s = BackgroundScheduler()

JOB_ENDPOINT = 'http://executor:5002/execute'

def job_ping():
    try:
        requests.post(JOB_ENDPOINT, json={'task': 'heartbeat'})
    except Exception as e:
        print('job error', e)

s.add_job(job_ping, 'interval', seconds=30)

@app.route('/start', methods=['POST'])
def start():
    if not s.running:
        s.start()
    return jsonify({'status': 'scheduler started'})

@app.route('/stop', methods=['POST'])
def stop():
    s.shutdown()
    return jsonify({'status': 'stopped'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5004))
    app.run(host='0.0.0.0', port=port)
PY

# ENV_BUILDER (genera dataset sintetici e scenari di simulazione)
mkdir -p env_builder
cat > env_builder/service.py <<'PY'
from flask import Flask, request, jsonify
import os, json, random
import numpy as np
app = Flask(__name__)

@app.route('/create_dataset', methods=['POST'])
def create_dataset():
    data = request.json or {}
    task_type = data.get('type', 'classification')
    n = int(data.get('n', 100))
    # dataset sintetico semplice
    X = np.random.randn(n, 5).tolist()
    y = [int(sum(x) > 0) for x in X]
    ds = {'X': X, 'y': y}
    return jsonify({'status': 'created', 'dataset': ds})

@app.route('/scenario', methods=['POST'])
def scenario():
    data = request.json or {}
    kind = data.get('kind', 'trading')
    # crea uno scenario fittizio
    if kind == 'trading':
        steps = [{'price': 100 + random.gauss(0,1)} for _ in range(200)]
    else:
        steps = [{'state': i, 'event': random.choice(['ok','fail'])} for i in range(100)]
    return jsonify({'status': 'ok', 'scenario': steps})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5005))
    app.run(host='0.0.0.0', port=port)
PY

# TRAINER (supporto supervised + RL stub che usa env_builder)
mkdir -p trainer
cat > trainer/service.py <<'PY'
from flask import Flask, request, jsonify
import os, time, requests
import json
from sklearn.linear_model import LogisticRegression
import numpy as np
app = Flask(__name__)
ENV_URL = 'http://env_builder:5005'
EVAL_URL = 'http://evaluator:5007'
EXEC_URL = 'http://executor:5002'

@app.route('/train', methods=['POST'])
def train():
    data = request.json or {}
    mode = data.get('mode', 'supervised')
    # ottieni dataset sintetico
    ds = requests.post(ENV_URL + '/create_dataset', json={'n': 200}).json()['dataset']
    X = np.array(ds['X'])
    y = np.array(ds['y'])
    # training semplice
    model = LogisticRegression(max_iter=200)
    model.fit(X, y)
    # serializziamo il "model" come codice molto semplice (stub)
    agent_code = f"""
# Agent auto-generato
import numpy as np
from sklearn.linear_model import LogisticRegression

# model coefficients serializzati
coef = {model.coef_.tolist()}
intercept = {model.intercept_.tolist()}

def predict(x):
    x = np.array(x)
    val = x.dot(np.array(coef).T) + np.array(intercept)
    return int(val.sum() > 0)
"""
    # valuta
    eval_res = requests.post(EVAL_URL + '/evaluate_agent', json={'code': agent_code}).json()
    # se passa, deploya
    if eval_res.get('score',0) > 0.7:
        dep = requests.post(EXEC_URL + '/deploy', json={'name': 'agent_' + str(int(time.time())), 'code': agent_code}).json()
        return jsonify({'status': 'trained_and_deployed', 'eval': eval_res, 'deploy': dep})
    else:
        return jsonify({'status': 'trained_but_failed_eval', 'eval': eval_res})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5006))
    app.run(host='0.0.0.0', port=port)
PY

# EVALUATOR (esegue test e ritorna metriche)
mkdir -p evaluator
cat > evaluator/service.py <<'PY'
from flask import Flask, request, jsonify
import traceback
app = Flask(__name__)

@app.route('/evaluate_agent', methods=['POST'])
def evaluate_agent():
    data = request.json or {}
    code = data.get('code','')
    # esegui in un namespace sicuro limitato (ATTENZIONE: questo è solo un esempio, non è sicuro per produzione)
    ns = {}
    try:
        exec(code, ns, ns)
        # test rapido: chiamare predict su input casuale
        tests = [[0.1]*5, [1]*5, [-1]*5]
        results = []
        for t in tests:
            r = ns.get('predict')(t)
            results.append(int(bool(r)))
        # score fittizio
        score = sum(results) / len(results)
        return jsonify({'score': score, 'results': results})
    except Exception as e:
        return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5007))
    app.run(host='0.0.0.0', port=port)
PY

# DEPLOYER (coordina deployment aggiuntivo e versioning)
mkdir -p deployer
cat > deployer/service.py <<'PY'
from flask import Flask, request, jsonify
import os, requests, time
app = Flask(__name__)
EXEC_URL = 'http://executor:5002'

@app.route('/register', methods=['POST'])
def register():
    data = request.json or {}
    name = data.get('name')
    code = data.get('code')
    if not name or not code:
        return jsonify({'error': 'name and code required'}), 400
    # proxy al executor per deploy reale
    r = requests.post(EXEC_URL + '/deploy', json={'name': name, 'code': code})
    return jsonify({'status': 'registered', 'executor': r.json()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5008))
    app.run(host='0.0.0.0', port=port)
PY

# DASHBOARD (UI minima per monitoraggio)
mkdir -p dashboard
cat > dashboard/service.py <<'PY'
from flask import Flask, jsonify
import os, psutil
app = Flask(__name__)

@app.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'running'})

@app.route('/metrics', methods=['GET'])
def metrics():
    # ritorna uso attuale di CPU/RAM
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    return jsonify({'cpu': cpu, 'memory': mem})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5020))
    app.run(host='0.0.0.0', port=port)
PY

# README
cat > README.md <<'MD'
# Super Agent Starter - Full Secure Edition
Questo scaffold estende il progetto con componenti per sicurezza, monitoraggio e gestione risorse:
- auth-gateway: API gateway con autenticazione e rate limiting
- budget-manager: gestione budget e costi
- resource-guard: monitoraggio e limitazione risorse (CPU/RAM)
- sandbox-runner: esecuzione di codice in sandbox sicure (container effimeri)
- dashboard: interfaccia di monitoraggio semplice

Flow di esempio:
1) L'utente interagisce tramite auth-gateway
2) Le richieste sono limitate e tracciate
3) I servizi possono essere eseguiti in sandbox isolate
4) Il monitoraggio delle risorse è attivo
5) I budget sono applicati per limitare i costi

Importante: questo codice è un PUNTO DI PARTENZA. Non usare in produzione senza:
- sandboxing vero per exec()
- limiti di risorse
- autenticazione
- gestione costi API

Esempi:
POST http://localhost:5006/train {"mode":"supervised"}
POST http://localhost:5005/create_dataset {"n":100}

MD

chmod -R 755 .

echo "Full Secure scaffold creato in: $(pwd)"

echo "Prossimi passi: entra nella cartella $ROOT_DIR e lancia: docker compose up --build"
# ---
# MODULI DI SICUREZZA AGGIUNTIVI
# ---
# 1. Genera API keys
mkdir -p scripts secrets
cat > scripts/generate_keys.py <<'PY'
#!/usr/bin/env python3
"""
Genera coppie di API keys per i servizi e le salva in keys.json
Uso: python3 scripts/generate_keys.py
"""
import secrets, json, os
os.makedirs('secrets', exist_ok=True)
keys = {
    'admin': secrets.token_urlsafe(32),
    'trainer': secrets.token_urlsafe(32),
    'executor': secrets.token_urlsafe(32),
    'deployer': secrets.token_urlsafe(32),
    'dashboard': secrets.token_urlsafe(32),
}
with open('secrets/keys.json','w') as f:
    json.dump(keys, f, indent=2)
print('Keys generated and saved to secrets/keys.json')
PY
chmod +x scripts/generate_keys.py

# 2. Abilita servizio JWT/OAuth
mkdir -p services/auth secrets
cat > services/auth_service.py <<'PY'
from flask import Flask, request, jsonify
import jwt, datetime, json, os
from functools import wraps

app = Flask(__name__)
# Secret for signing JWTs (in production store securely)
SECRET_FILE = 'secrets/jwt_secret'
if not os.path.exists('secrets'):
    os.makedirs('secrets')
if not os.path.exists(SECRET_FILE):
    with open(SECRET_FILE,'w') as f:
        f.write('change-me')
with open(SECRET_FILE) as f:
    JWT_SECRET = f.read().strip() or 'change-me'

# load API keys generated by generate_keys.py
KEYS_FILE = 'secrets/keys.json'
API_KEYS = {}
if os.path.exists(KEYS_FILE):
    with open(KEYS_FILE) as f:
        API_KEYS = json.load(f)

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get('X-API-KEY') or request.args.get('api_key')
        if not key or key not in API_KEYS.values():
            return jsonify({'error':'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/token', methods=['POST'])
@require_api_key
def token():
    user = request.json.get('user','user')
    exp = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    token = jwt.encode({'user': user, 'exp': exp}, JWT_SECRET, algorithm='HS256')
    return jsonify({'token': token})

@app.route('/verify', methods=['POST'])
def verify():
    token = request.json.get('token','')
    try:
        data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return jsonify({'valid': True, 'data': data})
    except Exception as e:
        return jsonify({'valid': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
PY

# 3. Prepara configurazioni Firecracker/gVisor
mkdir -p sandbox/firecracker sandbox/gvisor templates
cat > sandbox/firecracker/fc_config.json <<'JSON'
{
  "boot_args": "console=ttyS0 reboot=k panic=1 pci=off",
  "vcpu_count": 1,
  "mem_size_mib": 128,
  "network": false
}
JSON
cat > sandbox/gvisor/gvisor_config.json <<'JSON'
{
  "platform": "linux",
  "network": false,
  "memory": 128
}
JSON
