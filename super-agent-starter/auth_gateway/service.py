from flask import Flask, request, jsonify, g
from functools import wraps
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from utils.jwt_utils import require_jwt
import os

app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

API_KEYS = { 'admin-key-EXAMPLE': 'admin' }

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get('X-API-KEY') or request.args.get('api_key')
        if not key or key not in API_KEYS:
            return jsonify({'error':'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/status')
@require_api_key
@require_jwt
def status():
    return jsonify({'status':'ok', 'jwt_user': g.jwt_payload.get('sub')})

@app.route('/whoami')
@require_api_key
@require_jwt
def whoami():
    key = request.headers.get('X-API-KEY')
    return jsonify({'role': API_KEYS.get(key), 'jwt_user': g.jwt_payload.get('sub')})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5010))
    app.run(host='0.0.0.0', port=port)
