import yaml
from pathlib import Path


class PolicyViolation(Exception):
    pass


class PolicyEngine:
    def __init__(self, policy_path: str = None):
        # Resolve policy path with sensible fallbacks:
        # 1. explicit existing path
        # 2. treat provided name as relative to this module
        # 3. bundled 'policy.yaml' next to this module
        module_dir = Path(__file__).parent
        resolved = None
        if policy_path:
            p = Path(policy_path)
            if p.exists():
                resolved = p
            else:
                candidate = module_dir / policy_path
                if candidate.exists():
                    resolved = candidate
        if resolved is None:
            bundled = module_dir / 'policy.yaml'
            if bundled.exists():
                resolved = bundled
        if resolved is None:
            raise FileNotFoundError(f"Policy file not found: {policy_path}")

        self.policy = yaml.safe_load(resolved.read_text())

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
