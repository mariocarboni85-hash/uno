from flask import Flask, request, jsonify, g
import requests, json
from utils.jwt_utils import require_jwt
app = Flask(__name__)
# ora l'evaluator delega l'esecuzione a sandbox-runner per test più sicuri
SANDBOX = 'http://sandbox-runner:5013'

@app.route('/evaluate_agent', methods=['POST'])
@require_jwt
def evaluate_agent():
    data = request.json or {}
    code = data.get('code','')
    if not code:
        return jsonify({'error':'no code'}), 400
    r = requests.post(SANDBOX + '/run_code', json={'code': code, 'timeout': 5})
    if r.status_code != 200:
        return jsonify({'error':'sandbox error','detail': r.text}), 500
    res = r.json()
    # very naive scoring: if returncode==0 -> score 1.0
    score = 1.0 if res.get('returncode',1) == 0 else 0.0
    return jsonify({'score': score, 'sandbox': res, 'jwt_user': g.jwt_payload.get('sub')})

@app.route('/status')
@require_jwt
def status():
    return jsonify({'status':'ok','service':'evaluator','jwt_user': g.jwt_payload.get('sub')})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5007))
    app.run(host='0.0.0.0', port=port)
