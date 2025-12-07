"""
VS Code Advanced Integration - Installazione librerie per integrazione avanzata
Installa tutte le librerie necessarie per interagire con VS Code
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from tools.venv_manager import VirtualEnvironmentManager


def install_vscode_libraries():
    """Installa tutte le librerie per integrazione avanzata VS Code"""
    
    print("=" * 70)
    print("INSTALLAZIONE LIBRERIE VS CODE INTEGRATION")
    print("=" * 70)
    
    manager = VirtualEnvironmentManager()
    venv_name = "super_agent_advanced"
    
    # Librerie per integrazione VS Code
    vscode_libraries = {
        "Editor & File Management": [
            "watchdog",              # File system monitoring
            "pathspec",              # Path pattern matching (gitignore style)
            "chardet",               # Character encoding detection
            "python-magic-bin",      # File type detection (Windows)
            "filetype",              # File type identification
        ],
        
        "Code Analysis & AST": [
            "astroid",               # AST manipulation avanzata
            "ast-decompiler",        # AST to source code
            "astor",                 # AST to source code
            "redbaron",              # Full syntax tree (FST)
            "parso",                 # Python parser
            "jedi",                  # Code completion & analysis
            "rope",                  # Refactoring library
        ],
        
        "Linting & Formatting": [
            "flake8",                # Linting
            "autopep8",              # Auto-formatting
            "isort",                 # Import sorting
            "pycodestyle",           # PEP 8 checker
            "pydocstyle",            # Docstring checker
            "bandit",                # Security linter
            "radon",                 # Code complexity
            "mccabe",                # Complexity checker
        ],
        
        "Git Integration": [
            "gitpython",             # Git operations
            "pygit2",                # Git library
            "dulwich",               # Pure Python Git
        ],
        
        "Documentation": [
            "sphinx",                # Documentation generator
            "pdoc3",                 # Auto documentation
            "pydoc-markdown",        # Markdown documentation
            "mkdocs",                # Documentation site
            "mkdocs-material",       # Material theme
        ],
        
        "Testing Integration": [
            "pytest-watch",          # Auto-run tests
            "pytest-cov",            # Coverage for pytest
            "pytest-xdist",          # Parallel testing
            "pytest-timeout",        # Test timeouts
            "pytest-mock",           # Mocking
            "unittest-xml-reporting", # XML test reports
        ],
        
        "Debugging & Profiling": [
            "ipdb",                  # IPython debugger
            "pudb",                  # Full-screen debugger
            "pdbpp",                 # Enhanced debugger
            "memory-profiler",       # Memory profiling
            "line-profiler",         # Line profiling
            "py-spy",                # Sampling profiler
        ],
        
        "Language Server Protocol": [
            "python-lsp-server",     # Python LSP implementation
            "pylsp-mypy",            # Mypy plugin for LSP
            "python-lsp-black",      # Black plugin for LSP
            "pyls-isort",            # isort plugin
        ],
        
        "Terminal & Shell": [
            "click",                 # CLI creation (già installato via typer)
            "prompt-toolkit",        # Terminal UI
            "colorama",              # Colored terminal output
            "termcolor",             # Terminal colors
            "blessed",               # Terminal formatting
            "rich-cli",              # Rich CLI
        ],
        
        "File Formats": [
            "toml",                  # TOML parser
            "pyyaml",                # YAML parser
            "python-dotenv",         # .env file support
            "configparser",          # Config files (built-in enhanced)
            "jsonschema",            # JSON schema validation
            "xmltodict",             # XML to dict
        ],
        
        "Project Management": [
            "poetry",                # Dependency management
            "pipenv",                # Pipfile support
            "pip-tools",             # pip-compile, pip-sync
            "pipdeptree",            # Dependency tree
            "safety",                # Security vulnerabilities
        ],
        
        "Code Search & Navigation": [
            "pygments",              # Syntax highlighting
            "tree-sitter",           # Parser generator
            "whoosh",                # Full-text search
            "fuzzywuzzy",            # Fuzzy string matching
            "python-levenshtein",    # Edit distance
        ],
        
        "Workspace & Project": [
            "pyproject-hooks",       # PEP 517 hooks
            "build",                 # PEP 517 build frontend
            "setuptools-scm",        # Version from git
            "versioneer",            # Version management
        ],
        
        "Extensions & Plugins": [
            "pluggy",                # Plugin system
            "stevedore",             # Dynamic plugin loading
            "entrypoints",           # Entry point discovery
        ],
        
        "Performance & Optimization": [
            "cython",                # Python to C compiler
            "nuitka",                # Python compiler
            "pypy",                  # Alternative interpreter (se disponibile)
        ],
        
        "Utils & Helpers": [
            "more-itertools",        # Extended itertools
            "toolz",                 # Functional programming
            "attrs",                 # Class decorators
            "cattrs",                # Object serialization
            "box",                   # Dict with dot notation
            "boltons",               # Utility functions
        ]
    }
    
    print(f"\nInstallazione in ambiente: {venv_name}")
    print(f"{sum(len(libs) for libs in vscode_libraries.values())} librerie da installare\n")
    
    total_installed = 0
    total_failed = 0
    results_by_category = {}
    
    for category, libraries in vscode_libraries.items():
        print(f"\n{'='*70}")
        print(f"[{category}]")
        print(f"{'='*70}")
        
        category_results = {"success": [], "failed": []}
        
        for i, library in enumerate(libraries, 1):
            print(f"\n[{i}/{len(libraries)}] Installazione {library}...")
            
            try:
                success, message = manager.install_package(
                    venv_name,
                    library
                )
                
                if success:
                    print(f"  OK {library} installato con successo")
                    category_results["success"].append(library)
                    total_installed += 1
                else:
                    print(f"  X Errore: {message[:100]}")
                    category_results["failed"].append(library)
                    total_failed += 1
                    
            except Exception as e:
                print(f"  X Errore: {str(e)[:100]}")
                category_results["failed"].append(library)
                total_failed += 1
        
        results_by_category[category] = category_results
        
        # Riepilogo categoria
        success_count = len(category_results["success"])
        failed_count = len(category_results["failed"])
        total_count = len(libraries)
        
        print(f"\nRiepilogo {category}:")
        print(f"  OK Installati: {success_count}/{total_count}")
        if failed_count > 0:
            print(f"  X Falliti: {failed_count}")
            for lib in category_results["failed"]:
                print(f"     - {lib}")
    
    # Riepilogo finale
    print("\n" + "=" * 70)
    print("RIEPILOGO INSTALLAZIONE")
    print("=" * 70)
    
    total_libraries = total_installed + total_failed
    
    print(f"\nOK Librerie installate: {total_installed}/{total_libraries} ({total_installed/total_libraries*100:.1f}%)")
    print(f"X Fallite: {total_failed}")
    
    # Dettagli per categoria
    print(f"\nInstallazioni per categoria:")
    for category, results in results_by_category.items():
        success = len(results["success"])
        total = success + len(results["failed"])
        status = "OK" if len(results["failed"]) == 0 else "!!"
        print(f"  {status} {category}: {success}/{total}")
    
    # Ottieni info ambiente aggiornate
    print(f"\nVerifica ambiente finale...")
    venv_info = manager.get_venv_info(venv_name)
    
    if venv_info:
        print(f"\nAmbiente '{venv_name}':")
        print(f"  - Python: {venv_info['python_version']}")
        print(f"  - Pip: {venv_info['pip_version']}")
        print(f"  - Packages totali: {venv_info['packages_count']}")
        print(f"  - Path: {venv_info['path']}")
    
    # Export requirements aggiornati
    print(f"\nExport requirements aggiornati...")
    req_file = manager.export_requirements(venv_name, "requirements_vscode.txt")
    print(f"  OK Salvato: {req_file}")
    
    print("\n" + "=" * 70)
    if total_failed == 0:
        print("OK INSTALLAZIONE COMPLETATA CON SUCCESSO!")
    else:
        print(f"!! INSTALLAZIONE COMPLETATA CON {total_failed} ERRORI")
    print("=" * 70)
    
    print(f"\nAttivazione ambiente:")
    print(f"   . {venv_info['path']}\\Scripts\\activate.ps1")
    
    return {
        "total_installed": total_installed,
        "total_failed": total_failed,
        "results_by_category": results_by_category,
        "venv_info": venv_info
    }


if __name__ == "__main__":
    results = install_vscode_libraries()
    
    # Exit code basato sui risultati
    exit_code = 0 if results["total_failed"] == 0 else 1
    sys.exit(exit_code)
