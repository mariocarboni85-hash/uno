from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import List


def run(cmd: List[str], description: str) -> int:
    print(f"\n=== {description} ===")
    print("Comando:", " ".join(cmd))
    proc = subprocess.run(cmd, text=True)
    print(f"-- Exit code: {proc.returncode}\n")
    return proc.returncode


def main() -> None:
    python_exe = sys.executable
    repo_root = Path(__file__).resolve().parent
    run_super = str(repo_root / "run_super_agent.py")

    total_errors = 0

    # 1) Check di base veloce
    total_errors += run(
        [python_exe, run_super, "status"],
        "Verifica stato Super Agent (FAST)",
    )

    # 2) Analisi di un solo file mirato
    demo_file = repo_root / "demo_collaborative_learning.py"
    if demo_file.exists():
        total_errors += run(
            [python_exe, run_super, "analizza", "--file", str(demo_file)],
            "Analisi rapida del file demo_collaborative_learning.py",
        )

    # 3) Una demo collaborativa semplice
    total_errors += run(
        [python_exe, run_super, "demo", "basic"],
        "Esecuzione demo collaborativa (basic, FAST)",
    )

    if total_errors == 0:
        print("\n>>> SELFTEST SUPER AGENT (FAST): TUTTO OK <<<")
    else:
        print(
            f"\n>>> SELFTEST SUPER AGENT (FAST): COMPLETATO CON {total_errors} ERRORI (vedi sopra) <<<"
        )


if __name__ == "__main__":
    main()
