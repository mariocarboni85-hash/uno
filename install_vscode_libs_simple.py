"""
VS Code Libraries Installation - Script semplificato
Installa librerie direttamente con pip nel venv attivo
"""

import subprocess
import sys
from pathlib import Path


# Librerie VS Code categorizzate
VSCODE_LIBRARIES = {
    "Editor & File Management": [
        "watchdog", "pathspec", "chardet", "python-magic-bin", "filetype"
    ],
    "Code Analysis & AST": [
        "astroid", "astor", "redbaron", "parso", "jedi", "rope"
    ],
    "Linting & Formatting": [
        "flake8", "autopep8", "isort", "pycodestyle", "pydocstyle",
        "bandit", "radon", "mccabe"
    ],
    "Git Integration": [
        "gitpython", "dulwich"
    ],
    "Documentation": [
        "sphinx", "pdoc3", "mkdocs", "mkdocs-material"
    ],
    "Testing Integration": [
        "pytest-watch", "pytest-cov", "pytest-xdist",
        "pytest-timeout", "pytest-mock"
    ],
    "Debugging & Profiling": [
        "ipdb", "pudb", "memory-profiler", "line-profiler"
    ],
    "Language Server Protocol": [
        "python-lsp-server", "pylsp-mypy", "python-lsp-black"
    ],
    "Terminal & Shell": [
        "prompt-toolkit", "colorama", "termcolor", "blessed"
    ],
    "File Formats": [
        "toml", "pyyaml", "python-dotenv", "jsonschema", "xmltodict"
    ],
    "Project Management": [
        "pip-tools", "pipdeptree", "safety"
    ],
    "Code Search & Navigation": [
        "pygments", "whoosh", "fuzzywuzzy", "python-levenshtein"
    ],
    "Workspace & Project": [
        "pyproject-hooks", "build", "setuptools-scm"
    ],
    "Extensions & Plugins": [
        "pluggy", "stevedore", "entrypoints"
    ],
    "Utils & Helpers": [
        "more-itertools", "toolz", "attrs", "cattrs", "boltons"
    ]
}


def install_library(lib_name, timeout=180):
    """Installa una singola libreria"""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", lib_name, "--quiet"],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode == 0, result.stderr
    except subprocess.TimeoutExpired:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)


def main():
    print("=" * 70)
    print("INSTALLAZIONE LIBRERIE VS CODE INTEGRATION")
    print("=" * 70)
    
    total_libs = sum(len(libs) for libs in VSCODE_LIBRARIES.values())
    print(f"\nTotale librerie da installare: {total_libs}")
    print(f"Python: {sys.executable}\n")
    
    all_results = {}
    total_success = 0
    total_failed = 0
    
    for category, libraries in VSCODE_LIBRARIES.items():
        print(f"\n{'='*70}")
        print(f"[{category}]")
        print(f"{'='*70}")
        
        results = {"success": [], "failed": []}
        
        for i, lib in enumerate(libraries, 1):
            print(f"[{i}/{len(libraries)}] {lib}...", end=" ", flush=True)
            
            success, error = install_library(lib)
            
            if success:
                print("OK")
                results["success"].append(lib)
                total_success += 1
            else:
                print(f"FAIL ({error[:50]})")
                results["failed"].append(lib)
                total_failed += 1
        
        all_results[category] = results
        
        # Riepilogo categoria
        print(f"\nRiepilogo: {len(results['success'])}/{len(libraries)} OK")
    
    # Riepilogo finale
    print("\n" + "=" * 70)
    print("RIEPILOGO FINALE")
    print("=" * 70)
    print(f"\nOK: {total_success}/{total_libs} ({total_success/total_libs*100:.1f}%)")
    print(f"FAIL: {total_failed}")
    
    print(f"\nPer categoria:")
    for category, results in all_results.items():
        success = len(results["success"])
        total = success + len(results["failed"])
        print(f"  {category}: {success}/{total}")
        if results["failed"]:
            for lib in results["failed"]:
                print(f"    X {lib}")
    
    # Verifica finale
    print(f"\n" + "=" * 70)
    result = subprocess.run(
        [sys.executable, "-m", "pip", "list", "--format=columns"],
        capture_output=True,
        text=True
    )
    
    lines = result.stdout.strip().split('\n')
    pkg_count = len(lines) - 2  # Rimuovi header
    
    print(f"Packages totali installati: {pkg_count}")
    print("=" * 70)
    
    if total_failed == 0:
        print("\nOK INSTALLAZIONE COMPLETATA!")
        return 0
    else:
        print(f"\n!! COMPLETATA CON {total_failed} ERRORI")
        return 1


if __name__ == "__main__":
    sys.exit(main())
