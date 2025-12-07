from flask import Flask, request, jsonify, g
import os, json, time
from utils.jwt_utils import require_jwt
app = Flask(__name__)
STATE_FILE = 'budget_state.json'
MONTH_LIMIT_EUR = 10.0

if not os.path.exists(STATE_FILE):
    with open(STATE_FILE,'w') as f:
        json.dump({'month': [], 'monthly_total': 0.0}, f)

def load_state():
    with open(STATE_FILE) as f:
        return json.load(f)

def save_state(s):
    with open(STATE_FILE,'w') as f:
        json.dump(s,f)

@app.route('/charge', methods=['POST'])
@require_jwt
def charge():
    data = request.json or {}
    amount = float(data.get('amount',0))
    state = load_state()
    if state['monthly_total'] + amount > MONTH_LIMIT_EUR:
        return jsonify({'status':'blocked','reason':'monthly limit exceeded', 'jwt_user': g.jwt_payload.get('sub')}), 402
    state['month'].append({'t': time.time(), 'amount': amount})
    state['monthly_total'] += amount
    save_state(state)
    return jsonify({'status':'charged','monthly_total': state['monthly_total'], 'jwt_user': g.jwt_payload.get('sub')})

@app.route('/status', methods=['GET'])
@require_jwt
def status():
    return jsonify({**load_state(), 'jwt_user': g.jwt_payload.get('sub')})

@app.route('/reset', methods=['POST'])
@require_jwt
def reset():
    with open(STATE_FILE,'w') as f:
        json.dump({'month': [], 'monthly_total': 0.0}, f)
    return jsonify({'status':'reset', 'jwt_user': g.jwt_payload.get('sub')})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5011))
    app.run(host='0.0.0.0', port=port)
