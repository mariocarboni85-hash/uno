import jwt
import os
from flask import request, jsonify, g
from functools import wraps

SECRET_FILE = 'secrets/jwt_secret'
if not os.path.exists(SECRET_FILE):
    os.makedirs('secrets', exist_ok=True)
    with open(SECRET_FILE, 'w') as f:
        f.write('change-me')  # placeholder

with open(SECRET_FILE) as f:
    JWT_SECRET = f.read().strip()

def require_jwt(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid Authorization header'}), 401
        token = token.split(' ')[1]
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            g.jwt_payload = payload
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except Exception as e:
            return jsonify({'error': str(e)}), 401
        return f(*args, **kwargs)
    return decorated
