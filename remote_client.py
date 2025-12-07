"""
Remote Super Agent Client - Client per interagire con server remoto
"""

import requests
import json
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class RemoteAgentConfig:
    """Configurazione client remoto"""
    base_url: str = "http://localhost:5000"
    username: str = "admin"
    password: str = "admin123"
    timeout: int = 30


class RemoteSuperAgentClient:
    """Client per Super Agent remoto"""
    
    def __init__(self, config: RemoteAgentConfig = None):
        self.config = config or RemoteAgentConfig()
        self.token: Optional[str] = None
        self.session = requests.Session()
        
    def login(self) -> bool:
        """Login to remote server"""
        url = f"{self.config.base_url}/api/login"
        
        try:
            response = self.session.post(
                url,
                json={
                    'username': self.config.username,
                    'password': self.config.password
                },
                timeout=self.config.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data['token']
                print(f"[OK] Logged in as {data['username']}")
                return True
            else:
                print(f"[ERROR] Login failed: {response.json()}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Connection failed: {str(e)}")
            return False
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers with auth token"""
        return {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Check server health"""
        url = f"{self.config.base_url}/api/health"
        response = self.session.get(url, timeout=self.config.timeout)
        return response.json()
    
    def create_task(self, task_type: str, parameters: Dict[str, Any]) -> str:
        """Create remote task"""
        if not self.token:
            raise ValueError("Not logged in. Call login() first.")
        
        url = f"{self.config.base_url}/api/tasks"
        
        response = self.session.post(
            url,
            json={
                'task_type': task_type,
                'parameters': parameters
            },
            headers=self._get_headers(),
            timeout=self.config.timeout
        )
        
        if response.status_code == 201:
            data = response.json()
            return data['task_id']
        else:
            raise Exception(f"Task creation failed: {response.json()}")
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get task status"""
        if not self.token:
            raise ValueError("Not logged in. Call login() first.")
        
        url = f"{self.config.base_url}/api/tasks/{task_id}"
        
        response = self.session.get(
            url,
            headers=self._get_headers(),
            timeout=self.config.timeout
        )
        
        return response.json()
    
    def wait_for_task(self, task_id: str, max_wait: int = 60) -> Dict[str, Any]:
        """Wait for task to complete"""
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            status = self.get_task_status(task_id)
            
            if status['status'] in ['completed', 'failed']:
                return status
            
            time.sleep(1)
        
        raise TimeoutError(f"Task {task_id} did not complete within {max_wait}s")
    
    def list_tasks(self) -> List[Dict[str, Any]]:
        """List all tasks"""
        if not self.token:
            raise ValueError("Not logged in. Call login() first.")
        
        url = f"{self.config.base_url}/api/tasks"
        
        response = self.session.get(
            url,
            headers=self._get_headers(),
            timeout=self.config.timeout
        )
        
        return response.json()['tasks']
    
    def delete_task(self, task_id: str) -> bool:
        """Delete task"""
        if not self.token:
            raise ValueError("Not logged in. Call login() first.")
        
        url = f"{self.config.base_url}/api/tasks/{task_id}"
        
        response = self.session.delete(
            url,
            headers=self._get_headers(),
            timeout=self.config.timeout
        )
        
        return response.status_code == 200
    
    def get_stats(self) -> Dict[str, Any]:
        """Get server statistics"""
        if not self.token:
            raise ValueError("Not logged in. Call login() first.")
        
        url = f"{self.config.base_url}/api/stats"
        
        response = self.session.get(
            url,
            headers=self._get_headers(),
            timeout=self.config.timeout
        )
        
        return response.json()
    
    # High-level API methods
    
    def generate_code(self, description: str) -> Dict[str, Any]:
        """Generate code remotely"""
        if not self.token:
            raise ValueError("Not logged in. Call login() first.")
        
        url = f"{self.config.base_url}/api/agent/code"
        
        response = self.session.post(
            url,
            json={'description': description},
            headers=self._get_headers(),
            timeout=self.config.timeout
        )
        
        return response.json()
    
    def analyze_code(self, code: str) -> Dict[str, Any]:
        """Analyze code remotely"""
        if not self.token:
            raise ValueError("Not logged in. Call login() first.")
        
        url = f"{self.config.base_url}/api/agent/analyze"
        
        response = self.session.post(
            url,
            json={'code': code},
            headers=self._get_headers(),
            timeout=self.config.timeout
        )
        
        return response.json()
    
    def refactor_code(self, code: str) -> Dict[str, Any]:
        """Refactor code remotely"""
        if not self.token:
            raise ValueError("Not logged in. Call login() first.")
        
        url = f"{self.config.base_url}/api/agent/refactor"
        
        response = self.session.post(
            url,
            json={'code': code},
            headers=self._get_headers(),
            timeout=self.config.timeout
        )
        
        return response.json()
    
    def neural_predict(self, input_data: list) -> Dict[str, Any]:
        """Neural network prediction"""
        if not self.token:
            raise ValueError("Not logged in. Call login() first.")
        
        url = f"{self.config.base_url}/api/agent/neural/predict"
        
        response = self.session.post(
            url,
            json={'input': input_data},
            headers=self._get_headers(),
            timeout=self.config.timeout
        )
        
        return response.json()
    
    def run_async_task(self, task_type: str, parameters: Dict[str, Any], 
                      wait: bool = True) -> Dict[str, Any]:
        """Run task asynchronously"""
        task_id = self.create_task(task_type, parameters)
        print(f"[*] Task created: {task_id}")
        
        if wait:
            result = self.wait_for_task(task_id)
            print(f"[OK] Task completed: {result['status']}")
            return result
        
        return {'task_id': task_id, 'status': 'pending'}


def demo_remote_client():
    """Demo client usage"""
    print("=" * 80)
    print("REMOTE SUPER AGENT CLIENT DEMO")
    print("=" * 80)
    
    # Create client
    client = RemoteSuperAgentClient()
    
    # Health check
    print("\n[*] Checking server health...")
    try:
        health = client.health_check()
        print(f"   Status: {health['status']}")
        print(f"   Version: {health['version']}")
    except Exception as e:
        print(f"   [ERROR] Server not available: {str(e)}")
        print("   Please start the server first: python remote_server.py")
        return
    
    # Login
    print("\n[*] Logging in...")
    if not client.login():
        return
    
    # Generate code
    print("\n[*] Generating code...")
    result = client.generate_code("Function to calculate factorial")
    print(f"   Generated {result['lines']} lines")
    print(f"   Quality score: {result['quality_score']}")
    print(f"   Code:\n{result['code']}")
    
    # Analyze code
    print("\n[*] Analyzing code...")
    code_sample = "def hello():\n    print('Hello')"
    analysis = client.analyze_code(code_sample)
    print(f"   Lines: {analysis['lines']}")
    print(f"   Complexity: {analysis['complexity']}")
    print(f"   Quality: {analysis['quality_score']}")
    
    # Neural prediction
    print("\n[*] Neural network prediction...")
    prediction = client.neural_predict([[1, 2, 3, 4]])
    print(f"   Confidence: {prediction['confidence']}")
    print(f"   Model: {prediction['model']}")
    print(f"   Latency: {prediction['latency_ms']}ms")
    
    # Async task
    print("\n[*] Creating async task...")
    task_result = client.run_async_task(
        'generate_code',
        {'description': 'Sort algorithm'},
        wait=True
    )
    print(f"   Task result: {task_result['result']}")
    
    # Get stats
    print("\n[*] Server statistics...")
    stats = client.get_stats()
    print(f"   Total requests: {stats['total_requests']}")
    print(f"   Successful tasks: {stats['successful_tasks']}")
    print(f"   Total tasks: {stats['total_tasks']}")
    print(f"   Uptime: {stats['uptime']}")
    
    print("\n[OK] Demo completed successfully!")


if __name__ == "__main__":
    demo_remote_client()
