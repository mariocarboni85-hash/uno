def perform_arduino_action(params):
    """
    Mock azioni Arduino: 'write', 'read'.
    params: {'op': 'write'|'read', ...}
    """
    op = params.get('op')
    if op == 'write':
        return {'result': 'Dato scritto su Arduino (mock)'}
    elif op == 'read':
        return {'result': 'Dato letto da Arduino (mock)'}
    return {'error': 'Operazione non valida'}
"""Arduino helper tool for `arduino-cli` operations.

Functions:
- is_cli_installed()
- run_cli(args_list)
- compile_sketch(sketch_path, fqbn)
- upload_sketch(sketch_path, port, fqbn)
- list_boards()
- install_core(core_name)

Notes:
- Requires `arduino-cli` on PATH. On Windows install from https://arduino.github.io/arduino-cli/installation/
"""
import subprocess
from typing import List, Optional


def _run(args: List[str], timeout: Optional[int] = 120) -> str:
    completed = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    if completed.returncode != 0:
        raise RuntimeError(f"arduino-cli failed: {completed.stderr.strip()}")
    return completed.stdout.strip()


def is_cli_installed() -> bool:
    try:
        _run(["arduino-cli", "version"], timeout=5)
        return True
    except Exception:
        return False


def run_cli(args: List[str]) -> str:
    """Run arbitrary arduino-cli args (list) and return stdout."""
    return _run(["arduino-cli"] + args)


def compile_sketch(sketch_path: str, fqbn: str) -> str:
    """Compile a sketch. Returns compiler output.

    Example: compile_sketch('C:/path/to/Blink', 'arduino:avr:uno')
    """
    return _run(["arduino-cli", "compile", "--fqbn", fqbn, sketch_path])


def upload_sketch(sketch_path: str, port: str, fqbn: str) -> str:
    """Upload a compiled sketch to a board on `port` (e.g. COM3).

    Example: upload_sketch('C:/path/to/Blink', 'COM3', 'arduino:avr:uno')
    """
    return _run(["arduino-cli", "upload", "-p", port, "--fqbn", fqbn, sketch_path])


def list_boards() -> str:
    """Return the output of `arduino-cli board list` (connected boards)."""
    return _run(["arduino-cli", "board", "list"]) 


def install_core(core_name: str) -> str:
    """Install a core (vendor:arch) using `arduino-cli core install`.

    Example: install_core('arduino:avr')
    """
    return _run(["arduino-cli", "core", "install", core_name])
