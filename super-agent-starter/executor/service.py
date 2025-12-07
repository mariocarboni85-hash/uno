from flask import Flask, request, jsonify, g
import requests, os
from utils.jwt_utils import require_jwt

app = Flask(__name__)
EXECUTOR_SANDBOX = 'http://sandbox-runner:5013'

@app.route('/deploy', methods=['POST'])
@require_jwt
def deploy():
    data = request.json or {}
    # logica esistente del deploy
    return jsonify({'status': 'deployed', 'jwt_user': g.jwt_payload.get('sub')})

@app.route('/status')
@require_jwt
def status():
     return jsonify({'status':'ok','service':'executor','jwt_user': g.jwt_payload.get('sub')})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port)
