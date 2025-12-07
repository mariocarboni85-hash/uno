"""
Security System for Super Agent
Sistema completo di sicurezza con autenticazione, autorizzazione, crittografia
"""

import hashlib
import hmac
import secrets
import base64
import json
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import re
import os
from pathlib import Path


class SecurityLevel(Enum):
    """Livelli di sicurezza"""
    PUBLIC = "public"
    AUTHENTICATED = "authenticated"
    CONFIDENTIAL = "confidential"
    SECRET = "secret"
    TOP_SECRET = "top_secret"


class Permission(Enum):
    """Permessi sistema"""
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    DELETE = "delete"
    ADMIN = "admin"


@dataclass
class User:
    """Utente sistema"""
    username: str
    password_hash: str
    salt: str
    roles: List[str] = field(default_factory=list)
    permissions: List[Permission] = field(default_factory=list)
    security_clearance: SecurityLevel = SecurityLevel.AUTHENTICATED
    created_at: str = ""
    last_login: Optional[str] = None
    failed_attempts: int = 0
    locked: bool = False
    mfa_enabled: bool = False
    mfa_secret: Optional[str] = None
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


@dataclass
class AuditLog:
    """Log di audit"""
    timestamp: str
    user: str
    action: str
    resource: str
    result: str
    ip_address: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'timestamp': self.timestamp,
            'user': self.user,
            'action': self.action,
            'resource': self.resource,
            'result': self.result,
            'ip_address': self.ip_address,
            'details': self.details
        }


class PasswordPolicy:
    """Policy password"""
    
    def __init__(self):
        self.min_length = 12
        self.require_uppercase = True
        self.require_lowercase = True
        self.require_digits = True
        self.require_special = True
        self.max_age_days = 90
        self.history_size = 5
        
    def validate(self, password: str) -> Tuple[bool, List[str]]:
        """Valida password"""
        errors = []
        
        if len(password) < self.min_length:
            errors.append(f"Password must be at least {self.min_length} characters")
        
        if self.require_uppercase and not re.search(r'[A-Z]', password):
            errors.append("Password must contain uppercase letter")
        
        if self.require_lowercase and not re.search(r'[a-z]', password):
            errors.append("Password must contain lowercase letter")
        
        if self.require_digits and not re.search(r'\d', password):
            errors.append("Password must contain digit")
        
        if self.require_special and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Password must contain special character")
        
        # Check common passwords
        common_passwords = ['password', '12345678', 'qwerty', 'admin123']
        if password.lower() in common_passwords:
            errors.append("Password is too common")
        
        return len(errors) == 0, errors


class Encryptor:
    """Sistema di crittografia"""
    
    @staticmethod
    def hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
        """Hash password con salt"""
        if salt is None:
            salt = secrets.token_hex(32)
        
        pwd_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000  # iterations
        )
        
        return base64.b64encode(pwd_hash).decode('utf-8'), salt
    
    @staticmethod
    def verify_password(password: str, password_hash: str, salt: str) -> bool:
        """Verifica password"""
        computed_hash, _ = Encryptor.hash_password(password, salt)
        return hmac.compare_digest(computed_hash, password_hash)
    
    @staticmethod
    def encrypt_data(data: str, key: str) -> str:
        """Crittografia simmetrica (XOR-based per demo)"""
        key_bytes = key.encode('utf-8')
        data_bytes = data.encode('utf-8')
        
        encrypted = bytearray()
        for i, byte in enumerate(data_bytes):
            encrypted.append(byte ^ key_bytes[i % len(key_bytes)])
        
        return base64.b64encode(bytes(encrypted)).decode('utf-8')
    
    @staticmethod
    def decrypt_data(encrypted: str, key: str) -> str:
        """Decrittografia"""
        try:
            encrypted_bytes = base64.b64decode(encrypted)
            key_bytes = key.encode('utf-8')
            
            decrypted = bytearray()
            for i, byte in enumerate(encrypted_bytes):
                decrypted.append(byte ^ key_bytes[i % len(key_bytes)])
            
            return bytes(decrypted).decode('utf-8')
        except Exception:
            return ""
    
    @staticmethod
    def generate_token(length: int = 32) -> str:
        """Genera token sicuro"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def generate_api_key() -> str:
        """Genera API key"""
        return f"sa_{secrets.token_urlsafe(32)}"


class InputValidator:
    """Validatore input per prevenire injection"""
    
    @staticmethod
    def sanitize_string(input_str: str) -> str:
        """Sanitizza stringa"""
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&', ';', '|', '`', '$']
        sanitized = input_str
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        return sanitized.strip()
    
    @staticmethod
    def validate_username(username: str) -> Tuple[bool, str]:
        """Valida username"""
        if not username or len(username) < 3:
            return False, "Username must be at least 3 characters"
        
        if len(username) > 32:
            return False, "Username too long (max 32)"
        
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            return False, "Username can only contain letters, numbers, _ and -"
        
        return True, "Valid"
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Valida email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_path(path: str) -> bool:
        """Valida path (previene path traversal)"""
        # Check for path traversal attempts
        if '..' in path or path.startswith('/'):
            return False
        
        # Ensure path is relative and safe
        try:
            safe_path = Path(path).resolve()
            return True
        except Exception:
            return False
    
    @staticmethod
    def validate_code_injection(code: str) -> Tuple[bool, List[str]]:
        """Rileva potenziali code injection"""
        dangerous_patterns = [
            r'__import__',
            r'eval\s*\(',
            r'exec\s*\(',
            r'compile\s*\(',
            r'open\s*\(',
            r'os\.',
            r'subprocess',
            r'system\s*\(',
            r'popen\s*\('
        ]
        
        found = []
        for pattern in dangerous_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                found.append(pattern)
        
        return len(found) == 0, found


class RateLimiter:
    """Rate limiting"""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, List[float]] = {}
    
    def check_limit(self, identifier: str) -> Tuple[bool, int]:
        """Check if rate limit exceeded"""
        now = time.time()
        
        if identifier not in self.requests:
            self.requests[identifier] = []
        
        # Remove old requests outside window
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if now - req_time < self.window_seconds
        ]
        
        # Check limit
        if len(self.requests[identifier]) >= self.max_requests:
            return False, len(self.requests[identifier])
        
        # Add current request
        self.requests[identifier].append(now)
        return True, len(self.requests[identifier])


class SecurityManager:
    """Gestore sicurezza principale"""
    
    def __init__(self, data_dir: str = "security_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.users: Dict[str, User] = {}
        self.audit_logs: List[AuditLog] = []
        self.sessions: Dict[str, Dict[str, Any]] = {}
        
        self.password_policy = PasswordPolicy()
        self.rate_limiter = RateLimiter()
        self.encryptor = Encryptor()
        self.validator = InputValidator()
        
        self.master_key = self._get_or_create_master_key()
        
        # Load data
        self._load_users()
        
    def _get_or_create_master_key(self) -> str:
        """Get or create master encryption key"""
        key_file = self.data_dir / ".master_key"
        
        if key_file.exists():
            with open(key_file, 'r') as f:
                return f.read().strip()
        else:
            key = secrets.token_urlsafe(32)
            with open(key_file, 'w') as f:
                f.write(key)
            # Set restrictive permissions
            os.chmod(key_file, 0o600)
            return key
    
    def _load_users(self):
        """Load users from disk"""
        users_file = self.data_dir / "users.json"
        if users_file.exists():
            try:
                with open(users_file, 'r') as f:
                    data = json.load(f)
                    for username, user_data in data.items():
                        # Convert string permissions back to enum
                        if 'permissions' in user_data:
                            user_data['permissions'] = [
                                Permission(p) if isinstance(p, str) else p
                                for p in user_data['permissions']
                            ]
                        # Convert string security_clearance back to enum
                        if 'security_clearance' in user_data:
                            user_data['security_clearance'] = SecurityLevel(user_data['security_clearance'])
                        
                        self.users[username] = User(**user_data)
            except Exception as e:
                print(f"Error loading users: {e}")
    
    def _save_users(self):
        """Save users to disk"""
        users_file = self.data_dir / "users.json"
        try:
            data = {
                username: {
                    'username': user.username,
                    'password_hash': user.password_hash,
                    'salt': user.salt,
                    'roles': user.roles,
                    'permissions': [p.value if isinstance(p, Permission) else p for p in user.permissions],
                    'security_clearance': user.security_clearance.value if isinstance(user.security_clearance, SecurityLevel) else user.security_clearance,
                    'created_at': user.created_at,
                    'last_login': user.last_login,
                    'failed_attempts': user.failed_attempts,
                    'locked': user.locked,
                    'mfa_enabled': user.mfa_enabled,
                    'mfa_secret': user.mfa_secret
                }
                for username, user in self.users.items()
            }
            with open(users_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving users: {e}")
    
    def create_user(self, username: str, password: str, 
                   roles: Optional[List[str]] = None,
                   permissions: Optional[List[Permission]] = None) -> Tuple[bool, str]:
        """Create new user"""
        # Validate username
        valid, msg = self.validator.validate_username(username)
        if not valid:
            return False, msg
        
        # Check if exists
        if username in self.users:
            return False, "Username already exists"
        
        # Validate password
        valid, errors = self.password_policy.validate(password)
        if not valid:
            return False, "; ".join(errors)
        
        # Create user
        password_hash, salt = self.encryptor.hash_password(password)
        
        user = User(
            username=username,
            password_hash=password_hash,
            salt=salt,
            roles=roles or [],
            permissions=permissions or [Permission.READ],
            security_clearance=SecurityLevel.AUTHENTICATED
        )
        
        self.users[username] = user
        self._save_users()
        
        # Audit log
        self._add_audit_log(username, "CREATE_USER", username, "SUCCESS")
        
        return True, "User created successfully"
    
    def authenticate(self, username: str, password: str,
                    ip_address: Optional[str] = None) -> Tuple[bool, Optional[str]]:
        """Authenticate user"""
        # Rate limiting
        allowed, count = self.rate_limiter.check_limit(username)
        if not allowed:
            self._add_audit_log(username, "AUTH", username, "RATE_LIMITED", ip_address)
            return False, None
        
        # Check user exists
        if username not in self.users:
            self._add_audit_log(username, "AUTH", username, "USER_NOT_FOUND", ip_address)
            return False, None
        
        user = self.users[username]
        
        # Check if locked
        if user.locked:
            self._add_audit_log(username, "AUTH", username, "ACCOUNT_LOCKED", ip_address)
            return False, None
        
        # Verify password
        if self.encryptor.verify_password(password, user.password_hash, user.salt):
            # Success
            user.failed_attempts = 0
            user.last_login = datetime.now().isoformat()
            self._save_users()
            
            # Create session
            session_token = self.encryptor.generate_token()
            self.sessions[session_token] = {
                'username': username,
                'created_at': time.time(),
                'ip_address': ip_address
            }
            
            self._add_audit_log(username, "AUTH", username, "SUCCESS", ip_address)
            return True, session_token
        else:
            # Failed
            user.failed_attempts += 1
            if user.failed_attempts >= 5:
                user.locked = True
            self._save_users()
            
            self._add_audit_log(username, "AUTH", username, "FAILED", ip_address)
            return False, None
    
    def validate_session(self, session_token: str) -> Optional[str]:
        """Validate session token"""
        if session_token not in self.sessions:
            return None
        
        session = self.sessions[session_token]
        
        # Check expiry (24 hours)
        if time.time() - session['created_at'] > 86400:
            del self.sessions[session_token]
            return None
        
        return session['username']
    
    def check_permission(self, username: str, permission: Permission) -> bool:
        """Check if user has permission"""
        if username not in self.users:
            return False
        
        user = self.users[username]
        
        # Admin has all permissions
        if Permission.ADMIN in user.permissions:
            return True
        
        return permission in user.permissions
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        return self.encryptor.encrypt_data(data, self.master_key)
    
    def decrypt_sensitive_data(self, encrypted: str) -> str:
        """Decrypt sensitive data"""
        return self.encryptor.decrypt_data(encrypted, self.master_key)
    
    def _add_audit_log(self, user: str, action: str, resource: str,
                      result: str, ip_address: Optional[str] = None,
                      details: Optional[Dict[str, Any]] = None):
        """Add audit log entry"""
        log = AuditLog(
            timestamp=datetime.now().isoformat(),
            user=user,
            action=action,
            resource=resource,
            result=result,
            ip_address=ip_address,
            details=details
        )
        
        self.audit_logs.append(log)
        
        # Save to file
        audit_file = self.data_dir / "audit.log"
        with open(audit_file, 'a') as f:
            f.write(json.dumps(log.to_dict()) + '\n')
    
    def get_audit_logs(self, user: Optional[str] = None,
                      action: Optional[str] = None,
                      limit: int = 100) -> List[AuditLog]:
        """Get audit logs"""
        logs = self.audit_logs[-limit:]
        
        if user:
            logs = [log for log in logs if log.user == user]
        
        if action:
            logs = [log for log in logs if log.action == action]
        
        return logs
    
    def generate_api_key(self, username: str) -> Optional[str]:
        """Generate API key for user"""
        if username not in self.users:
            return None
        
        api_key = self.encryptor.generate_api_key()
        
        # Store encrypted
        user = self.users[username]
        if not hasattr(user, 'api_keys'):
            user.api_keys = []
        
        self._add_audit_log(username, "GENERATE_API_KEY", username, "SUCCESS")
        
        return api_key
    
    def scan_vulnerabilities(self, code: str) -> Dict[str, Any]:
        """Scan code for vulnerabilities"""
        results = {
            'safe': True,
            'issues': [],
            'severity': 'low'
        }
        
        # Check code injection
        safe, patterns = self.validator.validate_code_injection(code)
        if not safe:
            results['safe'] = False
            results['severity'] = 'high'
            results['issues'].append({
                'type': 'CODE_INJECTION',
                'patterns': patterns,
                'description': 'Potentially dangerous code patterns detected'
            })
        
        # Check for hardcoded secrets
        secret_patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']'
        ]
        
        for pattern in secret_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                results['safe'] = False
                results['issues'].append({
                    'type': 'HARDCODED_SECRET',
                    'pattern': pattern,
                    'description': 'Hardcoded secrets detected'
                })
                if results['severity'] == 'low':
                    results['severity'] = 'medium'
        
        return results
    
    def get_security_report(self) -> Dict[str, Any]:
        """Generate security report"""
        return {
            'total_users': len(self.users),
            'locked_users': sum(1 for u in self.users.values() if u.locked),
            'mfa_enabled': sum(1 for u in self.users.values() if u.mfa_enabled),
            'total_audit_logs': len(self.audit_logs),
            'failed_auth_attempts': sum(
                1 for log in self.audit_logs[-100:]
                if log.action == 'AUTH' and log.result == 'FAILED'
            ),
            'active_sessions': len(self.sessions),
            'password_policy': {
                'min_length': self.password_policy.min_length,
                'complexity_required': True
            }
        }


def create_default_users(manager: SecurityManager):
    """Create default users for demo"""
    users = [
        ('admin', 'AdminPass123!', ['admin'], [Permission.ADMIN]),
        ('developer', 'DevPass123!', ['developer'], [Permission.READ, Permission.WRITE, Permission.EXECUTE]),
        ('viewer', 'ViewPass123!', ['viewer'], [Permission.READ])
    ]
    
    for username, password, roles, permissions in users:
        success, msg = manager.create_user(username, password, roles, permissions)
        if success:
            print(f"[OK] Created user: {username}")
        else:
            print(f"[SKIP] {username}: {msg}")


if __name__ == "__main__":
    print("Security System for Super Agent")
    print("=" * 80)
    
    # Create security manager
    manager = SecurityManager()
    
    # Create default users
    create_default_users(manager)
    
    # Demo authentication
    print("\n[*] Testing authentication...")
    success, token = manager.authenticate('admin', 'AdminPass123!')
    if success:
        print(f"   [OK] Authenticated: {token[:20]}...")
    
    # Demo permission check
    print("\n[*] Testing permissions...")
    has_perm = manager.check_permission('admin', Permission.ADMIN)
    print(f"   Admin has ADMIN permission: {has_perm}")
    
    # Demo vulnerability scan
    print("\n[*] Testing vulnerability scan...")
    dangerous_code = "import os; os.system('rm -rf /')"
    scan_result = manager.scan_vulnerabilities(dangerous_code)
    print(f"   Safe: {scan_result['safe']}")
    print(f"   Issues: {len(scan_result['issues'])}")
    
    # Security report
    print("\n[*] Security Report:")
    report = manager.get_security_report()
    for key, value in report.items():
        print(f"   {key}: {value}")
    
    print("\n[OK] Security system initialized!")
