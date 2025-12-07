import sys, os, importlib.util
from flask import Flask, jsonify, request
current = os.path.abspath(os.path.dirname(__file__))
while not os.path.exists(os.path.join(current, 'utils', 'jwt_utils.py')):
    parent = os.path.dirname(current)
    if parent == current:
        raise FileNotFoundError('utils/jwt_utils.py not found in any parent directory')
    current = parent
jwt_utils_path = os.path.join(current, 'utils', 'jwt_utils.py')
spec = importlib.util.spec_from_file_location('jwt_utils', jwt_utils_path)
jwt_utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(jwt_utils)
require_jwt = jwt_utils.require_jwt

app = Flask(__name__)

@app.route('/status', methods=['GET'])
@require_jwt
def status():
    return jsonify({'service': 'evaluator', 'status': 'ok'})

if __name__ == '__main__':
    app.run(port=5003)
