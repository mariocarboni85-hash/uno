from flask import Flask, request, jsonify, g
import os, subprocess, tempfile, uuid, shutil
from utils.jwt_utils import require_jwt
app = Flask(__name__)

IMAGE = os.environ.get('SANDBOX_IMAGE','python:3.11-slim')

@app.route('/run_code', methods=['POST'])
@require_jwt
def run_code():
    data = request.json or {}
    code = data.get('code','')
    timeout = int(data.get('timeout', 10))
    if not code:
        return jsonify({'error':'no code'}), 400
    tmpdir = tempfile.mkdtemp()
    fname = os.path.join(tmpdir,'agent.py')
    with open(fname,'w') as f:
        f.write(code)
    cid = 'sandbox_' + uuid.uuid4().hex[:8]
    try:
        cmd = [
            'docker','run','--rm','--name',cid,
            '-v', f"{tmpdir}:/work:ro",
            IMAGE,
            'python','-u','/work/agent.py'
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        out = proc.stdout
        err = proc.stderr
        code_ret = proc.returncode
        return jsonify({'stdout': out, 'stderr': err, 'returncode': code_ret, 'jwt_user': g.jwt_payload.get('sub')})
    except subprocess.TimeoutExpired:
        return jsonify({'error':'timeout', 'jwt_user': g.jwt_payload.get('sub')}), 504
    except Exception as e:
        return jsonify({'error': str(e), 'jwt_user': g.jwt_payload.get('sub')}), 500
    finally:
        try:
            shutil.rmtree(tmpdir)
        except:
            pass

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5013))
    app.run(host='0.0.0.0', port=port)
