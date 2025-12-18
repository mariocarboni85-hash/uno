import yaml
from pathlib import Path


class PolicyViolation(Exception):
    pass


class PolicyEngine:
    def __init__(self, policy_path: str = None):
        # default to bundled policy file next to this module
        if policy_path is None:
            policy_path = Path(__file__).with_name('policy.yaml')
        self.policy = yaml.safe_load(Path(policy_path).read_text())

    def authorize(self, action):
        perms = self.policy.get('permissions', {}).get(action.type)

        if not perms or not perms.get('allowed', False):
            raise PolicyViolation(f"Azione '{action.type}' vietata")

        if action.type in ("file_read", "file_write"):
            self._check_path(action.payload.get('path', ''), perms)

    def _check_path(self, path: str, perms: dict):
        allowed = perms.get('paths', [])
        # Use Path.match for pattern matching
        if not any(Path(path).match(p) for p in allowed):
            raise PolicyViolation(f"Path non autorizzato: {path}")
