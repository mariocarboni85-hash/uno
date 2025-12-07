"""
Python Virtual Environment Manager
Complete virtual environment creation and management
"""
import os
import sys
import subprocess
import venv
import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import platform


class VirtualEnvironmentManager:
    """Manage Python virtual environments."""
    
    def __init__(self):
        self.python_exe = sys.executable
        self.platform = platform.system()
        self.envs_dir = Path.cwd() / "venvs"
        self.config_file = self.envs_dir / "environments.json"
        
        # Ensure envs directory exists
        self.envs_dir.mkdir(exist_ok=True)
        
        # Load environments config
        self.environments = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load environments configuration."""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_config(self):
        """Save environments configuration."""
        with open(self.config_file, 'w') as f:
            json.dump(self.environments, f, indent=2)
    
    def _get_activation_script(self, env_path: Path) -> str:
        """Get activation script path for platform."""
        if self.platform == "Windows":
            return str(env_path / "Scripts" / "activate.ps1")
        else:
            return str(env_path / "bin" / "activate")
    
    def _get_python_executable(self, env_path: Path) -> str:
        """Get Python executable path in venv."""
        if self.platform == "Windows":
            return str(env_path / "Scripts" / "python.exe")
        else:
            return str(env_path / "bin" / "python")
    
    def _get_pip_executable(self, env_path: Path) -> str:
        """Get pip executable path in venv."""
        if self.platform == "Windows":
            return str(env_path / "Scripts" / "pip.exe")
        else:
            return str(env_path / "bin" / "pip")
    
    def create_venv(self, name: str, python_version: Optional[str] = None,
                   with_pip: bool = True, system_site_packages: bool = False,
                   prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new virtual environment.
        
        Args:
            name: Environment name
            python_version: Specific Python version (e.g., "3.11")
            with_pip: Install pip in the environment
            system_site_packages: Give access to system site-packages
            prompt: Custom prompt prefix
        
        Returns:
            Dictionary with environment details
        """
        env_path = self.envs_dir / name
        
        # Check if already exists
        if env_path.exists():
            return {
                'success': False,
                'error': f'Environment "{name}" already exists',
                'path': str(env_path)
            }
        
        try:
            # Create builder
            builder = venv.EnvBuilder(
                system_site_packages=system_site_packages,
                clear=False,
                symlinks=(self.platform != "Windows"),
                upgrade=False,
                with_pip=with_pip,
                prompt=prompt or name
            )
            
            # Create environment
            builder.create(str(env_path))
            
            # Get paths
            python_exe = self._get_python_executable(env_path)
            pip_exe = self._get_pip_executable(env_path)
            activate_script = self._get_activation_script(env_path)
            
            # Verify creation
            if not Path(python_exe).exists():
                return {
                    'success': False,
                    'error': 'Failed to create Python executable'
                }
            
            # Upgrade pip if requested
            if with_pip:
                subprocess.run(
                    [python_exe, "-m", "pip", "install", "--upgrade", "pip"],
                    capture_output=True,
                    timeout=60
                )
            
            # Save to config
            self.environments[name] = {
                'path': str(env_path),
                'python': python_exe,
                'pip': pip_exe,
                'activate': activate_script,
                'created': True,
                'system_site_packages': system_site_packages
            }
            self._save_config()
            
            return {
                'success': True,
                'name': name,
                'path': str(env_path),
                'python': python_exe,
                'pip': pip_exe,
                'activate': activate_script,
                'message': f'Virtual environment "{name}" created successfully'
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def delete_venv(self, name: str) -> Dict[str, Any]:
        """Delete a virtual environment."""
        if name not in self.environments:
            return {
                'success': False,
                'error': f'Environment "{name}" not found'
            }
        
        env_path = Path(self.environments[name]['path'])
        
        try:
            if env_path.exists():
                shutil.rmtree(env_path)
            
            del self.environments[name]
            self._save_config()
            
            return {
                'success': True,
                'message': f'Environment "{name}" deleted successfully'
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_venvs(self) -> List[Dict[str, Any]]:
        """List all virtual environments."""
        envs = []
        
        for name, config in self.environments.items():
            env_path = Path(config['path'])
            exists = env_path.exists()
            
            # Get installed packages count
            packages_count = 0
            if exists:
                try:
                    result = subprocess.run(
                        [config['python'], "-m", "pip", "list", "--format=json"],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    if result.returncode == 0:
                        packages = json.loads(result.stdout)
                        packages_count = len(packages)
                except:
                    pass
            
            envs.append({
                'name': name,
                'path': str(env_path),
                'exists': exists,
                'python': config['python'],
                'packages_count': packages_count,
                'system_site_packages': config.get('system_site_packages', False)
            })
        
        return envs
    
    def get_venv_info(self, name: str) -> Dict[str, Any]:
        """Get detailed information about a virtual environment."""
        if name not in self.environments:
            return {
                'success': False,
                'error': f'Environment "{name}" not found'
            }
        
        config = self.environments[name]
        env_path = Path(config['path'])
        
        if not env_path.exists():
            return {
                'success': False,
                'error': f'Environment path does not exist: {env_path}'
            }
        
        info = {
            'name': name,
            'path': str(env_path),
            'python': config['python'],
            'pip': config['pip'],
            'activate': config['activate']
        }
        
        # Get Python version
        try:
            result = subprocess.run(
                [config['python'], "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            info['python_version'] = result.stdout.strip()
        except:
            info['python_version'] = 'Unknown'
        
        # Get pip version
        try:
            result = subprocess.run(
                [config['python'], "-m", "pip", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            info['pip_version'] = result.stdout.strip()
        except:
            info['pip_version'] = 'Unknown'
        
        # Get installed packages
        try:
            result = subprocess.run(
                [config['python'], "-m", "pip", "list", "--format=json"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                packages = json.loads(result.stdout)
                info['packages'] = packages
                info['packages_count'] = len(packages)
        except:
            info['packages'] = []
            info['packages_count'] = 0
        
        return info
    
    def get_packages(self, name: str) -> List[Dict[str, str]]:
        """
        Get list of installed packages in virtual environment.
        
        Args:
            name: Environment name
            
        Returns:
            List of package dictionaries with 'name' and 'version' keys
        """
        if name not in self.environments:
            return []
        
        config = self.environments[name]
        
        try:
            result = subprocess.run(
                [config['python'], "-m", "pip", "list", "--format=json"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return json.loads(result.stdout)
            return []
        except:
            return []
    
    def install_package(self, name: str, package: str,
                       upgrade: bool = False) -> Dict[str, Any]:
        """
        Install a package in virtual environment.
        
        Args:
            name: Environment name
            package: Package name (e.g., "requests" or "requests==2.28.0")
            upgrade: Upgrade if already installed
        """
        if name not in self.environments:
            return {
                'success': False,
                'error': f'Environment "{name}" not found'
            }
        
        config = self.environments[name]
        python_exe = config['python']
        
        try:
            cmd = [python_exe, "-m", "pip", "install"]
            if upgrade:
                cmd.append("--upgrade")
            cmd.append(package)
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            return {
                'success': result.returncode == 0,
                'package': package,
                'output': result.stdout,
                'error': result.stderr if result.returncode != 0 else None
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def install_requirements(self, name: str, requirements_file: str) -> Dict[str, Any]:
        """Install packages from requirements.txt."""
        if name not in self.environments:
            return {
                'success': False,
                'error': f'Environment "{name}" not found'
            }
        
        if not Path(requirements_file).exists():
            return {
                'success': False,
                'error': f'Requirements file not found: {requirements_file}'
            }
        
        config = self.environments[name]
        python_exe = config['python']
        
        try:
            result = subprocess.run(
                [python_exe, "-m", "pip", "install", "-r", requirements_file],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            return {
                'success': result.returncode == 0,
                'requirements_file': requirements_file,
                'output': result.stdout,
                'error': result.stderr if result.returncode != 0 else None
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def uninstall_package(self, name: str, package: str) -> Dict[str, Any]:
        """Uninstall a package from virtual environment."""
        if name not in self.environments:
            return {
                'success': False,
                'error': f'Environment "{name}" not found'
            }
        
        config = self.environments[name]
        python_exe = config['python']
        
        try:
            result = subprocess.run(
                [python_exe, "-m", "pip", "uninstall", "-y", package],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            return {
                'success': result.returncode == 0,
                'package': package,
                'output': result.stdout,
                'error': result.stderr if result.returncode != 0 else None
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def export_requirements(self, name: str, output_file: str = "requirements.txt") -> Dict[str, Any]:
        """Export installed packages to requirements.txt."""
        if name not in self.environments:
            return {
                'success': False,
                'error': f'Environment "{name}" not found'
            }
        
        config = self.environments[name]
        python_exe = config['python']
        
        try:
            result = subprocess.run(
                [python_exe, "-m", "pip", "freeze"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                with open(output_file, 'w') as f:
                    f.write(result.stdout)
                
                return {
                    'success': True,
                    'output_file': output_file,
                    'packages_count': len(result.stdout.strip().split('\n'))
                }
            else:
                return {
                    'success': False,
                    'error': result.stderr
                }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def run_script(self, name: str, script_path: str,
                  args: Optional[List[str]] = None) -> Dict[str, Any]:
        """Run a Python script in virtual environment."""
        if name not in self.environments:
            return {
                'success': False,
                'error': f'Environment "{name}" not found'
            }
        
        if not Path(script_path).exists():
            return {
                'success': False,
                'error': f'Script not found: {script_path}'
            }
        
        config = self.environments[name]
        python_exe = config['python']
        
        try:
            cmd = [python_exe, script_path]
            if args:
                cmd.extend(args)
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            return {
                'success': result.returncode == 0,
                'script': script_path,
                'exit_code': result.returncode,
                'output': result.stdout,
                'error': result.stderr if result.returncode != 0 else None
            }
        
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Script execution timed out (300s)'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_activation_command(self, name: str) -> Dict[str, Any]:
        """Get command to activate virtual environment."""
        if name not in self.environments:
            return {
                'success': False,
                'error': f'Environment "{name}" not found'
            }
        
        config = self.environments[name]
        activate_script = config['activate']
        
        if self.platform == "Windows":
            # PowerShell
            command = f". {activate_script}"
            shell = "PowerShell"
        else:
            # Bash/Zsh
            command = f"source {activate_script}"
            shell = "Bash/Zsh"
        
        return {
            'success': True,
            'command': command,
            'shell': shell,
            'script': activate_script,
            'usage': f"To activate: {command}"
        }
    
    def clone_venv(self, source_name: str, target_name: str) -> Dict[str, Any]:
        """Clone a virtual environment."""
        if source_name not in self.environments:
            return {
                'success': False,
                'error': f'Source environment "{source_name}" not found'
            }
        
        if target_name in self.environments:
            return {
                'success': False,
                'error': f'Target environment "{target_name}" already exists'
            }
        
        # Create new environment
        result = self.create_venv(target_name)
        
        if not result['success']:
            return result
        
        # Export requirements from source
        temp_req = "temp_requirements.txt"
        export_result = self.export_requirements(source_name, temp_req)
        
        if not export_result['success']:
            return {
                'success': False,
                'error': 'Failed to export source requirements'
            }
        
        # Install in target
        install_result = self.install_requirements(target_name, temp_req)
        
        # Clean up temp file
        Path(temp_req).unlink(missing_ok=True)
        
        if install_result['success']:
            return {
                'success': True,
                'message': f'Environment "{source_name}" cloned to "{target_name}"',
                'target': target_name
            }
        else:
            return {
                'success': False,
                'error': 'Failed to install packages in target environment'
            }


# Global instance
_venv_manager = VirtualEnvironmentManager()

def create_venv(name: str, **kwargs) -> Dict:
    """Create virtual environment."""
    return _venv_manager.create_venv(name, **kwargs)

def delete_venv(name: str) -> Dict:
    """Delete virtual environment."""
    return _venv_manager.delete_venv(name)

def list_venvs() -> List[Dict]:
    """List virtual environments."""
    return _venv_manager.list_venvs()

def install_package(name: str, package: str, upgrade: bool = False) -> Dict:
    """Install package in virtual environment."""
    return _venv_manager.install_package(name, package, upgrade)

def get_venv_info(name: str) -> Dict:
    """Get virtual environment info."""
    return _venv_manager.get_venv_info(name)
