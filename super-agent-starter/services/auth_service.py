#!/usr/bin/env python3
from flask import Flask, request, jsonify
import jwt, datetime, os, json
from functools import wraps
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

app = Flask(__name__)

# Carica le api key generate (fallback a env var)
KEY_FILE = os.environ.get('API_KEYS_FILE', 'secrets/api_keys.json')
if os.path.exists(KEY_FILE):
    with open(KEY_FILE) as f:
        API_KEYS = json.load(f)
else:
    API_KEYS = {'admin':'admin-key-DEFAULT'}

with open(os.path.join(current, 'secrets', 'jwt_secret')) as f:
    JWT_SECRET = f.read().strip()
JWT_ALG = 'HS256'

# semplice issuance di token JWT dato un api key
@app.route('/token', methods=['POST'])
def token():
    data = request.json or {}
    api_key = data.get('api_key')
    if not api_key or api_key not in API_KEYS.values():
        return jsonify({'error':'invalid_api_key'}), 401
    role = [k for k,v in API_KEYS.items() if v == api_key][0]
    payload = {
        'sub': role,
        'iat': datetime.datetime.utcnow().timestamp(),
        'exp': (datetime.datetime.utcnow() + datetime.timedelta(hours=12)).timestamp()
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)
    return jsonify({'access_token': token})

# decorator per verificare token

@app.route('/introspect', methods=['GET'])
@require_jwt
def introspect():
    from flask import g
    return jsonify({'role': g.jwt_payload.get('sub')})

@app.route('/health')
def health():
    return jsonify({'status':'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5009))
    app.run(host='0.0.0.0', port=port)
