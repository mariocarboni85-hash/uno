from flask import Flask, jsonify, g, request
import psutil, time, os
from utils.jwt_utils import require_jwt
app = Flask(__name__)

LIMITS = {'cpu_percent': 85, 'mem_percent': 85}

@app.route('/metrics')
@require_jwt
def metrics():
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    return jsonify({'cpu': cpu, 'mem': mem, 'limits': LIMITS, 'jwt_user': g.jwt_payload.get('sub')})

@app.route('/check')
@require_jwt
def check():
    m = metrics().get_json()
    if m['cpu'] > LIMITS['cpu_percent'] or m['mem'] > LIMITS['mem_percent']:
        return jsonify({'status':'throttle','metrics': m, 'jwt_user': g.jwt_payload.get('sub')})
    return jsonify({'status':'ok','metrics': m, 'jwt_user': g.jwt_payload.get('sub')})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5012))
    app.run(host='0.0.0.0', port=port)
