"""
Remote Super Agent Server - API REST per accesso remoto
"""

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import jwt
import datetime
import hashlib
import json
import threading
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
import uuid
from functools import wraps
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class RemoteTask:
    """Task remoto per Super Agent"""
    task_id: str
    task_type: str
    parameters: Dict[str, Any]
    status: str  # pending, running, completed, failed
    result: Optional[Any] = None
    error: Optional[str] = None
    created_at: str = ""
    completed_at: Optional[str] = None
    
    def to_dict(self):
        return asdict(self)


class RemoteSuperAgentServer:
    """Server per eseguire Super Agent in remoto"""
    
    def __init__(self, secret_key: str = None, port: int = 5000):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = secret_key or self._generate_secret_key()
        CORS(self.app)
        
        self.port = port
        self.tasks: Dict[str, RemoteTask] = {}
        self.users: Dict[str, str] = {
            'admin': self._hash_password('admin123'),
            'user': self._hash_password('user123')
        }
        
        # Statistics
        self.stats = {
            'total_requests': 0,
            'successful_tasks': 0,
            'failed_tasks': 0,
            'active_connections': 0,
            'uptime_start': datetime.datetime.now().isoformat()
        }
        
        self._setup_routes()
        
    def _generate_secret_key(self) -> str:
        """Generate random secret key"""
        return hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
    
    def _hash_password(self, password: str) -> str:
        """Hash password"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _create_token(self, username: str) -> str:
        """Create JWT token"""
        payload = {
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        return jwt.encode(payload, self.app.config['SECRET_KEY'], algorithm='HS256')
    
    def _verify_token(self, token: str) -> Optional[str]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.app.config['SECRET_KEY'], algorithms=['HS256'])
            return payload['username']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def require_auth(self, f):
        """Decorator for requiring authentication"""
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')
            
            if not token:
                return jsonify({'error': 'Token missing'}), 401
            
            if token.startswith('Bearer '):
                token = token[7:]
            
            username = self._verify_token(token)
            if not username:
                return jsonify({'error': 'Invalid or expired token'}), 401
            
            return f(username, *args, **kwargs)
        
        return decorated
    
    def _setup_routes(self):
        """Setup all API routes"""
        
        @self.app.route('/api/health', methods=['GET'])
        def health_check():
            """Health check endpoint"""
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.datetime.now().isoformat(),
                'version': '1.0.0'
            })
        
        @self.app.route('/api/login', methods=['POST'])
        def login():
            """Login endpoint"""
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return jsonify({'error': 'Username and password required'}), 400
            
            hashed_password = self._hash_password(password)
            
            if username in self.users and self.users[username] == hashed_password:
                token = self._create_token(username)
                logger.info(f"User {username} logged in successfully")
                return jsonify({
                    'token': token,
                    'username': username,
                    'expires_in': 86400  # 24 hours
                })
            
            return jsonify({'error': 'Invalid credentials'}), 401
        
        @self.app.route('/api/tasks', methods=['POST'])
        @self.require_auth
        def create_task(username):
            """Create new remote task"""
            self.stats['total_requests'] += 1
            
            data = request.get_json()
            task_type = data.get('task_type')
            parameters = data.get('parameters', {})
            
            if not task_type:
                return jsonify({'error': 'task_type required'}), 400
            
            task_id = str(uuid.uuid4())
            task = RemoteTask(
                task_id=task_id,
                task_type=task_type,
                parameters=parameters,
                status='pending',
                created_at=datetime.datetime.now().isoformat()
            )
            
            self.tasks[task_id] = task
            
            # Execute task in background
            threading.Thread(target=self._execute_task, args=(task_id,), daemon=True).start()
            
            logger.info(f"Task {task_id} created by {username}: {task_type}")
            
            return jsonify({
                'task_id': task_id,
                'status': 'pending',
                'message': 'Task created successfully'
            }), 201
        
        @self.app.route('/api/tasks/<task_id>', methods=['GET'])
        @self.require_auth
        def get_task(username, task_id):
            """Get task status and result"""
            task = self.tasks.get(task_id)
            
            if not task:
                return jsonify({'error': 'Task not found'}), 404
            
            return jsonify(task.to_dict())
        
        @self.app.route('/api/tasks', methods=['GET'])
        @self.require_auth
        def list_tasks(username):
            """List all tasks"""
            return jsonify({
                'tasks': [task.to_dict() for task in self.tasks.values()],
                'total': len(self.tasks)
            })
        
        @self.app.route('/api/tasks/<task_id>', methods=['DELETE'])
        @self.require_auth
        def delete_task(username, task_id):
            """Delete task"""
            if task_id in self.tasks:
                del self.tasks[task_id]
                logger.info(f"Task {task_id} deleted by {username}")
                return jsonify({'message': 'Task deleted successfully'})
            
            return jsonify({'error': 'Task not found'}), 404
        
        @self.app.route('/api/stats', methods=['GET'])
        @self.require_auth
        def get_stats(username):
            """Get server statistics"""
            stats = self.stats.copy()
            stats['total_tasks'] = len(self.tasks)
            stats['pending_tasks'] = sum(1 for t in self.tasks.values() if t.status == 'pending')
            stats['running_tasks'] = sum(1 for t in self.tasks.values() if t.status == 'running')
            stats['uptime'] = str(datetime.datetime.now() - 
                                datetime.datetime.fromisoformat(stats['uptime_start']))
            
            return jsonify(stats)
        
        @self.app.route('/api/agent/code', methods=['POST'])
        @self.require_auth
        def generate_code(username):
            """Generate Python code"""
            data = request.get_json()
            description = data.get('description', '')
            
            # Simulate code generation
            result = self._simulate_code_generation(description)
            
            self.stats['successful_tasks'] += 1
            logger.info(f"Code generated for {username}")
            
            return jsonify(result)
        
        @self.app.route('/api/agent/analyze', methods=['POST'])
        @self.require_auth
        def analyze_code(username):
            """Analyze code"""
            data = request.get_json()
            code = data.get('code', '')
            
            # Simulate code analysis
            result = self._simulate_code_analysis(code)
            
            self.stats['successful_tasks'] += 1
            logger.info(f"Code analyzed for {username}")
            
            return jsonify(result)
        
        @self.app.route('/api/agent/refactor', methods=['POST'])
        @self.require_auth
        def refactor_code(username):
            """Refactor code"""
            data = request.get_json()
            code = data.get('code', '')
            
            # Simulate refactoring
            result = self._simulate_refactoring(code)
            
            self.stats['successful_tasks'] += 1
            logger.info(f"Code refactored for {username}")
            
            return jsonify(result)
        
        @self.app.route('/api/agent/neural/predict', methods=['POST'])
        @self.require_auth
        def neural_predict(username):
            """Neural network prediction"""
            data = request.get_json()
            input_data = data.get('input', [])
            
            # Simulate neural prediction
            result = self._simulate_neural_prediction(input_data)
            
            self.stats['successful_tasks'] += 1
            logger.info(f"Neural prediction for {username}")
            
            return jsonify(result)
        
        @self.app.route('/api/stream', methods=['GET'])
        @self.require_auth
        def stream_updates(username):
            """Server-sent events for real-time updates"""
            def generate():
                while True:
                    stats = self.stats.copy()
                    stats['timestamp'] = datetime.datetime.now().isoformat()
                    yield f"data: {json.dumps(stats)}\n\n"
                    time.sleep(2)
            
            return Response(generate(), mimetype='text/event-stream')
    
    def _execute_task(self, task_id: str):
        """Execute task in background"""
        task = self.tasks[task_id]
        task.status = 'running'
        
        try:
            # Simulate task execution
            time.sleep(2)  # Simulate processing
            
            # Execute based on task type
            if task.task_type == 'generate_code':
                result = self._simulate_code_generation(task.parameters.get('description', ''))
            elif task.task_type == 'analyze_code':
                result = self._simulate_code_analysis(task.parameters.get('code', ''))
            elif task.task_type == 'refactor_code':
                result = self._simulate_refactoring(task.parameters.get('code', ''))
            elif task.task_type == 'neural_predict':
                result = self._simulate_neural_prediction(task.parameters.get('input', []))
            else:
                result = {'message': 'Task type not implemented'}
            
            task.result = result
            task.status = 'completed'
            task.completed_at = datetime.datetime.now().isoformat()
            self.stats['successful_tasks'] += 1
            
            logger.info(f"Task {task_id} completed successfully")
            
        except Exception as e:
            task.status = 'failed'
            task.error = str(e)
            task.completed_at = datetime.datetime.now().isoformat()
            self.stats['failed_tasks'] += 1
            
            logger.error(f"Task {task_id} failed: {str(e)}")
    
    def _simulate_code_generation(self, description: str) -> Dict[str, Any]:
        """Simulate code generation"""
        return {
            'code': f'def generated_function():\n    """{description}"""\n    pass',
            'language': 'python',
            'lines': 3,
            'quality_score': 0.95
        }
    
    def _simulate_code_analysis(self, code: str) -> Dict[str, Any]:
        """Simulate code analysis"""
        return {
            'lines': len(code.split('\n')),
            'complexity': 5,
            'quality_score': 0.88,
            'issues': [],
            'suggestions': ['Add docstrings', 'Add type hints']
        }
    
    def _simulate_refactoring(self, code: str) -> Dict[str, Any]:
        """Simulate refactoring"""
        return {
            'original_lines': len(code.split('\n')),
            'refactored_lines': len(code.split('\n')) - 2,
            'improvements': ['Simplified logic', 'Removed redundancy'],
            'refactored_code': code + '\n# Refactored'
        }
    
    def _simulate_neural_prediction(self, input_data: list) -> Dict[str, Any]:
        """Simulate neural network prediction"""
        import numpy as np
        predictions = np.random.rand(len(input_data) if input_data else 1, 10).tolist()
        return {
            'predictions': predictions,
            'confidence': 0.92,
            'model': 'enhanced_neural_network',
            'latency_ms': 15
        }
    
    def run(self, debug: bool = False):
        """Start server"""
        logger.info(f"Starting Remote Super Agent Server on port {self.port}")
        logger.info(f"API available at http://localhost:{self.port}/api")
        logger.info(f"Users: admin/admin123, user/user123")
        
        self.app.run(host='0.0.0.0', port=self.port, debug=debug, threaded=True)


if __name__ == "__main__":
    server = RemoteSuperAgentServer(port=5000)
    server.run(debug=True)
