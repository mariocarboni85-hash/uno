"""
Sandbox sicura: esecuzione codice Python isolato tramite subprocess
"""
import subprocess
import tempfile
import os
import sys

def run_code_in_sandbox(code, timeout=5):
    """Esegue codice Python in modo isolato, con timeout e output controllato."""
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.py') as tmp:
        tmp.write(code)
        tmp_path = tmp.name
    try:
        result = subprocess.run(
            [sys.executable, tmp_path],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False
        )
        output = result.stdout
        error = result.stderr
    except subprocess.TimeoutExpired:
        output = ''
        error = 'Timeout scaduto.'
    finally:
        os.remove(tmp_path)
    return output, error
