"""
Super Agent - Agente Programmatore Autonomo
Può essere eseguito come script standalone per automatizzare task di sviluppo
"""

import sys
import time
import runpy
import cProfile
import pstats
from pathlib import Path
from typing import Dict, Any, Optional, Union

# Add tools to path
tools_path = Path(__file__).parent / "tools"
sys.path.insert(0, str(tools_path))

from tools.code_generator import CodeGenerator
from tools.venv_manager import VirtualEnvironmentManager
from tools.library_updater import LibraryUpdater
from tools.vscode_learning import VSCodeLearningSystem
try:
    from tools.vscode_advanced_integration import VSCodeAdvancedIntegration, AnalysisResult, ADVANCED_LIBS_AVAILABLE
except ImportError:
    VSCodeAdvancedIntegration = None
    AnalysisResult = None
    ADVANCED_LIBS_AVAILABLE = False
from tools.local_llm_client import get_default_client
from tools.powershell_learning import PowerShellLearningSystem
from tools.powershell_advanced import PowerShellScriptGenerator, PowerShellAnalyzer
try:
    from tools.neural_agent_builder import (
        NeuralAgentBuilder,
        AgentArchitecture,
        TrainingConfig,
        NeuralArchitectureSearch,
        class SuperAgent:
            """
            Agente Programmatore Autonomo con tutte le capacità implementate
            """

            def __init__(self, workspace_path: Optional[str] = None):
                """
                Inizializza Super Agent
                Args:
                    workspace_path: Path del workspace (default: directory corrente)
                """
                if NeuralAgentBuilder and NEURAL_LIBS_AVAILABLE:
                    self.neural_builder = NeuralAgentBuilder()
                else:
                    self.neural_builder = None
                if AdvancedNeuralArchitect and ADVANCED_NEURAL_LIBS_AVAILABLE:
                    self.advanced_neural = AdvancedNeuralArchitect()
                else:
                    self.advanced_neural = None
                self.workspace = Path(workspace_path or Path.cwd())
                # Inizializza tutti i moduli
                self.code_gen = CodeGenerator()
                self.venv_manager = VirtualEnvironmentManager()
                self.library_updater = LibraryUpdater()
                self.learning = VSCodeLearningSystem()
                if VSCodeAdvancedIntegration and ADVANCED_LIBS_AVAILABLE:
                    self.vscode_integration = VSCodeAdvancedIntegration(workspace_path=str(self.workspace))
                else:
                    self.vscode_integration = None
                self.ps_learning = PowerShellLearningSystem()
                self.ps_generator = PowerShellScriptGenerator()
                self.ps_analyzer = PowerShellAnalyzer()
                print("[*] Super Agent inizializzato")
                print(f"[+] Workspace: {self.workspace}")
                print("[+] Moduli caricati: CodeGen, VenvManager, LibUpdater, VSCodeIntegration")
                print("[+] PowerShell: Learning, Generator, Analyzer")
                print("[OK] Ready per Python e PowerShell avanzato\n")
        # Inizializza tutti i moduli
        self.code_gen = CodeGenerator()
        self.venv_manager = VirtualEnvironmentManager()
        self.library_updater = LibraryUpdater()
        self.learning = VSCodeLearningSystem()
        if VSCodeAdvancedIntegration and ADVANCED_LIBS_AVAILABLE:
            self.vscode_integration = VSCodeAdvancedIntegration(workspace_path=str(self.workspace))
        else:
            self.vscode_integration = None
        self.ps_learning = PowerShellLearningSystem()
        self.ps_generator = PowerShellScriptGenerator()
        self.ps_analyzer = PowerShellAnalyzer()
        
        print("[*] Super Agent inizializzato")
        print(f"[+] Workspace: {self.workspace}")
        print("[+] Moduli caricati: CodeGen, VenvManager, LibUpdater, VSCodeIntegration")
        print("[+] PowerShell: Learning, Generator, Analyzer")
        print("[OK] Ready per Python e PowerShell avanzato\n")
    
    def generate_code(self, task: str) -> str:
        """
        Genera codice in base al task
        
        Args:
            task: Descrizione del codice da generare
            
        Returns:
            Codice generato
        """
        print(f"[*] Task: {task}")
        
        # Esempi di generazione codice
        if "classe" in task.lower() or "class" in task.lower():
            return self._generate_class_example(task)
        elif "funzione" in task.lower() or "function" in task.lower():
            return self._generate_function_example(task)
        elif "api" in task.lower():
            return self._generate_api_client_example(task)
        else:
            return "# Codice generato per: " + task
    
    def _generate_function_example(self, task: str) -> str:
        """Genera una funzione di esempio"""
        code = self.code_gen.generate_function(
            name="process_data",
            params=[
                {'name': 'data', 'type': 'List[Dict]', 'description': 'Input data'},
                {'name': 'validate', 'type': 'bool', 'default': True, 'description': 'Validate input'}
            ],
            return_type="Dict[str, Any]",
            docstring="Processa i dati in input e restituisce risultato",
            body="""results = {'processed': 0, 'errors': 0}
for item in data:
    try:
        if validate and not item:
            raise ValueError('Invalid item')
        # Process item
        results['processed'] += 1
    except Exception as e:
        results['errors'] += 1
        print(f'Error: {e}')
return results""",
            decorators=['@performance_monitor', '@error_handler']
        )
        return code
    
    def _generate_class_example(self, task: str) -> str:
        """Genera una classe di esempio"""
        code = self.code_gen.generate_class(
            name="DataProcessor",
            attributes=[
                {'name': 'data', 'type': 'List[Dict]', 'description': 'Raw data'},
                {'name': 'processed', 'type': 'int', 'description': 'Items processed'}
            ],
            methods=[
                {
                    'name': '__init__',
                    'params': [
                        {'name': 'self'},
                if NeuralAgentBuilder and NEURAL_LIBS_AVAILABLE:
                    self.neural_builder = NeuralAgentBuilder()
                else:
                    self.neural_builder = None
                self.workspace = Path(workspace_path or Path.cwd())
                # Inizializza tutti i moduli
                self.code_gen = CodeGenerator()
                self.venv_manager = VirtualEnvironmentManager()
                self.library_updater = LibraryUpdater()
                self.learning = VSCodeLearningSystem()
                if VSCodeAdvancedIntegration and ADVANCED_LIBS_AVAILABLE:
                    self.vscode_integration = VSCodeAdvancedIntegration(workspace_path=str(self.workspace))
                else:
                    self.vscode_integration = None
                self.ps_learning = PowerShellLearningSystem()
                self.ps_generator = PowerShellScriptGenerator()
                self.ps_analyzer = PowerShellAnalyzer()
                print("[*] Super Agent inizializzato")
                print(f"[+] Workspace: {self.workspace}")
                print("[+] Moduli caricati: CodeGen, VenvManager, LibUpdater, VSCodeIntegration")
                print("[+] PowerShell: Learning, Generator, Analyzer")
                print("[OK] Ready per Python e PowerShell avanzato\n")
    
    def generate_powershell(self, task: str, script_type: str = "auto") -> str:
        """
        Genera script PowerShell in base al task
        
        Args:
            task: Descrizione del task
            script_type: Tipo di script (cmdlet, function, script, auto)
            
        Returns:
            Script PowerShell generato
        """
        print(f"[*] Generando PowerShell: {task}")
        
        task_lower = task.lower()
        
        # Auto-detect tipo
        if script_type == "auto":
            if any(verb in task_lower for verb in ['get', 'set', 'new', 'remove', 'test']):
                script_type = "cmdlet"
            elif 'function' in task_lower:
                script_type = "function"
            else:
                script_type = "script"
        
        if script_type == "cmdlet":
            # Genera cmdlet
            verb = "Get"
            noun = "Data"
            
            # Estrai verb dal task
            for v in ['Get', 'Set', 'New', 'Remove', 'Test', 'Start', 'Stop', 'Add']:
                if v.lower() in task_lower:
                    verb = v
                    break
            
            """
            Agente Programmatore Autonomo con tutte le capacità implementate
            """
            def __init__(self, workspace_path: Optional[str] = None):
                noun = nouns[0]
            
            script = self.ps_generator.generate_cmdlet(
                verb=verb,
                noun=noun,
                parameters=[
                    {'name': 'InputObject', 'type': 'string', 'mandatory': True, 'pipeline': True},
                    {'name': 'Detailed', 'type': 'switch', 'mandatory': False}
                ],
                synopsis=task,
                process_block=f'''Write-Verbose "Processing $InputObject"
$result = @{{
    Input = $InputObject
    ProcessedAt = Get-Date
    Status = "Success"
}}

if ($Detailed) {{
    $result.Details = @{{
        Computer = $env:COMPUTERNAME
        User = $env:USERNAME
    }}
}}

return $result'''
            )
            
        elif script_type == "function":
            # Genera function
            script = self.ps_generator.generate_function(
                name="Invoke-CustomTask",
                parameters=[
                    {'name': 'Path', 'type': 'string', 'mandatory': True},
                    {'name': 'Recurse', 'type': 'switch', 'mandatory': False}
                ],
                synopsis=task,
                body='''Write-Verbose "Processing path: $Path"

$items = if ($Recurse) {
    Get-ChildItem -Path $Path -Recurse
} else {
    Get-ChildItem -Path $Path
}

Write-Output "Found $($items.Count) items"
return $items'''
            )
            
        else:
            # Genera script completo
            script = self.ps_generator.generate_script_with_header(
                title=task,
                parameters=[
                    {'name': 'InputPath', 'type': 'string', 'mandatory': True, 'description': 'Input path'},
                    {'name': 'OutputPath', 'type': 'string', 'mandatory': False, 'default': '"output.txt"', 'description': 'Output path'}
                ],
                main_logic='''Write-Log "Processing input: $InputPath"

if (Test-Path $InputPath) {
    $content = Get-Content $InputPath
    Write-Log "Read $($content.Count) lines"
    
    # Process content
    $processed = $content | ForEach-Object {
        $_.ToUpper()
    }
    
    # Save output
    $processed | Out-File $OutputPath
    Write-Log "Output saved to: $OutputPath"
    
    Write-Output "Success: Processed $($content.Count) lines"
} else {
    Write-Log "Input path not found: $InputPath" -Level "ERROR"
    throw "Input path not found"
}''',
                description=f"PowerShell script for: {task}",
                log_file="script_$(Get-Date -Format 'yyyyMMdd').log"
            )
        
        # Apprendi lo script generato
        self.ps_learning.learn_from_script(script, task)
        
        return script
    
    def analyze_powershell(self, script_content: str) -> Dict:
        """
        Analizza uno script PowerShell
        
        Args:
            script_content: Contenuto script
            
        Returns:
            Analisi completa
        """
        print(f"[*] Analizzando PowerShell script...")
        
        analysis = self.ps_analyzer.analyze_script(script_content)
        
        print(f"\n[+] Analisi:")
        print(f"  Lines: {analysis['metrics']['total_lines']}")
        print(f"  Cmdlets: {analysis['cmdlets']['unique']}")
        print(f"  Variables: {analysis['variables']['unique']}")
        print(f"  Complexity: {analysis['complexity']['total']} ({analysis['complexity']['rating']})")
        
        if analysis['best_practices']:
            print(f"\n[!] Best Practices ({len(analysis['best_practices'])} issues):")
            for issue in analysis['best_practices'][:3]:
                print(f"  - {issue}")
        
        if analysis['security']:
            print(f"\n[!] Security ({len(analysis['security'])} warnings):")
            for warning in analysis['security']:
                print(f"  [!] {warning}")
        
        return analysis
    
    def analyze_code(self, file_path: Union[str, Path]):
        """
        Analizza un file Python con tutti gli engines
        
        Args:
            file_path: Path del file da analizzare
        """
        print(f"\n[*] Analizzando: {file_path}")

        file_path = Path(file_path)
        if not file_path.exists():
            print(f"[ERROR] File non trovato: {file_path}")
            return

        # Analisi unificata
        result: AnalysisResult = self.vscode_integration.code_intelligence.run_full_analysis(str(file_path))

        print("\n[+] SYNTHESIS:")
        print(
            f"  - Status: {result.status} | "
            f"Quality: {result.quality_score:.1f}/100 | "
            f"Security: {result.security_score:.1f}/100"
        )

        ast_info = result.ast
        print(f"\n[+] AST Analysis:")
        print(f"  - Classes: {len(ast_info.get('classes', []))}")
        print(f"  - Functions: {len(ast_info.get('functions', []))}")
        print(f"  - Complexity: {ast_info.get('complexity', 0)}")
        print(f"  - LOC: {ast_info.get('lines_of_code', 0)}")

        print(f"\n[+] Quality Score: {result.quality_score:.1f}/100")
        issues = result.quality.issues if result.quality else []
        if issues:
            print(f"  [!] Issues trovati: {len(issues)}")
            for issue in issues[:5]:
                print(f"    - {issue.get('message', 'N/A')}")

        if result.security_issues:
            print("\n[+] Security overview:")
            high = sum(1 for i in result.security_issues if i.get("severity") == "high")
            medium = sum(1 for i in result.security_issues if i.get("severity") == "medium")
            low = sum(1 for i in result.security_issues if i.get("severity") == "low")
            print(f"  - High: {high}, Medium: {medium}, Low: {low}")
            for issue in result.security_issues[:5]:
                print(
                    f"    - ({issue['severity'].upper()} / {issue['category']}) "
                    f"{issue.get('code', 'N/A')}: {issue.get('message', '')}"
                )

        # Learning
        file_content = file_path.read_text(encoding='utf-8')
        self.learning.learn_from_code(file_content, str(file_path))
        insights = self.learning.generate_insights()
        
        if insights.get('summary'):
            print(f"\n[!] Insights:")
            summary = insights['summary']
            if 'patterns_learned' in summary:
                print(f"  - Patterns: {summary['patterns_learned']}")
            if 'common_errors' in summary:
                print(f"  - Errori comuni: {len(summary.get('common_errors', []))}")

    def security_scan(self, target: Optional[Union[str, Path]] = None):
        """Esegue una security scan usando il motore di analisi unificato."""
        print("\n[*] SECURITY SCAN")
        target_path: Optional[Path] = Path(target) if target else None

        files: list[Path]
        if target_path and target_path.is_file():
            files = [target_path]
        else:
            files = list(self.workspace.rglob("*.py"))[:20]

        if not files:
            print("[!] Nessun file Python trovato per la security scan")
            return

        all_results: list[AnalysisResult] = []

        for file in files:
            print(f"\n[*] Analizzando sicurezza: {file}")
            result = self.vscode_integration.code_intelligence.run_full_analysis(str(file))
            all_results.append(result)

            if result.security_issues:
                print(f"  [!] Problemi di sicurezza: {len(result.security_issues)}")
                for issue in result.security_issues[:5]:
                    print(
                        f"    - ({issue['severity'].upper()} / {issue['category']}) "
                        f"{issue.get('code', 'N/A')}: {issue.get('message', '')}"
                    )
            else:
                print("  [OK] Nessun problema critico rilevato (euristico)")

        total_issues = sum(len(r.security_issues) for r in all_results)
        by_severity: dict[str, int] = {"high": 0, "medium": 0, "low": 0}
        by_category: dict[str, int] = {}
        for r in all_results:
            for issue in r.security_issues:
                sev = str(issue.get("severity", "low")).lower()
                by_severity[sev] = by_severity.get(sev, 0) + 1
                cat = str(issue.get("category", "other"))
                by_category[cat] = by_category.get(cat, 0) + 1

        print("\n=== RIEPILOGO SECURITY SCAN ===")
        print(f"[+] File analizzati: {len(files)}")
        print(f"[+] Problemi totali: {total_issues}")
        print("[+] Per severità:")
        for sev in ["high", "medium", "low"]:
            print(f"    - {sev}: {by_severity.get(sev, 0)}")
        if by_category:
            print("[+] Per categoria:")
            for cat, count in sorted(by_category.items(), key=lambda x: (-x[1], x[0])):
                print(f"    - {cat}: {count}")

    def profile_script(self, file_path: Union[str, Path]):
        """Profila l'esecuzione di uno script Python e mostra i top hotspot."""
        file_path = Path(file_path)
        if not file_path.exists():
            print(f"[ERROR] File non trovato per profiling: {file_path}")
            return

        print(f"\n[*] Profiling: {file_path}")
        profiler = cProfile.Profile()
        start = time.time()
        try:
            profiler.enable()
            runpy.run_path(str(file_path), run_name="__main__")
            profiler.disable()
        except SystemExit:
            profiler.disable()
        duration = time.time() - start

        print(f"[+] Tempo totale esecuzione: {duration:.3f}s")
        stats = pstats.Stats(profiler).strip_dirs().sort_stats("cumulative")
        print("\n[+] Top 20 funzioni per tempo cumulativo:")
        stats.print_stats(20)

    def watch(self, interval: float = 2.0):
        """Modalità watch semplice: riesegue una mini-analisi sui file modificati.

        Scansiona la cartella di workspace e, ogni `interval` secondi, controlla
        se sono cambiati timestamp di file .py; per quelli modificati esegue
        un'analisi rapida con `analyze_code`.
        """
        print("\n[*] WATCH MODE attiva (Ctrl+C per uscire)")
        last_mtimes: dict[Path, float] = {}
        log_file = self.workspace / "super_agent_watch_log.jsonl"

        try:
            while True:
                python_files = list(self.workspace.rglob("*.py"))
                changed: list[Path] = []

                for file in python_files:
                    try:
                        mtime = file.stat().st_mtime
                    except OSError:
                        continue
                    old = last_mtimes.get(file)
                    if old is None:
                        last_mtimes[file] = mtime
                    elif mtime > old:
                        last_mtimes[file] = mtime
                        changed.append(file)

                if changed:
                    print(f"\n[+] File modificati rilevati: {len(changed)}")
                    for file in changed[:5]:
                        print(f"  - {file}")
                        result = self.vscode_integration.code_intelligence.run_full_analysis(str(file))

                        # Sintesi veloce a schermo
                        print(
                            f"    Status: {result.status} | "
                            f"Q: {result.quality_score:.1f} | S: {result.security_score:.1f}"
                        )

                        # Log JSON line per ogni analisi
                        try:
                            import json
                            entry = {
                                "timestamp": time.time(),
                                "file": str(file),
                                "status": result.status,
                                "quality_score": result.quality_score,
                                "security_score": result.security_score,
                            }
                            with log_file.open("a", encoding="utf-8") as f:
                                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
                        except Exception as exc:  # noqa: BLE001
                            print(f"[WARN] Impossibile scrivere il log watch: {exc}")

                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n[OK] Watch mode terminata dall'utente")
    
    def improve_code(self, file_path: Union[str, Path], output_path: Optional[Union[str, Path]] = None):
        """
        Migliora un file Python con refactoring automatico
        
        Args:
            file_path: File da migliorare
            output_path: Dove salvare output (default: sovrascrive originale)
        """
        print(f"\n[*] Migliorando: {file_path}")
        
        file_path = Path(file_path)
        if not file_path.exists():
            print(f"[ERROR] File non trovato: {file_path}")
            return
        
        # Legge sempre il file in UTF-8 per supportare caratteri estesi
        code = file_path.read_text(encoding="utf-8")
        
        # Refactoring
        improved = self.vscode_integration.refactoring_engine.format_code(code)
        improved = self.vscode_integration.refactoring_engine.organize_imports(improved)
        
        # Salva
        output = Path(output_path) if output_path else file_path
        output.write_text(improved, encoding="utf-8")
        
        print(f"[OK] Codice migliorato salvato in: {output}")
    
    def manage_environment(self, action: str, **kwargs):
        """
        Gestisce virtual environments
        
        Args:
            action: Azione da eseguire (create, list, install, packages, update)
            **kwargs: Parametri specifici per l'azione
        """
        print(f"\n[*] Virtual Environment: {action}")
        
        if action == "create":
            name = kwargs.get('name', 'new_env')
            result = self.venv_manager.create_venv(name)
            print(f"[OK] Ambiente creato: {result['name']}")
            
        elif action == "list":
            envs = self.venv_manager.list_venvs()
            print(f"[+] Ambienti disponibili: {len(envs)}")
            for env in envs:
                status = "[OK]" if env['exists'] else "[ERROR]"
                print(f"  {status} {env['name']}: {env['packages_count']} packages")
        
        elif action == "packages":
            name = kwargs.get('name', 'super_agent_advanced')
            packages = self.venv_manager.get_packages(name)
            print(f"[+] Packages in {name}: {len(packages)}")
            for pkg in packages[:10]:  # Primi 10
                print(f"  - {pkg['name']} {pkg['version']}")
            if len(packages) > 10:
                print(f"  ... e altri {len(packages) - 10}")
        
        elif action == "install":
            name = kwargs.get('name', 'super_agent_advanced')
            package = kwargs.get('package')
            if package:
                result = self.venv_manager.install_package(name, package)
                if result.get('success'):
                    print(f"[OK] Installato: {package}")
                else:
                    print(f"[ERROR] Errore: {result.get('error')}")
        
        elif action == "update":
            name = kwargs.get('name', 'super_agent_advanced')
            outdated = self.library_updater.list_outdated_packages(name)
            print(f"[+] Packages da aggiornare: {len(outdated)}")
            for pkg in outdated[:5]:
                print(f"  - {pkg['name']}: {pkg['version']} → {pkg['latest_version']}")
    
    def auto_task(self, task_description: str):
        """
        Esegue un task completo in modo autonomo
        
        Args:
            task_description: Descrizione del task
        """
        print(f"\n[*] AUTO TASK: {task_description}\n")
        print("=" * 80)
        
        # Analizza task e decide azioni
        task_lower = task_description.lower()
        
        if "analizza" in task_lower or "analyze" in task_lower:
            # Trova file Python nel workspace
            python_files = list(self.workspace.rglob("*.py"))
            print(f"[+] Trovati {len(python_files)} file Python")
            
            # Analizza primi N file
            for i, file in enumerate(python_files[:5], 1):
                print(f"\n[{i}/{min(5, len(python_files))}] ", end="")
                self.analyze_code(file)
        
        elif "genera" in task_lower or "create" in task_lower:
            code = self.generate_code(task_description)
            
            # Salva in file
            output_file = self.workspace / "generated_code.py"
            output_file.write_text(code)
            print(f"\n[OK] Codice generato salvato in: {output_file}")
            print(f"\n{code}")
        
        elif "migliora" in task_lower or "improve" in task_lower:
            python_files = list(self.workspace.rglob("*.py"))
            if python_files:
                self.improve_code(python_files[0])
        
        elif "venv" in task_lower or "ambiente" in task_lower:
            self.manage_environment("list")
        
        else:
            print("[!] Task non riconosciuto, eseguo analisi generale...")
            self.manage_environment("list")
            
        print("\n" + "=" * 80)
        print("[OK] Task completato!")

    def run_learning_demo(self, demo_case: str = "all"):
        """Esegue i demo del sistema di apprendimento collaborativo"""
        try:
            from demo_collaborative_learning import (
                demo_basic_learning,
                demo_agent_observation,
                demo_teaching,
                demo_collaboration,
                demo_shared_knowledge,
                demo_multi_agent_learning,
                demo_knowledge_export_import,
                demo_skill_improvement,
                demo_peer_learning
            )
        except ImportError as exc:
            print(f"[ERROR] Impossibile caricare i demo: {exc}")
            return

        demos = {
            "basic": demo_basic_learning,
            "observation": demo_agent_observation,
            "teaching": demo_teaching,
            "collaboration": demo_collaboration,
            "shared_knowledge": demo_shared_knowledge,
            "multi_agent": demo_multi_agent_learning,
            "export_import": demo_knowledge_export_import,
            "skill_improvement": demo_skill_improvement,
            "peer_learning": demo_peer_learning
        }

        normalized = (demo_case or "all").strip().lower().replace("-", "_").replace(" ", "_")
        if not normalized:
            normalized = "all"

        to_run = []
        if normalized == "all":
            to_run = list(demos.items())
        elif normalized in demos:
            to_run = [(normalized, demos[normalized])]
        else:
            matches = [name for name in demos if normalized in name]
            if matches:
                to_run = [(matches[0], demos[matches[0]])]
            else:
                print(f"[!] Demo non riconosciuto: {demo_case}")
                print(f"    Opzioni: {', '.join(sorted(demos.keys()))}")
                return

        for demo_name, demo_fn in to_run:
            print(f"\n[ DEMO ] Esecuzione: {demo_name}")
            try:
                demo_fn()
            except Exception as exc:
                print(f"[ERROR] Il demo {demo_name} ha sollevato un errore: {exc}")


def main():
    """Entry point per esecuzione da terminale"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Super Agent - Agente Programmatore Autonomo"
    )
    parser.add_argument(
        "task",
        nargs="?",
        default="status",
        help=(
            "Task da eseguire "
            "(genera, analizza, migliora, venv, auto, demo, status, "
            "security, profile, watch, report)"
        ),
    )
    parser.add_argument(
        "description",
        nargs="*",
        help="Descrizione task per generazione codice"
    )
    parser.add_argument(
        "--file",
        help="File target per analisi/miglioramento/profiling/security",
    )
    parser.add_argument(
        "--workspace",
        default=".",
        help="Path del workspace (default: directory corrente)"
    )
    parser.add_argument(
        "--demo-case",
        help="Nome del demo da eseguire (basic, observation, teaching, collaboration, etc.)"
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=2.0,
        help="Intervallo in secondi per la modalità watch (default: 2.0)",
    )
    
    args = parser.parse_args()
    
    # Combina task e description per input libero
    full_task = args.task
    if args.description:
        full_task = args.task + " " + " ".join(args.description)
    
    # Inizializza agent
    agent = SuperAgent(workspace_path=args.workspace)
    
    # Esegui task
    if args.task == "status":
        print("[+] STATUS CHECK")
        agent.manage_environment("list")
        
    elif args.task == "genera":
        # Genera codice con descrizione personalizzata
        if args.description:
            description = " ".join(args.description)
            code = agent.generate_code(f"Genera {description}")
        else:
            code = agent.generate_code("Genera una classe DataProcessor")
        print("\n" + "=" * 80)
        print(code)
        print("=" * 80)
        
    elif args.task == "analizza":
        if args.file:
            agent.analyze_code(args.file)
        else:
            print("[!] Specifica --file per analisi")
            
    elif args.task == "migliora":
        if args.file:
            agent.improve_code(args.file)
        else:
            print("[!] Specifica --file per miglioramento")
            
    elif args.task == "venv":
        agent.manage_environment("list")

    elif args.task == "demo":
        demo_case = args.demo_case or (" ".join(args.description) if args.description else "all")
        agent.run_learning_demo(demo_case)

    elif args.task == "security":
        # Security scan euristica basata sul quality analyzer
        agent.security_scan(args.file)

    elif args.task == "profile":
        if args.file:
            agent.profile_script(args.file)
        else:
            print("[!] Specifica --file per il profiling")

    elif args.task == "watch":
        agent.watch(interval=args.interval)

    elif args.task == "report":
        # Report basato sui log JSONL prodotti da watch e da altre analisi future
        log_file = Path(args.workspace) / "super_agent_watch_log.jsonl"
        if not log_file.exists():
            print(f"[!] Nessun log trovato in: {log_file}")
            print("    Esegui prima 'watch' o altri comandi che producono log.")
            return

        try:
            import json
        except ImportError:
            print("[ERROR] Impossibile importare json (modulo standard mancante?)")
            return

        entries: list[dict[str, Any]] = []
        for line in log_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                entries.append(data)
            except Exception:
                continue

        if not entries:
            print("[!] Nessuna entry valida trovata nel log")
            return

        # Aggrega per file
        per_file: dict[str, dict[str, Any]] = {}
        for e in entries:
            file = str(e.get("file", "?"))
            info = per_file.setdefault(
                file,
                {
                    "count": 0,
                    "last_status": "?",
                    "last_quality": 0.0,
                    "last_security": 0.0,
                    "worst_quality": 100.0,
                    "worst_security": 100.0,
                },
            )
            q = float(e.get("quality_score", 0.0))
            s = float(e.get("security_score", 0.0))
            status = str(e.get("status", "?"))

            info["count"] += 1
            info["last_status"] = status
            info["last_quality"] = q
            info["last_security"] = s
            info["worst_quality"] = min(info["worst_quality"], q)
            info["worst_security"] = min(info["worst_security"], s)

        # Ordina i file peggiori per combinazione di qualità + sicurezza
        ranked = sorted(
            per_file.items(),
            key=lambda kv: (kv[1]["worst_quality"] + kv[1]["worst_security"]),
        )

        print("\n=== SUPER AGENT REPORT (basato su watch log) ===")
        print(f"[+] File tracciati: {len(per_file)}")
        print(f"[+] Analisi totali: {len(entries)}")

        print("\n[TOP 10] File più critici (qualità + sicurezza)")
        for i, (file, info) in enumerate(ranked[:10], 1):
            print(
                f"{i:2d}. {file}\n"
                f"    Last:   status={info['last_status']} "
                f"Q={info['last_quality']:.1f} S={info['last_security']:.1f}\n"
                f"    Worst:  Q={info['worst_quality']:.1f} S={info['worst_security']:.1f} "
                f"(samples={info['count']})"
            )
        
    elif args.task == "auto":
        # Auto task con descrizione
        if args.description:
            description = " ".join(args.description)
            agent.auto_task(description)
        else:
            print("[!] Specifica descrizione task dopo 'auto'")
        
    else:
        # Qualsiasi altro input viene trattato come auto task
        agent.auto_task(full_task)


if __name__ == "__main__":
    main()
