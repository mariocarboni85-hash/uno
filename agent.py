"""Module `agent` — classe `uno` (pulita e con metodi richiesti).

Questa versione fornisce implementazioni di base per i metodi richiesti
con comportamenti di fallback e docstring.
"""
from typing import Any, Dict, List, Optional
from pathlib import Path
import json
import ast
from uno.action import Action

try:
    from core.planner import Planner
except Exception:
    class Planner:
        def create_plan(self, goal: str):
            return [f"do:{goal}"]

try:
    from core.brain import Brain, think
except Exception:
    class Brain:
        def select_action(self, plan: List[Dict[str, Any]]):
            if not plan:
                return None
            # simple mock action
            return {"verb": "run", "tool": "shell", "args": {"cmd": plan[0]}}

    def think(prompt: str) -> str:
        return f"[THINK] {prompt}"

try:
    from tools.shell import run as run_shell
except Exception:
    def run_shell(cmd: str):
        return f"(mock) executed: {cmd}"

try:
    from tools.files import read_file, write_file
except Exception:
    def read_file(path: str):
        return f"(mock) read {path}"

    def write_file(path: str, content: str):
        return f"(mock) wrote {len(content)} bytes to {path}"

try:
    # optional policy module
    from uno import policy as _uno_policy
except Exception:
    _uno_policy = None

try:
    from uno.actions import ActionNormalizer as ExternalActionNormalizer  # type: ignore
except Exception:
    ExternalActionNormalizer = None

try:
    from uno.tool_executor import ToolExecutor
except Exception:
    ToolExecutor = None
try:
    from uno.policy_engine import PolicyEngine, PolicyViolation
except Exception:
    PolicyEngine = None
    PolicyViolation = Exception


class uno:
    """Agente `uno` con metodi principali richiesti.

    Metodi implementati:
    - __init__, run, ask, handle_action, send_message,
      _verifica_veridicita_per_vit, pensa, super_meta_ragionamento_evolutivo,
      federated_learn, federated_learn_multi, evolve_to_super_meta_asi
    """

    def __init__(self, tools: Optional[Dict[str, Any]] = None, name: str = "uno", config: Optional[Dict[str, Any]] = None, policy: Optional[Any] = None):
        self.name = name
        self.tools = tools or {}
        self.config = config or {}
        # optional policy object (uno.policy.Policy)
        self.policy = policy
        self.planner = Planner()
        self.brain = Brain()
        self.inbox = None
        self.strategy = getattr(self, "strategy", "default")
        self.experience = getattr(self, "experience", 0)
        # budget helper (per-run)
        self._budget = None

    # ---- Action Normalizer & Budget ----
    # Delegate normalisation to `uno.actions.ActionNormalizer`
    class ActionNormalizer:
        @staticmethod
        def normalize(item: Any) -> Action:
            if isinstance(item, Action):
                return item
            if isinstance(item, dict):
                if ExternalActionNormalizer:
                    return ExternalActionNormalizer.normalize(item)
                # fallback inline behaviour
                typ = item.get('type') or item.get('tool') or item.get('verb')
                payload = item.get('payload') or item.get('args') or {}
                sender = item.get('sender') or item.get('from') or 'vit'
                mode = item.get('mode') or 'restricted'
                return Action(type=str(typ), payload=dict(payload), sender=str(sender), mode=str(mode))
            raise TypeError('Unsupported plan item type; expected dict or Action')

    class ActionBudget:
        """Simple per-run budget to avoid runaway loops.

        Uses a max_actions cap (default 20) which can be overridden via policy.
        """
        def __init__(self, max_actions=5, max_shell=0, max_write=3):
            self.remaining_actions = max_actions
            self.remaining_shell = max_shell
            self.remaining_write = max_write

        def consume(self, action_type: str):
            if self.remaining_actions <= 0:
                raise RuntimeError("Budget azioni esaurito")

            if action_type == "shell":
                if self.remaining_shell <= 0:
                    raise RuntimeError("Shell non consentita")
                self.remaining_shell -= 1

            if action_type == "file_write":
                if self.remaining_write <= 0:
                    raise RuntimeError("Scrittura non consentita")
                self.remaining_write -= 1

            self.remaining_actions -= 1

        def remaining(self) -> Dict[str, int]:
            return {
                'actions': self.remaining_actions,
                'shell': self.remaining_shell,
                'write': self.remaining_write,
            }

    def run(self, goal: str, max_steps: int = 5) -> None:
        """Esegue un semplice ciclo: crea piano, seleziona e lancia azioni."""
        raw_plan = self.planner.create_plan(goal)
        # Keep raw_plan as produced by the planner; brain.select_action
        # expects to receive planner items (strings or dicts).
        plan = raw_plan
        steps = 0
        # budget: prefer policy rate_limit if present
        pol = getattr(self, 'policy', None)
        max_actions = None
        try:
            if pol:
                max_actions = pol.policy.get('security', {}).get('rate_limit', {}).get('max_actions_per_minute')
        except Exception:
            max_actions = None
        # derive budget limits from policy if available
        try:
            if pol:
                ra = pol.policy.get('security', {}).get('rate_limit', {}).get('max_actions_per_minute')
                max_actions_val = int(ra) if ra is not None else (max_steps or 5)
                max_shell_val = pol.policy.get('budget', {}).get('max_shell', 0)
                max_write_val = pol.policy.get('budget', {}).get('max_write', 3)
            else:
                max_actions_val = max_steps or 5
                # Allow shell by default when no policy is present
                max_shell_val = 1
                max_write_val = 3
        except Exception:
            max_actions_val = max_steps or 5
            max_shell_val = 0
            max_write_val = 3
        self._budget = self.ActionBudget(max_actions_val, max_shell_val, max_write_val)
        while plan and steps < max_steps:
            raw_action = self.brain.select_action(plan)
            if not raw_action:
                break
            # Normalize the raw action (handles dicts and Action instances)
            try:
                action = self.ActionNormalizer.normalize(raw_action)
                if not isinstance(action, Action):
                    break
            except Exception:
                break

            try:
                result = self.execute_action(action, sender='vit')
                print('action result:', result)
            except Exception as e:
                print('Errore execute_action:', e)
                break

            plan = plan[1:]
            steps += 1

    def run_with_context(self, goal: str, vit_context: Dict[str, Any]) -> None:
        """Run loop that consumes an explicit `vit_context` budget.

        vit_context: {
            'budget': {'max_actions': int, 'max_shell': int, 'max_write': int}
        }
        This method mirrors the proposed pseudocode: it normalizes selected
        actions, consumes the budget, executes via `execute_action` and
        allows the plan to be updated with results when applicable.
        """
        bcfg = vit_context.get('budget', {}) if isinstance(vit_context, dict) else {}
        max_actions = bcfg.get('max_actions', 5)
        max_shell = bcfg.get('max_shell', 0)
        max_write = bcfg.get('max_write', 3)

        budget = self.ActionBudget(max_actions=max_actions, max_shell=max_shell, max_write=max_write)

        plan = self.planner.create_plan(goal)
        # normalize initial plan items to Actions where possible
        normalized_plan: List[Action] = []
        for item in plan:
            try:
                normalized_plan.append(self.ActionNormalizer.normalize(item))
            except Exception:
                continue

        while True:
            raw_action = self.brain.select_action(normalized_plan)

            if raw_action is None:
                break

            try:
                action = self.ActionNormalizer.normalize(raw_action)
            except Exception:
                break

            # consume budget based on action.type
            try:
                budget.consume(getattr(action, 'type', None))
            except Exception as e:
                # budget exhausted or disallowed
                return

            # execute action using existing pipeline
            result = self.execute_action(action, sender=getattr(action, 'sender', 'vit'))

            # allow plan to be updated if result provides updates (best-effort)
            try:
                if isinstance(result, dict) and hasattr(normalized_plan, 'update'):
                    # if plan supports update (unlikely for list), try it
                    normalized_plan.update(result)  # type: ignore
            except Exception:
                pass

            # remove first element of plan if present
            if normalized_plan:
                normalized_plan = normalized_plan[1:]

    def run_with_vit(self, goal: str, vit_context: Dict[str, Any]) -> None:
        """Run using explicit vit_context with AuditLog + PolicyEngine + ActionBudget + ToolExecutor.

        Signature: run_with_vit(goal, vit_context)
        vit_context: { 'policy': <path_or_none>, 'budget': {'max_actions':..,'max_shell':..,'max_write':..} }
        """
        from dataclasses import asdict
        # prepare policy engine
        policy_engine = None
        try:
            if PolicyEngine and isinstance(vit_context, dict) and vit_context.get('policy'):
                try:
                    policy_engine = PolicyEngine(vit_context.get('policy'))
                except Exception:
                    policy_engine = PolicyEngine()
        except Exception:
            policy_engine = None

        # budget
        bcfg = vit_context.get('budget', {}) if isinstance(vit_context, dict) else {}
        try:
            budget = self.ActionBudget(
                max_actions=bcfg.get('max_actions', 5),
                max_shell=bcfg.get('max_shell', 0),
                max_write=bcfg.get('max_write', 3),
            )
        except Exception:
            budget = self.ActionBudget()

        # audit log
        try:
            from uno.audit_log import AuditLog
            audit = AuditLog()
        except Exception:
            audit = None

        plan = self.planner.create_plan(goal)

        while plan:
            raw_action = self.brain.select_action(plan)
            if raw_action is None:
                break

            try:
                action = self.ActionNormalizer.normalize(raw_action)
            except Exception:
                break

            # policy authorize
            try:
                if policy_engine:
                    policy_engine.authorize(action)
            except Exception as e:
                # audit denial if possible
                if audit:
                    try:
                        audit.append({
                            'phase': 'intent',
                            'agent': self.name,
                            'action': asdict(action),
                            'authorized_by': 'vit',
                            'allowed': False,
                            'reason': str(e),
                        })
                    except Exception:
                        pass
                return

            # budget consume
            try:
                budget.consume(action.type)
            except Exception as e:
                if audit:
                    try:
                        audit.append({
                            'phase': 'intent',
                            'agent': self.name,
                            'action': asdict(action),
                            'authorized_by': 'vit',
                            'allowed': False,
                            'reason': str(e),
                        })
                    except Exception:
                        pass
                return

            # audit intent
            if audit:
                try:
                    audit.append({
                        'phase': 'intent',
                        'agent': self.name,
                        'action': asdict(action),
                        'authorized_by': 'vit',
                    })
                except Exception:
                    pass

            # execute
            try:
                if ToolExecutor:
                    res = ToolExecutor.execute(action, self.tools, audit_fn=(getattr(self, 'policy', None) and getattr(__import__('uno.policy', fromlist=['audit']), 'audit')))
                else:
                    # fallback to existing execute_action
                    res = self.execute_action(action, sender=action.sender)
                status = 'success'
            except Exception as e:
                res = str(e)
                status = 'error'

            # audit result
            if audit:
                try:
                    audit.append({
                        'phase': 'result',
                        'agent': self.name,
                        'action': asdict(action),
                        'status': status,
                        'result': res,
                    })
                except Exception:
                    pass

            # update plan
            try:
                if isinstance(res, dict) and 'plan' in res:
                    plan = res['plan']
                elif hasattr(plan, 'update'):
                    try:
                        plan.update(res)  # type: ignore
                    except Exception:
                        plan = plan[1:]
                else:
                    if plan:
                        plan = plan[1:]
            except Exception:
                if plan:
                    plan = plan[1:]

        def run_with_vit_context(self, goal: str, vit_context: Dict[str, Any]) -> None:
            """Run loop driven by explicit vit_context (policy + budget).

            vit_context expected shape:
            {
                'policy': '<path-to-policy-yaml>' or None,
                'budget': {'max_actions': int, 'max_shell': int, 'max_write': int}
            }
            """
            # Prepare policy engine
            policy_path = None
            try:
                policy_path = vit_context.get('policy') if isinstance(vit_context, dict) else None
            except Exception:
                policy_path = None

            policy_engine = None
            if PolicyEngine:
                try:
                    policy_engine = PolicyEngine(policy_path)
                except Exception:
                    policy_engine = None

            # Budget
            bcfg = vit_context.get('budget', {}) if isinstance(vit_context, dict) else {}
            budget = self.ActionBudget(
                max_actions=bcfg.get('max_actions', 5),
                max_shell=bcfg.get('max_shell', 0),
                max_write=bcfg.get('max_write', 3),
            )

            plan = self.planner.create_plan(goal)

            while plan:
                raw_action = self.brain.select_action(plan)
                if raw_action is None:
                    break

                try:
                    action = self.ActionNormalizer.normalize(raw_action)
                except Exception:
                    # Can't normalize -> skip
                    break

                # Policy authorize (vit is final authority)
                if policy_engine:
                    try:
                        policy_engine.authorize(action)
                    except PolicyViolation as pv:
                        # audit denial if possible
                        try:
                            from uno import policy as _uno_policy
                            if _uno_policy:
                                _uno_policy.audit(policy_engine.policy, action.type, action.sender, False, str(pv))
                        except Exception:
                            pass
                        return

                # Budget consume
                try:
                    budget.consume(action.type)
                except Exception:
                    return

                # Execute via tool executor
                try:
                    if ToolExecutor:
                        res = ToolExecutor.execute(action, self.tools, audit_fn=(getattr(__import__('uno.policy', fromlist=['audit']), 'audit') if hasattr(__import__('uno.policy', fromlist=['audit']), 'audit') else None))
                    else:
                        # fallback to execute_action (which applies policy/budget again)
                        res = self.execute_action(action, sender=action.sender)
                except Exception:
                    # execution failure -> stop
                    return

                # Allow plan to be updated from result if applicable
                try:
                    if isinstance(res, dict) and hasattr(plan, 'update'):
                        plan.update(res)  # type: ignore
                    elif isinstance(res, dict) and 'plan' in res:
                        plan = res['plan']
                    else:
                        # advance plan
                        if plan:
                            plan = plan[1:]
                except Exception:
                    if plan:
                        plan = plan[1:]

    def ask(self, prompt: str) -> Any:
        """Interroga il processo di pensiero interno e gestisce eventuali azioni."""
        resp = think(prompt)
        if isinstance(resp, str) and resp.startswith("ACTION:"):
            # Expect the thinker to return a JSON or Python-literal after the prefix
            raw = resp[len("ACTION:"):].strip()
            raw_action = None
            if not raw:
                return "Malformed ACTION: empty payload"
            # Try JSON first
            try:
                raw_action = json.loads(raw)
            except Exception:
                try:
                    raw_action = ast.literal_eval(raw)
                except Exception:
                    return "Malformed ACTION: payload not JSON or Python literal"

            try:
                return self.execute_action(raw_action, sender='vit')
            except Exception as e:
                return f"Action execution error: {e}"
        return resp

    def handle_action(self, action: str, sender: Optional[str] = None) -> Any:
        """Interpreta comandi di tipo ACTION: e delega a helper semplici.

        Protegge l'esecuzione di comandi shell: solo il mittente `vit` può
        richiedere esecuzione shell remota.
        """
        raise RuntimeError("handle_action disabilitato: usare Action strutturate")

    def execute_action(self, raw_action: Any, sender: Optional[str] = None) -> Any:
        """Central execution pipeline: normalize -> policy.check -> budget.consume -> execute -> audit."""
        # Normalize
        try:
            action = raw_action if isinstance(raw_action, Action) else self.ActionNormalizer.normalize(raw_action)
        except Exception as e:
            return f"Normalization error: {e}"

        sender = sender or getattr(action, 'sender', 'unknown')
        action_type = getattr(action, 'type', None)
        args = getattr(action, 'payload', {}) or {}

        # Policy check
        # Policy authorization: prefer attached VitPolicy if present
        try:
            pol = getattr(self, 'policy', None)
            if pol:
                mode = self.config.get('mode') or pol.policy.get('modes', {}).get('default')
                cmd = args.get('cmd') if isinstance(args, dict) else None
                allowed, reason = pol.check(action_type, sender=sender or 'unknown', mode=mode, command=cmd)
                if not allowed:
                    try:
                        from uno import policy as _uno_policy
                        if _uno_policy:
                            _uno_policy.audit(pol.policy if getattr(pol, 'policy', None) else {}, action_type, sender or 'unknown', False, reason)
                    except Exception:
                        pass
                    return f"Policy denied: {reason}"
            else:
                # no attached policy: do not apply bundled PolicyEngine implicitly
                pass
        except Exception as e:
            return f"Policy evaluation error: {e}"

        # Budget consumption
        try:
            if not self._budget:
                raise RuntimeError('Budget not initialized')
            self._budget.consume(action_type)
        except Exception as e:
            return f"Budget exceeded: {e}"

        # Audit BEFORE execution (attempt)
        try:
            try:
                from uno import policy as _uno_policy
            except Exception:
                _uno_policy = None
            policy_dict = getattr(self, 'policy').policy if getattr(self, 'policy', None) and getattr(self, 'policy', None).policy else {}
            if _uno_policy:
                try:
                    _uno_policy.audit(policy_dict, action_type, sender or 'unknown', True, 'attempt')
                except Exception:
                    pass
        except Exception:
            pass

        # Execute via ToolExecutor if available (pass audit fn for AFTER)
        try:
            def _after_audit(policy_obj, a_type, a_sender, allowed, reason, **meta):
                try:
                    from uno import policy as _uno_policy
                    policy_dict_local = getattr(self, 'policy').policy if getattr(self, 'policy', None) and getattr(self, 'policy', None).policy else {}
                    if _uno_policy:
                        try:
                            # include budget snapshot when available
                            if hasattr(self, '_budget') and getattr(self, '_budget'):
                                meta.setdefault('budget', getattr(self, '_budget').remaining())
                            _uno_policy.audit(policy_dict_local, a_type, a_sender or 'unknown', allowed, reason, **meta)
                        except Exception:
                            pass
                except Exception:
                    pass

            if ToolExecutor:
                try:
                    return ToolExecutor.execute(action, self.tools, audit_fn=_after_audit)
                except Exception as e:
                    # ensure after-audit records failure
                    try:
                        _after_audit(None, action_type, sender or 'unknown', False, str(e))
                    except Exception:
                        pass
                    return f"Execution error: {e}"

            # Fallback behaviour if ToolExecutor not present
            tool = self.tools.get(action_type)
            if tool is None:
                # after-audit failure
                try:
                    _after_audit(None, action_type, sender or 'unknown', False, 'tool not found')
                except Exception:
                    pass
                return f"Tool {action_type} not found"
            try:
                if callable(tool):
                    res = tool(**args)
                else:
                    res = tool
                # after-audit success
                try:
                    _after_audit(None, action_type, sender or 'unknown', True, 'executed')
                except Exception:
                    pass
                return res
            except Exception as e:
                try:
                    _after_audit(None, action_type, sender or 'unknown', False, str(e))
                except Exception:
                    pass
                return f"Execution error: {e}"
        except Exception:
            return "Execution pipeline error"

    def _verifica_veridicita_per_vit(self, recipient: Any, message: str) -> bool:
        """Controllo semplificato della veridicità per messaggi destinati a `vit`."""
        if getattr(recipient, "name", recipient) == 'vit' or recipient == 'vit':
            if isinstance(message, str) and message.strip().lower().startswith('bugia'):
                return False
        return True


# Compatibility shim for existing tests and older code that expect `SuperAgent`
class SuperAgent(uno):
    """Backward-compatible alias for historical test-suite expecting `SuperAgent`.

    Use this class in tests that import `SuperAgent` from `uno.agent`.
    """
    pass

    def send_message(self, recipient: Any, message: str) -> str:
        """Invia un messaggio a `recipient` se autorizzato."""
        if (getattr(recipient, "name", recipient) == 'vit' or recipient == 'vit') and not self._verifica_veridicita_per_vit(recipient, message):
            return "Invio negato: veridicità non verificata"
        # prova a mettere nel .inbox se presente
        if hasattr(recipient, 'inbox') and hasattr(recipient.inbox, 'put'):
            try:
                recipient.inbox.put(message)
                return f"Messaggio inviato a {getattr(recipient, 'name', str(recipient))}"
            except Exception:
                return "Errore invio messaggio: inbox non disponibile"
        return "Destinatario non raggiungibile"

    def pensa(self, input_data: Any, tipo: str = 'cognitivo') -> str:
        """Semplice emulazione di diversi stili di pensiero."""
        s = str(input_data)
        if tipo == 'creativo':
            return f"[creativo] nuova idea da '{s}' -> '{s[::-1]}'"
        if tipo == 'realistico':
            return f"[realistico] analisi di '{s}' -> '{s.lower()}'"
        if tipo == 'analitico':
            return f"[analitico] componenti: {list(s)}"
        return f"[cognitivo] riflessione: {s.upper()}"

    def super_meta_ragionamento_evolutivo(self, feedback: Optional[str] = None, contesto: Optional[Dict[str, Any]] = None, risultati: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        out: Dict[str, Any] = {}
        if feedback:
            out['feedback'] = feedback
        if contesto:
            out['contesto'] = contesto
        if risultati:
            out['risultati'] = risultati
        if feedback and 'negativo' in feedback.lower():
            out['azione'] = 'cambia_strategia'
        elif feedback and 'positivo' in feedback.lower():
            out['azione'] = 'mantieni'
        else:
            out['azione'] = 'analisi_completata'
        return out

    def federated_learn(self, altro_asi: Any, sender: Optional[str] = None) -> str:
        if sender != 'vit':
            return 'Solo vit può ordinare federated learning.'
        if hasattr(altro_asi, 'experience') and getattr(altro_asi, 'experience', 0) > getattr(self, 'experience', 0):
            self.strategy = getattr(altro_asi, 'strategy', self.strategy)
            return f"Strategia aggiornata: {self.strategy}"
        return 'Federated learning completato.'

    def federated_learn_multi(self, altri_asi: List[Any], sender: Optional[str] = None) -> str:
        if sender != 'vit':
            return 'Solo vit può ordinare federated learning multi-ecosistema.'
        aggiornata = False
        for altro in altri_asi:
            if getattr(altro, 'experience', 0) > getattr(self, 'experience', 0):
                self.strategy = getattr(altro, 'strategy', self.strategy)
                aggiornata = True
        if aggiornata:
            return f"Strategia aggiornata tramite federated multi: {self.strategy}"
        return 'Federated learning multi-ecosistema completato.'

    def evolve_to_super_meta_asi(self, sender: Optional[str] = None) -> Any:
        if sender != 'vit':
            return 'Solo vit può ordinare questa evoluzione.'
        try:
            from uno.agent_hierarchy import SuperMetaASI

            return SuperMetaASI(self.name, superiore='vit')
        except Exception:
            return 'SuperMetaASI non disponibile in questo ambiente'


class SuperAgent(uno):
    """Alias compatibilità"""


if __name__ == '__main__':
    # If an examples runner is available, prefer running it.
    try:
        from uno.examples import run_agent_demo
        run_agent_demo.main()
    except Exception:
        a = SuperAgent()
        print(a.pensa('ciao mondo', tipo='creativo'))
        print(a.super_meta_ragionamento_evolutivo('feedback positivo'))
