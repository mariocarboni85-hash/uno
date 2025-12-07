from flask import Flask, request, jsonify, g
import requests, json, time
import numpy as np
from sklearn.linear_model import LogisticRegression
from utils.jwt_utils import require_jwt
from utils.jwt_utils import require_jwt
app = Flask(__name__)
ENV = 'http://env_builder:5005'
EVAL = 'http://evaluator:5007'
EXEC = 'http://executor:5002'

@app.route('/train', methods=['POST'])
@require_jwt
def train():
    ds = requests.post(ENV + '/create_dataset', json={'n': 200}).json()['dataset']
    X = np.array(ds['X']); y = np.array(ds['y'])
    model = LogisticRegression(max_iter=200)
    model.fit(X,y)
    agent_code = f"""
import numpy as np
coef = {model.coef_.tolist()}
intercept = {model.intercept_.tolist()}
def predict(x):
    x = np.array(x)
    val = x.dot(np.array(coef).T) + np.array(intercept)
    return int(val.sum() > 0)

if __name__ == '__main__':
    print(predict([0.1]*5))
"""
    # invia al deploy tramite executor
    dep = requests.post(EXEC + '/deploy', json={'name': 'agent_' + str(int(time.time())), 'code': agent_code})
    return jsonify({'deploy': dep.json(), 'jwt_user': g.jwt_payload.get('sub')})
    
@app.route('/status')
@require_jwt
def status():
     return jsonify({'status':'ok','service':'trainer','jwt_user': g.jwt_payload.get('sub')})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5006))
    app.run(host='0.0.0.0', port=port)
