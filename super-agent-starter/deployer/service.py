from flask import Flask, request, jsonify, g
import requests, os
from utils.jwt_utils import require_jwt
 
app = Flask(__name__)
EXEC = 'http://executor:5002'

@app.route('/register', methods=['POST'])
@require_jwt
def register():
    data = request.json or {}
    r = requests.post(EXEC + '/deploy', json=data)
    return jsonify(r.json())
    
@app.route('/status')
@require_jwt
def status():
    return jsonify({'status':'ok','service':'deployer','jwt_user': g.jwt_payload.get('sub')})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5008))
    app.run(host='0.0.0.0', port=port)
