"""
Installer per librerie PowerShell avanzate per Super Agent
Linguaggio, progettazione e creazione automatica con PowerShell
"""

import subprocess
import sys
from pathlib import Path


# Librerie per interazione avanzata con PowerShell
POWERSHELL_LIBRARIES = {
    # Core PowerShell Integration
    'powershell': {
        'package': 'pythonnet',
        'description': 'Python.NET for PowerShell integration',
        'category': 'Core PowerShell'
    },
    
    # Script Generation & Parsing
    'powershell-parser': {
        'package': 'pyparsing',
        'description': 'Parser per sintassi PowerShell',
        'category': 'Parsing'
    },
    'ast-analysis': {
        'package': 'astroid',
        'description': 'AST analysis anche per PowerShell',
        'category': 'Analysis'
    },
    
    # Template & Code Generation
    'jinja2': {
        'package': 'jinja2',
        'description': 'Template engine per generazione script',
        'category': 'Generation'
    },
    'mako': {
        'package': 'mako',
        'description': 'Template engine alternativo',
        'category': 'Generation'
    },
    
    # Syntax Highlighting & Formatting
    'pygments': {
        'package': 'pygments',
        'description': 'Syntax highlighting PowerShell',
        'category': 'Formatting'
    },
    'black': {
        'package': 'black',
        'description': 'Code formatter (adattabile a PowerShell)',
        'category': 'Formatting'
    },
    
    # DSL & Language Design
    'textx': {
        'package': 'textX',
        'description': 'DSL framework per creare linguaggi',
        'category': 'Language Design'
    },
    'lark': {
        'package': 'lark-parser',
        'description': 'Parser per creare linguaggi custom',
        'category': 'Language Design'
    },
    'parsimonious': {
        'package': 'parsimonious',
        'description': 'PEG parser per linguaggi',
        'category': 'Language Design'
    },
    
    # Shell Automation
    'pexpect': {
        'package': 'pexpect',
        'description': 'Automazione shell interattiva',
        'category': 'Automation'
    },
    'sh': {
        'package': 'sh',
        'description': 'Shell command wrapper',
        'category': 'Automation'
    },
    'plumbum': {
        'package': 'plumbum',
        'description': 'Shell combinators e command line',
        'category': 'Automation'
    },
    
    # Configuration & DSL
    'pyyaml': {
        'package': 'pyyaml',
        'description': 'YAML per configurazioni PowerShell',
        'category': 'Configuration'
    },
    'toml': {
        'package': 'toml',
        'description': 'TOML per configurazioni',
        'category': 'Configuration'
    },
    'hydra': {
        'package': 'hydra-core',
        'description': 'Configuration framework avanzato',
        'category': 'Configuration'
    },
    
    # Process Management
    'psutil': {
        'package': 'psutil',
        'description': 'Process e system utilities',
        'category': 'System'
    },
    'supervisor': {
        'package': 'supervisor',
        'description': 'Process control system',
        'category': 'System'
    },
    
    # Windows Integration
    'pywin32': {
        'package': 'pywin32',
        'description': 'Windows API access',
        'category': 'Windows'
    },
    'wmi': {
        'package': 'wmi',
        'description': 'Windows Management Instrumentation',
        'category': 'Windows'
    },
    'winrm': {
        'package': 'pywinrm',
        'description': 'Windows Remote Management',
        'category': 'Windows'
    },
    
    # Code Analysis
    'radon': {
        'package': 'radon',
        'description': 'Code complexity metrics',
        'category': 'Analysis'
    },
    'lizard': {
        'package': 'lizard',
        'description': 'Code complexity analyzer',
        'category': 'Analysis'
    },
    
    # Documentation Generation
    'sphinx': {
        'package': 'sphinx',
        'description': 'Documentation generator',
        'category': 'Documentation'
    },
    'mkdocs': {
        'package': 'mkdocs',
        'description': 'Markdown documentation',
        'category': 'Documentation'
    },
    
    # Testing & Validation
    'hypothesis': {
        'package': 'hypothesis',
        'description': 'Property-based testing',
        'category': 'Testing'
    },
    'schema': {
        'package': 'schema',
        'description': 'Data validation',
        'category': 'Validation'
    },
    'cerberus': {
        'package': 'cerberus',
        'description': 'Validation framework',
        'category': 'Validation'
    },
    
    # AI/NLP per comprensione comandi
    'transformers': {
        'package': 'transformers',
        'description': 'NLP per comprensione linguaggio naturale',
        'category': 'AI/NLP'
    },
    'spacy': {
        'package': 'spacy',
        'description': 'NLP per parsing comandi',
        'category': 'AI/NLP'
    },
    'nltk': {
        'package': 'nltk',
        'description': 'Natural Language Toolkit',
        'category': 'AI/NLP'
    },
    
    # Graph & Visualization (per dependency graphs)
    'networkx': {
        'package': 'networkx',
        'description': 'Graph analysis per dipendenze',
        'category': 'Graph'
    },
    'graphviz': {
        'package': 'graphviz',
        'description': 'Graph visualization',
        'category': 'Visualization'
    },
    
    # CLI Building
    'click': {
        'package': 'click',
        'description': 'CLI framework',
        'category': 'CLI'
    },
    'typer': {
        'package': 'typer',
        'description': 'Modern CLI framework',
        'category': 'CLI'
    },
    'argcomplete': {
        'package': 'argcomplete',
        'description': 'Bash/PowerShell completion',
        'category': 'CLI'
    },
    
    # Rich Output
    'rich': {
        'package': 'rich',
        'description': 'Rich terminal output',
        'category': 'Output'
    },
    'colorama': {
        'package': 'colorama',
        'description': 'Cross-platform colored output',
        'category': 'Output'
    },
    'tabulate': {
        'package': 'tabulate',
        'description': 'Table formatting',
        'category': 'Output'
    },
    
    # Async & Concurrency
    'asyncio': {
        'package': 'aiofiles',
        'description': 'Async file operations',
        'category': 'Async'
    },
    'trio': {
        'package': 'trio',
        'description': 'Async I/O framework',
        'category': 'Async'
    },
}


def get_venv_python():
    """Ottiene path Python del venv super_agent_advanced"""
    venv_path = Path("venvs/super_agent_advanced")
    
    if sys.platform == "win32":
        python_exe = venv_path / "Scripts" / "python.exe"
    else:
        python_exe = venv_path / "bin" / "python"
    
    if not python_exe.exists():
        raise FileNotFoundError(f"Virtual environment non trovato: {venv_path}")
    
    return str(python_exe)


def install_libraries():
    """Installa tutte le librerie PowerShell avanzate"""
    python_exe = get_venv_python()
    
    print("🤖 Super Agent - PowerShell Advanced Libraries Installer")
    print("=" * 80)
    print(f"Target: {python_exe}")
    print(f"Total libraries: {len(POWERSHELL_LIBRARIES)}")
    print("=" * 80)
    
    # Raggruppa per categoria
    by_category = {}
    for name, info in POWERSHELL_LIBRARIES.items():
        category = info['category']
        if category not in by_category:
            by_category[category] = []
        by_category[category].append((name, info))
    
    installed = 0
    failed = 0
    skipped = 0
    
    for category, libs in sorted(by_category.items()):
        print(f"\n📦 {category} ({len(libs)} libraries)")
        print("-" * 80)
        
        for name, info in libs:
            package = info['package']
            desc = info['description']
            
            print(f"\n  Installing: {name}")
            print(f"  Package: {package}")
            print(f"  Description: {desc}")
            
            try:
                # Installa pacchetto
                result = subprocess.run(
                    [python_exe, "-m", "pip", "install", package, "-q"],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if result.returncode == 0:
                    print(f"  ✅ SUCCESS")
                    installed += 1
                else:
                    # Controlla se già installato
                    if "already satisfied" in result.stdout.lower() or "already satisfied" in result.stderr.lower():
                        print(f"  ⏭️  ALREADY INSTALLED")
                        skipped += 1
                    else:
                        print(f"  ❌ FAILED: {result.stderr[:100]}")
                        failed += 1
                        
            except subprocess.TimeoutExpired:
                print(f"  ⏱️  TIMEOUT (>300s)")
                failed += 1
            except Exception as e:
                print(f"  ❌ ERROR: {str(e)[:100]}")
                failed += 1
    
    # Summary
    print("\n" + "=" * 80)
    print("INSTALLATION SUMMARY")
    print("=" * 80)
    print(f"✅ Installed: {installed}")
    print(f"⏭️  Already installed: {skipped}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total: {installed + skipped + failed}/{len(POWERSHELL_LIBRARIES)}")
    print(f"📈 Success rate: {(installed + skipped) / len(POWERSHELL_LIBRARIES) * 100:.1f}%")
    
    if failed == 0:
        print("\n🎉 ALL LIBRARIES INSTALLED SUCCESSFULLY!")
    else:
        print(f"\n⚠️  {failed} libraries failed to install")
    
    print("\n" + "=" * 80)
    print("Categories installed:")
    for category in sorted(by_category.keys()):
        count = len(by_category[category])
        print(f"  • {category}: {count} libraries")
    
    return installed + skipped == len(POWERSHELL_LIBRARIES)


if __name__ == "__main__":
    try:
        success = install_libraries()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
