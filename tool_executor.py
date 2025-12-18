from typing import Any, Dict, Optional
from uno.action import Action

def _safe_call(tool, payload: Dict[str, Any]):
    if callable(tool):
        # pass payload as kwargs if it's a dict, else pass as single arg
        if isinstance(payload, dict):
            return tool(**payload)
        return tool(payload)
    return tool


class ToolExecutor:
    @staticmethod
    def execute(action: Action, tools: Dict[str, Any], audit_fn: Optional[callable] = None) -> Any:
        """Execute the given Action using provided tools dict.

        Calls `audit_fn(policy, action_type, sender, allowed, reason)` when provided
        after execution to record success/failure. Returns the tool result or
        raises if execution fails.
        """
        action_type = getattr(action, 'type', None)
        sender = getattr(action, 'sender', 'unknown')
        payload = getattr(action, 'payload', {}) or {}

        tool = None
        if isinstance(tools, dict):
            tool = tools.get(action_type)

        try:
            if tool is None:
                # No tool provided; raise to let caller handle
                raise RuntimeError(f"Tool {action_type} not found")
            res = _safe_call(tool, payload)
            if audit_fn:
                try:
                    audit_fn(None, action_type, sender or 'unknown', True, 'executed', payload=payload)
                except Exception:
                    pass
            return res
        except Exception as e:
            if audit_fn:
                try:
                    audit_fn(None, action_type, sender or 'unknown', False, str(e), payload=payload)
                except Exception:
                    pass
            raise
