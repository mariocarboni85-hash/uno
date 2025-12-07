import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], description: str) -> int:
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

    total_errors += run(
        [python_exe, run_super, "status"],
        "Verifica stato Super Agent",
    )

    total_errors += run(
        [python_exe, run_super, "auto", "analizza e migliora"],
        "Esecuzione automatica 'analizza e migliora'",
    )

    demo_file = repo_root / "demo_collaborative_learning.py"
    if demo_file.exists():
        total_errors += run(
            [python_exe, run_super, "analizza", "--file", str(demo_file)],
            "Analisi del file demo_collaborative_learning.py",
        )

    total_errors += run(
        [python_exe, run_super, "demo", "basic"],
        "Esecuzione demo di apprendimento collaborativo (basic)",
    )

    if total_errors == 0:
        print("\n>>> SELFTEST SUPER AGENT: TUTTO OK (senza pytest) <<<")
    else:
        print(f"\n>>> SELFTEST SUPER AGENT: COMPLETATO CON {total_errors} ERRORI (vedi sopra) <<<")


if __name__ == "__main__":
    main()
