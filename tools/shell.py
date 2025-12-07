def schedule_task(params):
    """
    Schedula un task (mock).
    params: {'cmd': ..., 'time': ...}
    """
    cmd = params.get('cmd')
    time = params.get('time')
    print(f"[SCHEDULING] Comando: {cmd} | Orario: {time}")
    return {'result': 'ok'}
def send_notification(params):
    """
    Invia una notifica/email (mock).
    params: {'to': ..., 'subject': ..., 'body': ...}
    """
    to = params.get('to')
    subject = params.get('subject')
    body = params.get('body')
    print(f"[NOTIFICA] To: {to} | Subject: {subject} | Body: {body}")
    return {'result': 'ok'}
def run_tests(params):
    """
    Esegue test automatici.
    params: {'type': 'python'|'node', 'path': ...}
    """
    import subprocess
    t = params.get('type')
    path = params.get('path')
    try:
        if t == 'python':
            out = subprocess.check_output(f'pytest {path}', shell=True, encoding='utf-8', timeout=60)
        elif t == 'node':
            out = subprocess.check_output(f'npm test --prefix {path}', shell=True, encoding='utf-8', timeout=60)
        else:
            return {'error': 'Tipo non supportato'}
        return {'output': out}
    except Exception as e:
        return {'error': str(e)}
def update_dependencies(params):
    """
    Aggiorna dipendenze pip o npm.
    params: {'type': 'pip'|'npm'}
    """
    import subprocess
    t = params.get('type')
    try:
        if t == 'pip':
            out = subprocess.check_output('pip install --upgrade pip', shell=True, encoding='utf-8', timeout=60)
        elif t == 'npm':
            out = subprocess.check_output('npm update', shell=True, encoding='utf-8', timeout=60)
        else:
            return {'error': 'Tipo non supportato'}
        return {'output': out}
    except Exception as e:
        return {'error': str(e)}
def install_program(params):
    """
    Installa un programma o pacchetto.
    params: {'type': 'pip'|'npm'|'exe', 'name': ..., 'args': ...}
    """
    import subprocess
    t = params.get('type')
    name = params.get('name')
    args = params.get('args', '')
    try:
        if t == 'pip':
            out = subprocess.check_output(f'pip install {name} {args}', shell=True, encoding='utf-8', timeout=60)
        elif t == 'npm':
            out = subprocess.check_output(f'npm install {name} {args}', shell=True, encoding='utf-8', timeout=60)
        elif t == 'exe':
            out = subprocess.check_output(f'{name} {args}', shell=True, encoding='utf-8', timeout=60)
        else:
            return {'error': 'Tipo non supportato'}
        return {'output': out}
    except Exception as e:
        return {'error': str(e)}
def perform_shell_action(params):
    """
    Esegue comandi shell.
    params: {'op': 'run', 'cmd': ...}
    """
    import subprocess
    op = params.get('op')
    cmd = params.get('cmd')
    if op == 'run' and cmd:
        try:
            out = subprocess.check_output(cmd, shell=True, encoding='utf-8', timeout=10)
            return {'output': out}
        except Exception as e:
            return {'error': str(e)}
    return {'error': 'Operazione non valida'}
"""
Advanced Shell Tool - Enhanced command execution with monitoring and safety
"""
import subprocess
import shlex
import os
import platform
import time
from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path


class ShellExecutor:
    """Advanced shell command executor with safety features."""
    
    def __init__(self):
        self.history = []
        self.dangerous_commands = [
            'rm -rf /', 'del /f /s /q', 'format', 'mkfs',
            'dd if=', ':(){ :|:& };:', 'sudo rm -rf'
        ]
        self.system = platform.system()
        self.shell = 'powershell' if self.system == 'Windows' else 'bash'
    
    def is_safe(self, cmd: str) -> Tuple[bool, str]:
        """Check if command is safe to execute."""
        cmd_lower = cmd.lower()
        
        for dangerous in self.dangerous_commands:
            if dangerous.lower() in cmd_lower:
                return False, f"Dangerous command detected: {dangerous}"
        
        # Check for suspicious patterns
        if '>' in cmd and '/dev/' in cmd:
            return False, "Suspicious redirection to system device"
        
        return True, "Command appears safe"
    
    def run(self, cmd: str, timeout: Optional[int] = 30, 
            cwd: Optional[str] = None, env: Optional[Dict] = None,
            check_safety: bool = True) -> Dict[str, Any]:
        """
        Run shell command with advanced features.
        
        Args:
            cmd: Command to execute
            timeout: Timeout in seconds
            cwd: Working directory
            env: Environment variables
            check_safety: Whether to check command safety
            
        Returns:
            Dict with stdout, stderr, returncode, duration, etc.
        """
        # Safety check
        if check_safety:
            is_safe, reason = self.is_safe(cmd)
            if not is_safe:
                return {
                    'success': False,
                    'error': reason,
                    'stdout': '',
                    'stderr': reason,
                    'returncode': -1
                }
        
        start_time = time.time()
        
        try:
            # Prepare environment
            exec_env = os.environ.copy()
            if env:
                exec_env.update(env)
            
            # Execute command
            process = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd,
                env=exec_env
            )
            
            duration = time.time() - start_time
            
            result = {
                'success': process.returncode == 0,
                'stdout': process.stdout,
                'stderr': process.stderr,
                'returncode': process.returncode,
                'duration': round(duration, 3),
                'command': cmd,
                'cwd': cwd or os.getcwd()
            }
            
            # Add to history
            self.history.append({
                'command': cmd,
                'timestamp': time.time(),
                'success': result['success'],
                'duration': duration
            })
            
            return result
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': f"Command timeout after {timeout}s",
                'stdout': '',
                'stderr': f"Timeout: {timeout}s exceeded",
                'returncode': -2,
                'duration': timeout,
                'command': cmd
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'stdout': '',
                'stderr': str(e),
                'returncode': -3,
                'duration': time.time() - start_time,
                'command': cmd
            }
    
    def run_async(self, cmd: str, cwd: Optional[str] = None) -> subprocess.Popen:
        """Run command asynchronously."""
        return subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=cwd
        )
    
    def run_batch(self, commands: List[str], stop_on_error: bool = True,
                 timeout: int = 30) -> List[Dict[str, Any]]:
        """Run multiple commands in sequence."""
        results = []
        
        for cmd in commands:
            result = self.run(cmd, timeout=timeout)
            results.append(result)
            
            if stop_on_error and not result['success']:
                break
        
        return results
    
    def run_parallel(self, commands: List[str], timeout: int = 30) -> List[Dict[str, Any]]:
        """Run multiple commands in parallel."""
        processes = []
        
        for cmd in commands:
            proc = self.run_async(cmd)
            processes.append((cmd, proc))
        
        results = []
        for cmd, proc in processes:
            try:
                stdout, stderr = proc.communicate(timeout=timeout)
                results.append({
                    'success': proc.returncode == 0,
                    'stdout': stdout,
                    'stderr': stderr,
                    'returncode': proc.returncode,
                    'command': cmd
                })
            except subprocess.TimeoutExpired:
                proc.kill()
                results.append({
                    'success': False,
                    'error': 'Timeout',
                    'command': cmd
                })
        
        return results
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information."""
        return {
            'platform': platform.system(),
            'platform_release': platform.release(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'processor': platform.processor(),
        }


"""Simple shell tool to run commands (backwards compatible API)."""
import subprocess
from typing import Optional as _Optional


def run(cmd: str, timeout: _Optional[int] = 30):
    """Run a shell command and return stdout (text)."""
    completed = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    if completed.returncode != 0:
        raise RuntimeError(f"Command failed: {completed.stderr.strip()}")
    return completed.stdout.strip()


def run_shell(cmd: str, timeout: _Optional[int] = 30):
    """Run a shell command and return stdout or error message (no exceptions)."""
    try:
        process = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if process.returncode != 0 and process.stderr:
            return f"Errore:\n{process.stderr}"
        return process.stdout if process.stdout else "Comando eseguito senza output."
    except subprocess.TimeoutExpired:
        return f"Timeout: comando ha superato i {timeout} secondi."
    except Exception as e:
        return f"Eccezione: {str(e)}"
    
    def get_running_processes(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get list of running processes."""
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'cpu_percent': proc.info['cpu_percent'],
                    'memory_percent': round(proc.info['memory_percent'], 2)
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Sort by CPU usage
        processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
        return processes[:limit]
    
    def kill_process(self, pid: int) -> Dict[str, Any]:
        """Kill process by PID."""
        try:
            process = psutil.Process(pid)
            name = process.name()
            process.kill()
            return {
                'success': True,
                'message': f"Process {name} (PID {pid}) killed"
            }
        except psutil.NoSuchProcess:
            return {
                'success': False,
                'error': f"Process {pid} not found"
            }
        except psutil.AccessDenied:
            return {
                'success': False,
                'error': f"Access denied to process {pid}"
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def find_command(self, command: str) -> Optional[str]:
        """Find full path of command."""
        if self.system == 'Windows':
            result = self.run(f"where {command}", check_safety=False)
        else:
            result = self.run(f"which {command}", check_safety=False)
        
        if result['success'] and result['stdout']:
            return result['stdout'].strip().split('\n')[0]
        return None
    
    def get_environment_variable(self, var: str) -> Optional[str]:
        """Get environment variable value."""
        return os.getenv(var)
    
    def set_environment_variable(self, var: str, value: str) -> bool:
        """Set environment variable (for current process only)."""
        try:
            os.environ[var] = value
            return True
        except Exception:
            return False
    
    def get_history(self, limit: int = 10) -> List[Dict]:
        """Get command execution history."""
        return self.history[-limit:]
    
    def clear_history(self):
        """Clear command history."""
        self.history = []


# Global executor instance
_executor = ShellExecutor()

def run(cmd: str, timeout: Optional[int] = 30) -> str:
    """
    Simple command execution - returns stdout or raises RuntimeError.
    
    Args:
        cmd: Command to execute
        timeout: Timeout in seconds
        
    Returns:
        Command output as string
        
    Raises:
        RuntimeError: If command fails
    """
    result = _executor.run(cmd, timeout=timeout)
    if not result['success']:
        raise RuntimeError(f"Command failed: {result.get('stderr', result.get('error'))}")
    return result['stdout'].strip()

def run_shell(cmd: str, timeout: Optional[int] = 30) -> str:
    """
    Safe command execution - returns output or error message (no exceptions).
    
    Args:
        cmd: Command to execute
        timeout: Timeout in seconds
        
    Returns:
        Command output or error message
    """
    result = _executor.run(cmd, timeout=timeout)
    
    if not result['success']:
        error_msg = result.get('stderr') or result.get('error', 'Unknown error')
        return f"Errore:\n{error_msg}"
    
    return result['stdout'] if result['stdout'] else "Comando eseguito senza output."

def run_advanced(cmd: str, timeout: int = 30, cwd: str = None, 
                env: Dict = None, check_safety: bool = True) -> Dict[str, Any]:
    """
    Advanced command execution with full control and detailed results.
    
    Args:
        cmd: Command to execute
        timeout: Timeout in seconds
        cwd: Working directory
        env: Environment variables
        check_safety: Check command safety
        
    Returns:
        Dict with detailed execution results
    """
    return _executor.run(cmd, timeout=timeout, cwd=cwd, env=env, check_safety=check_safety)

def get_system_info() -> Dict[str, Any]:
    """Get system information."""
    return _executor.get_system_info()

def get_processes(limit: int = 10) -> List[Dict[str, Any]]:
    """Get running processes."""
    return _executor.get_running_processes(limit)

def find_command(command: str) -> Optional[str]:
    """Find command path."""
    return _executor.find_command(command)

