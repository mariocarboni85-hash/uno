from flask import Flask, request, jsonify
import jwt, datetime, os, json
app = Flask(__name__)

KEY_FILE = 'secrets/api_keys.json'
JWT_SECRET = os.environ.get('JWT_SECRET', 'supersecret_jwt_key')
JWT_ALG = 'HS256'

if os.path.exists(KEY_FILE):
    with open(KEY_FILE) as f:
        API_KEYS = json.load(f)
else:
    API_KEYS = {'admin':'admin-key-DEFAULT'}

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

@app.route('/health')
def health():
    return jsonify({'status':'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5030))
    app.run(host='0.0.0.0', port=port)
