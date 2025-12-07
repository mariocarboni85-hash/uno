def create_plan(goal):
    """
    Crea un piano multi-step per raggiungere un obiettivo.
    goal: string
    """
    # Mock: suddivide il goal in 3 step
    steps = [f"Step {i+1} per {goal}" for i in range(3)]
    return {'goal': goal, 'steps': steps, 'status': ['pending']*3}
"""Planner: creates a trivial plan from a text goal."""

def _split_goal_to_steps(goal: str) -> list:
    # Very naive split: use commas or split into words groups
    if ',' in goal:
        return [s.strip() for s in goal.split(',') if s.strip()]
    return [goal]


class Planner:
    def create_plan(self, goal: str) -> list:
        """Return a list of step dicts. Each step: {verb, tool, args}.
        This is a simple heuristic-based planner.
        """
        raw_steps = _split_goal_to_steps(goal)
        plan = []
        for step in raw_steps:
            # simple heuristics
            low = step.lower()
            if 'create' in low or 'write' in low or 'file' in low:
                plan.append({
                    'verb': 'write_file',
                    'tool': 'files_write',
                    'args': {'path': 'output/hello.txt', 'content': 'Hello from SuperAgent!'}
                })
            elif 'run' in low or 'execute' in low or 'command' in low:
                plan.append({
                    'verb': 'run_shell',
                    'tool': 'shell',
                    'args': {'cmd': 'echo Hello from shell'}
                })
            elif 'list' in low or 'dir' in low:
                plan.append({
                    'verb': 'list_dir',
                    'tool': 'list_dir',
                    'args': {'path': '.'}
                })
            else:
                # fallback: attempt a fetch
                plan.append({
                    'verb': 'fetch',
                    'tool': 'browser',
                    'args': {'url': low}
                })
        return plan

    def plan_description(self, task: str) -> str:
        """Return a textual description of the planning process."""
        return f"""Per completare questo compito seguirò i seguenti step:
1. Analisi del task
2. Selezione dei tool appropriati
3. Esecuzione sequenziale
4. Risposta finale

Task: {task}"""
