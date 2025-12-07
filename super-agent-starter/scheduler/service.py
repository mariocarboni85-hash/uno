from flask import Flask, request, jsonify, g
from apscheduler.schedulers.background import BackgroundScheduler
import requests, os
from utils.jwt_utils import require_jwt
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
@require_jwt
def start():
    if not s.running:
        s.start()
    return jsonify({'status': 'scheduler started'})

@app.route('/stop', methods=['POST'])
@require_jwt
def stop():
    s.shutdown()
    return jsonify({'status': 'stopped'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5004))
    app.run(host='0.0.0.0', port=port)
