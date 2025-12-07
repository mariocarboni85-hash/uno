import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from agent import SuperAgent
from tools.shell import run_shell
from tools.files import read_file, write_file, list_dir


TOOLS = {
    "shell": run_shell,
    "read_file": read_file,
    "write_file": write_file,
    "list_dir": list_dir,
}


def main():
    agent = SuperAgent(tools=TOOLS, name="analista_requisiti", config=None)
    print("Agente 'analista_requisiti' inizializzato. Integra questo runner nel tuo prodotto,")
    print("oppure usa sdk.loader.load_custom_agent('analista_requisiti') dalla root del progetto.")


if __name__ == "__main__":
    main()
