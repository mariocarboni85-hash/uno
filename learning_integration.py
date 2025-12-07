"""
VS Code Learning Integration - Integrazione automatica con il workflow
Monitora e apprende automaticamente durante lo sviluppo
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tools.vscode_learning import VSCodeLearningSystem
from pathlib import Path
import subprocess
import time
from datetime import datetime


class LearningIntegration:
    """Integra il sistema di apprendimento con il workflow di sviluppo"""
    
    def __init__(self):
        self.learner = VSCodeLearningSystem()
        
    def monitor_file_changes(self, file_path: str, content: str):
        """Monitora modifiche ai file e apprende pattern"""
        
        # Analizza il tipo di file
        ext = Path(file_path).suffix
        
        if ext == ".py":
            self._analyze_python_code(content, file_path)
        elif ext in [".js", ".ts"]:
            self._analyze_javascript_code(content, file_path)
    
    def _analyze_python_code(self, code: str, file_path: str):
        """Analizza codice Python e apprende pattern"""
        
        # Pattern comuni
        patterns = {
            "import": r"^import\s+\w+|^from\s+\w+\s+import",
            "function": r"^def\s+\w+\(",
            "class": r"^class\s+\w+",
            "async": r"^async\s+def",
            "decorator": r"^@\w+"
        }
        
        lines = code.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Identifica pattern
            for pattern_type, regex in patterns.items():
                import re
                if re.match(regex, line):
                    self.learner.learn_code_pattern(
                        code=line,
                        pattern_type=pattern_type,
                        context=f"Found in {Path(file_path).name}",
                        success=True
                    )
    
    def _analyze_javascript_code(self, code: str, file_path: str):
        """Analizza codice JavaScript/TypeScript"""
        
        lines = code.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Pattern comuni JS/TS
            if line.startswith('import ') or line.startswith('export '):
                self.learner.learn_code_pattern(
                    code=line,
                    pattern_type="import/export",
                    context=f"Found in {Path(file_path).name}",
                    success=True
                )
            elif 'function ' in line or '=>' in line:
                self.learner.learn_code_pattern(
                    code=line,
                    pattern_type="function",
                    context=f"Found in {Path(file_path).name}",
                    success=True
                )
    
    def monitor_command_execution(
        self,
        command: str,
        command_type: str = "terminal"
    ):
        """Monitora esecuzione comandi e apprende"""
        
        start_time = time.time()
        
        try:
            # Esegui comando
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            execution_time = time.time() - start_time
            success = result.returncode == 0
            
            # Apprendi
            self.learner.learn_command(
                command=command,
                command_type=command_type,
                output=result.stdout + result.stderr,
                success=success,
                execution_time=execution_time
            )
            
            return success, result.stdout, result.stderr
            
        except subprocess.TimeoutExpired:
            self.learner.learn_command(
                command=command,
                command_type=command_type,
                output="Timeout",
                success=False,
                execution_time=300
            )
            return False, "", "Command timeout"
        except Exception as e:
            self.learner.learn_command(
                command=command,
                command_type=command_type,
                output=str(e),
                success=False
            )
            return False, "", str(e)
    
    def handle_error(
        self,
        error_type: str,
        error_message: str,
        code_context: str = "",
        file_path: str = ""
    ):
        """Gestisce errori e cerca soluzioni"""
        
        # Cerca soluzione esistente
        solution = self.learner.get_error_solution(error_type, error_message)
        
        if solution:
            print(f"💡 Soluzione suggerita dal sistema di apprendimento:")
            print(f"   {solution}")
        
        # Registra errore
        self.learner.learn_error(
            error_type=error_type,
            error_message=error_message,
            code_context=code_context,
            solution=solution,
            file_path=file_path
        )
        
        return solution
    
    def suggest_snippets(self, context: str, language: str = "python"):
        """Suggerisci snippet basati sul contesto"""
        
        results = self.learner.search_snippets(context, language=language)
        
        if results:
            print(f"\n💡 Snippet suggeriti per '{context}':")
            for i, snippet in enumerate(results[:3], 1):
                print(f"\n{i}. {snippet['name']} (usato {snippet['used_count']} volte)")
                print(f"   {snippet['description']}")
                print(f"   Tags: {', '.join(snippet['tags'])}")
        
        return results
    
    def get_recommendations(self):
        """Ottieni raccomandazioni basate sull'apprendimento"""
        
        insights = self.learner.generate_insights()
        
        print("\n" + "=" * 60)
        print("📊 RACCOMANDAZIONI BASATE SULL'APPRENDIMENTO")
        print("=" * 60)
        
        # Riepilogo
        summary = insights["summary"]
        print(f"\n✓ Pattern appresi: {summary['patterns']['total']}")
        print(f"  • Tasso successo: {summary['patterns']['success_rate']:.1%}")
        
        print(f"\n✓ Errori gestiti: {summary['errors']['unique_errors']}")
        print(f"  • Risolti: {summary['errors']['solved']}")
        print(f"  • Tasso risoluzione: {summary['errors']['solve_rate']:.1%}")
        
        print(f"\n✓ Comandi eseguiti: {summary['commands']['total_executed']}")
        
        # Raccomandazioni
        if insights["recommendations"]:
            print(f"\n💡 Raccomandazioni:")
            for rec in insights["recommendations"]:
                print(f"  • {rec}")
        
        # Warnings
        if insights["warnings"]:
            print(f"\n⚠️  Avvisi:")
            for warn in insights["warnings"]:
                print(f"  • {warn}")
        
        # Pattern più usati
        most_used = self.learner.get_most_used_commands(5)
        if most_used:
            print(f"\n🔥 Comandi più usati:")
            for cmd, count in most_used:
                print(f"  • {cmd}: {count} volte")
        
        return insights
    
    def daily_summary(self):
        """Genera riepilogo giornaliero dell'apprendimento"""
        
        stats = self.learner.get_learning_stats()
        
        print("\n" + "=" * 60)
        print(f"📅 RIEPILOGO APPRENDIMENTO - {datetime.now().strftime('%d/%m/%Y')}")
        print("=" * 60)
        
        print(f"\n📚 Knowledge Base:")
        print(f"  • Pattern: {stats['patterns']['total']}")
        print(f"  • Errori: {stats['errors']['total']} ({stats['errors']['solved']} risolti)")
        print(f"  • Comandi: {stats['commands']['total']}")
        print(f"  • Snippets: {stats['snippets']['total']}")
        
        if stats['patterns']['by_type']:
            print(f"\n📊 Pattern per tipo:")
            for ptype, count in stats['patterns']['by_type'].most_common(5):
                print(f"  • {ptype}: {count}")
        
        if stats['errors']['by_type']:
            print(f"\n❌ Errori per tipo:")
            for etype, count in stats['errors']['by_type'].most_common(5):
                print(f"  • {etype}: {count}")
        
        if stats['snippets']['most_used']:
            print(f"\n🔥 Snippet più usati:")
            for snippet_id, snippet in stats['snippets']['most_used']:
                print(f"  • {snippet['name']}: {snippet['used_count']} volte")
        
        return stats


def demo_integration():
    """Demo dell'integrazione"""
    
    print("=" * 60)
    print("VS CODE LEARNING INTEGRATION - Demo")
    print("=" * 60)
    
    integration = LearningIntegration()
    
    # Scenario 1: Monitora modifiche file
    print("\n1️⃣  Monitoraggio modifiche file Python")
    python_code = """
import pandas as pd
import numpy as np

def process_data(df):
    return df.dropna()

class DataProcessor:
    def __init__(self):
        pass
"""
    integration.monitor_file_changes("test.py", python_code)
    print("   ✓ Pattern appresi dal codice Python")
    
    # Scenario 2: Esecuzione comando
    print("\n2️⃣  Monitoraggio esecuzione comando")
    success, stdout, stderr = integration.monitor_command_execution(
        "python --version"
    )
    if success:
        print(f"   ✓ Comando eseguito: {stdout.strip()}")
    
    # Scenario 3: Gestione errore
    print("\n3️⃣  Gestione errore con suggerimento soluzione")
    integration.handle_error(
        error_type="ImportError",
        error_message="No module named 'pandas'",
        code_context="import pandas as pd",
        file_path="test.py"
    )
    
    # Aggiungi soluzione per test
    integration.learner.learn_error(
        error_type="ImportError",
        error_message="No module named 'pandas'",
        code_context="import pandas as pd",
        solution="pip install pandas"
    )
    
    # Ri-testa
    solution = integration.handle_error(
        error_type="ImportError",
        error_message="No module named 'pandas'",
        code_context="import pandas as pd"
    )
    
    # Scenario 4: Snippet suggestions
    print("\n4️⃣  Suggerimenti snippet")
    integration.learner.learn_snippet(
        name="Read CSV",
        code="df = pd.read_csv('file.csv')",
        language="python",
        description="Read CSV file with pandas",
        tags=["pandas", "csv", "data"]
    )
    
    snippets = integration.suggest_snippets("csv pandas", language="python")
    
    # Scenario 5: Raccomandazioni
    print("\n5️⃣  Raccomandazioni")
    integration.get_recommendations()
    
    # Scenario 6: Riepilogo giornaliero
    print("\n6️⃣  Riepilogo giornaliero")
    integration.daily_summary()
    
    print("\n✅ Demo completata!")


if __name__ == "__main__":
    demo_integration()
