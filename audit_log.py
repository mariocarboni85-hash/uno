import json
import hashlib
from datetime import datetime
from pathlib import Path

class AuditLog:
    def __init__(self, path="./logs/audit.log"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.last_hash = self._load_last_hash()

    def _load_last_hash(self):
        if not self.path.exists():
            return "GENESIS"
        last = self.path.read_text().strip().splitlines()[-1]
        try:
            return json.loads(last)["hash"]
        except Exception:
            return "GENESIS"

    def _hash(self, payload):
        return hashlib.sha256(payload.encode()).hexdigest()

    def append(self, record: dict):
        record["timestamp"] = datetime.utcnow().isoformat()
        record["prev_hash"] = self.last_hash

        raw = json.dumps(record, sort_keys=True)
        record["hash"] = self._hash(raw)

        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

        self.last_hash = record["hash"]

    def verify(self, path: str = None) -> dict:
        """Verify the integrity of the audit log.

        Returns a dict with keys:
          - valid: bool
          - issues: list of strings describing problems
        If `path` is provided, verifies that file; otherwise verifies self.path.
        """
        target = Path(path) if path else self.path
        issues = []
        if not target.exists():
            return {"valid": True, "issues": []}

        prev_hash = "GENESIS"
        for idx, line in enumerate(target.read_text(encoding='utf-8').splitlines()):
            try:
                rec = json.loads(line)
            except Exception:
                issues.append(f"line {idx+1}: invalid json")
                continue

            stored_hash = rec.get('hash')
            # recompute expected hash: remove 'hash' then dump with sort_keys
            rec_copy = dict(rec)
            rec_copy.pop('hash', None)
            raw = json.dumps(rec_copy, sort_keys=True)
            expected_hash = hashlib.sha256(raw.encode()).hexdigest()

            if stored_hash != expected_hash:
                issues.append(f"line {idx+1}: hash mismatch (stored={stored_hash} expected={expected_hash})")

            if idx == 0:
                if rec.get('prev_hash') != 'GENESIS':
                    issues.append(f"line {idx+1}: prev_hash should be GENESIS")
            else:
                if rec.get('prev_hash') != prev_hash:
                    issues.append(f"line {idx+1}: prev_hash mismatch (stored={rec.get('prev_hash')} expected={prev_hash})")

            prev_hash = stored_hash

        return {"valid": len(issues) == 0, "issues": issues}
