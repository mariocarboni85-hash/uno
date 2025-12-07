"""SuperAgent: orchestrates planner, brain and tools.
File: agent.py
"""
from core.planner import Planner
from core.brain import Brain, think
from tools.shell import run_shell
from tools.files import read_file, write_file

class SuperAgent:
    def __init__(self, tools: dict | None = None, name: str = "SuperAgent", config: dict | None = None):
        self.name = name
        self.tools = tools or {}
        self.config = config or {}
        self.planner = Planner()
        self.brain = Brain()

    def run(self, goal: str, max_steps: int = 5):
        """Run a simple loop: create plan, pick next action, execute via tool."""
        plan = self.planner.create_plan(goal)
        steps_run = 0
        while plan and steps_run < max_steps:
            action = self.brain.select_action(plan)
            if not action:
                break
            verb = action.get("verb")
            args = action.get("args", {})
            tool = self.tools.get(action.get("tool"))
            if tool is None:
                print(f"Tool not found: {action.get('tool')}")
                break
            print(f"Executing action: {verb} with {tool.__name__ if hasattr(tool,'__name__') else tool}")
            try:
                result = tool(**args)
                print("Result:", result)
            except Exception as e:
                print("Error executing tool:", e)
                break
            # simple: remove the first plan step after execution
            plan.pop(0)
            steps_run += 1
        print("Run finished.")

    def handle_action(self, action):
        """Esegue i comandi generati dall'IA."""
        try:
            if action.startswith("ACTION:shell:"):
                cmd = action.replace("ACTION:shell:", "")
                return run_shell(cmd)

            if action.startswith("ACTION:read:"):
                path = action.replace("ACTION:read:", "").strip()
                return read_file(path)

            if action.startswith("ACTION:write:"):
                parts = action.split(":", 3)
                path = parts[2]
                content = parts[3]
                return write_file(path, content)

            return "Azione non riconosciuta."

        except Exception as e:
            return f"Errore: {str(e)}"

    def ask(self, prompt):
        """Ask a question to the agent and get a response."""
        response = think(prompt)

        if response.startswith("ACTION:"):
            return self.handle_action(response)

        return response


if __name__ == '__main__':
    # demo usage when executed directly
    from tools.shell import run
    from tools.files import write_file

    tools = {
        "shell": run,
        "files_write": write_file,
    }
    agent = SuperAgent(tools)
    agent.run("create a hello.txt file")
