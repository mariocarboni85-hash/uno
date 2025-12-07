from flask import Flask, request, jsonify, g
import numpy as np, random
from utils.jwt_utils import require_jwt
app = Flask(__name__)

@app.route('/create_dataset', methods=['POST'])
@require_jwt
def create_dataset():
    data = request.json or {}
    n = int(data.get('n', 100))
    X = np.random.randn(n, 5).tolist()
    y = [int(sum(x) > 0) for x in X]
    return jsonify({'dataset': {'X': X, 'y': y}})

@app.route('/status')
@require_jwt
def status():
     return jsonify({'status':'ok','service':'env_builder','jwt_user': g.jwt_payload.get('sub')})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5005))
    app.run(host='0.0.0.0', port=port)
