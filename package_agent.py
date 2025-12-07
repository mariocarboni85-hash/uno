"""Utility per impacchettare un agente generato in uno ZIP distribuibile.

Uso da PowerShell / terminale, dalla root del progetto:

    python package_agent.py supporto_clienti
    python package_agent.py devops_shell_sicuro

Lo ZIP verrà creato nella cartella `dist/`.
"""
import sys
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
AGENTS_DIR = ROOT / "agents"
DIST_DIR = ROOT / "dist"


def package_agent(agent_name: str) -> Path:
    agent_path = AGENTS_DIR / agent_name
    if not agent_path.exists() or not agent_path.is_dir():
        raise SystemExit(f"Agente non trovato: {agent_path}")

    DIST_DIR.mkdir(parents=True, exist_ok=True)

    zip_base = DIST_DIR / agent_name
    # shutil.make_archive aggiunge estensione .zip automaticamente
    archive_path = shutil.make_archive(str(zip_base), "zip", root_dir=AGENTS_DIR, base_dir=agent_name)
    return Path(archive_path)


def main(argv: list[str]) -> None:
    if len(argv) < 2:
        print("Uso: python package_agent.py <nome_agente>")
        print("Esempi: supporto_clienti, devops_shell_sicuro")
        raise SystemExit(1)

    agent_name = argv[1]
    archive = package_agent(agent_name)
    print(f"Creato pacchetto: {archive}")


if __name__ == "__main__":
    main(sys.argv)
