"""Factory utilities to generate a custom agent skeleton on disk.

This module uses the existing tools.files helpers to create a
minimal, sellable agent package inside the `agents/` directory.
"""
from pathlib import Path
from typing import Dict, List, Tuple, Optional

from tools.files import write_file


AGENTS_ROOT = Path(__file__).resolve().parent.parent / "agents"


def _parse_files_plan(plan_text: str) -> List[Tuple[str, str]]:
    """Parse a simple plaintext plan into (relative_path, description).

    Expected loose format, for example lines like:
        agents/support/agent_prompt.txt - prompt di sistema
        config_support.py - configurazione modello

    Everything before the first "-" is treated as path, the rest as description.
    Lines without "-" are ignored.
    """
    results: List[Tuple[str, str]] = []
    for raw_line in plan_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "-" not in line:
            continue
        path_part, desc_part = line.split("-", 1)
        rel_path = path_part.strip()
        description = desc_part.strip()
        if not rel_path:
            continue
        results.append((rel_path, description))
    return results


def create_agent_package(spec: Dict[str, str], files_plan: Optional[str] = None) -> str:
    """Create a minimal custom agent package.

    Expected keys in `spec`:
    - name: machine-friendly name (e.g. "supporto_clienti")
    - title: human-friendly title
    - description: short description of the agent

    Returns the path to the created agent folder as string.
    """
    name = spec.get("name", "custom_agent").strip().replace(" ", "_")
    title = spec.get("title", name)
    description = spec.get("description", "Agente custom generato da SuperAgent.")

    agent_dir = AGENTS_ROOT / name
    agent_dir.mkdir(parents=True, exist_ok=True)

    # Basic agent file
    agent_py = f'''"""Custom agent: {title}

This module defines a simple wrapper class around SuperAgent
specialized for: {description}
"""
from agent import SuperAgent


class CustomAgent(SuperAgent):
    """Agente custom generato automaticamente."""

    def __init__(self, tools: dict):
        super().__init__(tools, name="{title}")
'''
    write_file(str(agent_dir / "agent_custom.py"), agent_py)

    # Runner
    run_py = f'''"""Runner for custom agent: {title}"""
from agent import SuperAgent
from tools import shell, files, browser

TOOLS = {{
    'shell': shell.run,
    'files_write': files.write_file,
    'files_read': files.read_file,
    'list_dir': files.list_dir,
    'browser': browser.fetch,
}}


def main():
    agent = SuperAgent(TOOLS, name="{title}")
    print("Agente custom pronto. Integrazione specifica da completare.")


if __name__ == '__main__':
    main()
'''
    write_file(str(agent_dir / "run_custom.py"), run_py)

    # Minimal README
    readme = f'''# {title}

{description}

Generato automaticamente dal framework SuperAgent.

## Uso rapido

```bash
python run_custom.py
```
'''
    write_file(str(agent_dir / "README.md"), readme)

    # Optional: interpret files_plan and create extra files relative to agent_dir
    if files_plan:
        extra_files = _parse_files_plan(files_plan)
        for rel_path, desc in extra_files:
            try:
                extra_path = agent_dir / rel_path
                extra_path.parent.mkdir(parents=True, exist_ok=True)
                # Very simple default content; the description is embedded as comment/text
                if str(extra_path).endswith(".py"):
                    content = (
                        "\"\"\"File generato automaticamente.\n\n"
                        f"Descrizione: {desc}\n"
                        "\"\"\"\n"
                    )
                else:
                    content = f"File generato automaticamente.\nDescrizione: {desc}\n"
                write_file(str(extra_path), content)
            except Exception:
                # Non bloccare la generazione del pacchetto per errori su singoli file
                continue

    return str(agent_dir)
