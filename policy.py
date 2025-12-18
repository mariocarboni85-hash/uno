import os
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

try:
    import yaml
except Exception:
    yaml = None


class VitPolicy:
    def __init__(self, source: Optional[str] = None, policy_dict: Optional[Dict[str, Any]] = None):
        if policy_dict is not None:
            self.policy = policy_dict
        else:
            self.policy = {}
            if source:
                self.load(source)
            else:
                # try default bundled policy file
                default = Path(__file__).with_name('policy.yaml')
                if default.exists():
                    self.load(str(default))

    def load(self, path: str) -> None:
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(path)
        text = p.read_text(encoding='utf-8')
        if yaml:
            self.policy = yaml.safe_load(text)
        else:
            # fallback: try json
            try:
                self.policy = json.loads(text)
            except Exception:
                raise RuntimeError('PyYAML not installed and policy is not valid JSON')

    def check(self, action_type: str, sender: str = 'unknown', mode: Optional[str] = None, command: Optional[str] = None) -> Tuple[bool, str]:
        """Return (allowed: bool, reason: str).

        This implements a minimal policy check based on the `permissions` section.
        More advanced checks (paths, content sizes) are best-effort here.
        """
        perms = self.policy.get('permissions', {}) if isinstance(self.policy, dict) else {}
        if not isinstance(perms, dict):
            return False, 'Invalid policy format'

        # map action_type directly to permission keys where possible
        entry = perms.get(action_type)
        if entry is None:
            # unknown action types are denied by default
            return False, f'Unknown action type: {action_type}'

        allowed = bool(entry.get('allowed', False))
        if not allowed:
            return False, f'{action_type} non consentito dalla policy'

        # For api_call, we could check command/target; for now allow if flagged
        return True, 'ok'


def audit(policy: Dict[str, Any], action_type: str, sender: str, allowed: bool, reason: str) -> None:
    """Append an audit record to `logs/audit.log` (best-effort).

    This is intentionally simple to avoid raising in tests.
    """
    try:
        root = Path(__file__).parent
        logs_dir = root / 'logs'
        logs_dir.mkdir(parents=True, exist_ok=True)
        log_file = logs_dir / 'audit.log'
        ts = datetime.utcnow().isoformat() + 'Z'
        rec = f"{ts} action={action_type} sender={sender} allowed={allowed} reason={reason}\n"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(rec)
    except Exception:
        # swallow errors to avoid breaking agent execution
        pass
