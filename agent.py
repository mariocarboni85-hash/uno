"""Module `agent` — classe `uno` (pulita e con metodi richiesti).

Questa versione fornisce implementazioni di base per i metodi richiesti
con comportamenti di fallback e docstring.
"""
from typing import Any, Dict, List, Optional
from pathlib import Path
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
        def __init__(self, max_actions: int = 5, max_shell: int = 0, max_write: int = 3):
            self.remaining_actions = int(max_actions)
            self.remaining_shell = int(max_shell)
            self.remaining_write = int(max_write)

        def consume(self, action_type: str) -> None:
            if self.remaining_actions <= 0:
                raise RuntimeError("Budget azioni esaurito")

            if action_type == "shell":
                if self.remaining_shell <= 0:
                    raise RuntimeError("Budget shell esaurito")
                self.remaining_shell -= 1

            if action_type == "file_write":
                if self.remaining_write <= 0:
                    raise RuntimeError("Budget write esaurito")
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
        # Normalize plan: only Action objects from here on
        plan: List[Action] = []
        for item in raw_plan:
            try:
                plan.append(self.ActionNormalizer.normalize(item))
            except Exception:
                # skip invalid entries
                continue
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
                max_shell_val = 0
                max_write_val = 3
        except Exception:
            max_actions_val = max_steps or 5
            max_shell_val = 0
            max_write_val = 3
        self._budget = self.ActionBudget(max_actions_val, max_shell_val, max_write_val)
        while plan and steps < max_steps:
            action = self.brain.select_action(plan)
            if not action:
                break
            # Delegate full processing to execute_action
            try:
                if isinstance(action, dict):
                    action = self.ActionNormalizer.normalize(action)
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

    def ask(self, prompt: str) -> Any:
        """Interroga il processo di pensiero interno e gestisce eventuali azioni."""
        resp = think(prompt)
        if isinstance(resp, str) and resp.startswith("ACTION:"):
            return self.handle_action(resp)
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
        try:
            pol = getattr(self, 'policy', None) or getattr(_uno_policy, 'VitPolicy', None)
            if pol:
                mode = self.config.get('mode') or pol.policy.get('modes', {}).get('default')
                cmd = args.get('cmd') if isinstance(args, dict) else None
                allowed, reason = pol.check(action_type, sender=sender or 'unknown', mode=mode, command=cmd)
                if not allowed:
                    try:
                        from uno import policy as _uno_policy
                        if _uno_policy:
                            _uno_policy.audit(pol.policy, action_type, sender or 'unknown', False, reason)
                    except Exception:
                        pass
                    return f"Policy denied: {reason}"
        except Exception:
            return "Policy evaluation error"

        # Budget
        try:
            if not self._budget:
                raise RuntimeError('Budget not initialized')
            self._budget.consume(action_type)
        except Exception as e:
            return f"Budget exceeded: {e}"

        # Execute
        tool = self.tools.get(action_type)
        if tool is None:
            return f"Tool {action_type} not found"
        try:
            if callable(tool):
                res = tool(**args)
            else:
                res = tool
            # Audit success
            try:
                pol = getattr(self, 'policy', None) or getattr(_uno_policy, 'VitPolicy', None)
                if pol:
                    from uno import policy as _uno_policy
                    if _uno_policy:
                        _uno_policy.audit(pol.policy, action_type, sender or 'unknown', True, 'executed')
            except Exception:
                pass
            return res
        except Exception as e:
            return f"Execution error: {e}"

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
