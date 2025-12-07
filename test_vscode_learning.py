"""
Test suite per VS Code Learning System
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tools.vscode_learning import VSCodeLearningSystem, quick_learn_pattern, get_insights
from pathlib import Path
import json
import shutil


def test_vscode_learning():
    """Test del sistema di apprendimento VS Code"""
    
    print("=" * 60)
    print("TEST VS CODE LEARNING SYSTEM")
    print("=" * 60)
    
    # Setup test environment
    test_dir = Path("test_learning_workspace")
    test_dir.mkdir(exist_ok=True)
    
    learner = VSCodeLearningSystem(str(test_dir))
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Apprendimento pattern
    print("\n[1/12] Test apprendimento pattern...")
    try:
        pattern_id = learner.learn_code_pattern(
            code="def hello_world():\n    print('Hello!')",
            pattern_type="function",
            context="greeting function",
            success=True,
            metadata={"complexity": "simple"}
        )
        
        assert pattern_id in learner.patterns
        assert learner.patterns[pattern_id]["success_count"] == 1
        
        print(f"  ✓ Pattern appreso: {pattern_id}")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Errore: {e}")
        tests_failed += 1
    
    # Test 2: Pattern multipli dello stesso tipo
    print("\n[2/12] Test pattern ripetuti...")
    try:
        # Apprendi lo stesso pattern 3 volte
        for i in range(3):
            learner.learn_code_pattern(
                code="import pandas as pd",
                pattern_type="import",
                success=True
            )
        
        # Trova il pattern
        pattern = next(p for p in learner.patterns.values() if "pandas" in p["code"])
        assert pattern["occurrences"] == 3
        
        print(f"  ✓ Pattern ripetuto 3 volte registrato correttamente")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Errore: {e}")
        tests_failed += 1
    
    # Test 3: Recupero pattern simili
    print("\n[3/12] Test recupero pattern simili...")
    try:
        similar = learner.get_similar_patterns("function", min_success_rate=0.5)
        
        assert len(similar) > 0
        assert all("success_rate" in p for p in similar)
        
        print(f"  ✓ Trovati {len(similar)} pattern simili")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Errore: {e}")
        tests_failed += 1
    
    # Test 4: Apprendimento errori
    print("\n[4/12] Test apprendimento errori...")
    try:
        error_id = learner.learn_error(
            error_type="TypeError",
            error_message="unsupported operand type(s) for +: 'int' and 'str'",
            code_context="x = 5 + '10'",
            solution="x = 5 + int('10')"
        )
        
        assert error_id in learner.errors
        assert len(learner.errors[error_id]["solutions"]) == 1
        
        print(f"  ✓ Errore registrato: {error_id}")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Errore: {e}")
        tests_failed += 1
    
    # Test 5: Recupero soluzione errore
    print("\n[5/12] Test recupero soluzione errore...")
    try:
        solution = learner.get_error_solution("TypeError", "unsupported operand")
        
        assert solution is not None
        assert "int(" in solution
        
        print(f"  ✓ Soluzione recuperata: {solution[:50]}...")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Errore: {e}")
        tests_failed += 1
    
    # Test 6: Apprendimento comandi
    print("\n[6/12] Test apprendimento comandi...")
    try:
        learner.learn_command(
            command="python test.py",
            command_type="terminal",
            output="Success",
            success=True,
            execution_time=1.5
        )
        
        learner.learn_command(
            command="npm install",
            command_type="terminal",
            output="Error",
            success=False,
            execution_time=3.2
        )
        
        assert len(learner.commands) >= 2
        
        history = learner.get_command_history(command_type="terminal")
        assert len(history) >= 2
        
        print(f"  ✓ {len(history)} comandi registrati")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Errore: {e}")
        tests_failed += 1
    
    # Test 7: Comandi più usati
    print("\n[7/12] Test comandi più usati...")
    try:
        # Aggiungi più comandi
        for i in range(5):
            learner.learn_command(
                command="pytest",
                command_type="terminal",
                output="OK",
                success=True
            )
        
        most_used = learner.get_most_used_commands(limit=5)
        assert len(most_used) > 0
        assert most_used[0][0] == "pytest"
        assert most_used[0][1] >= 5
        
        print(f"  ✓ Comando più usato: {most_used[0][0]} ({most_used[0][1]} volte)")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Errore: {e}")
        tests_failed += 1
    
    # Test 8: Apprendimento snippet
    print("\n[8/12] Test apprendimento snippet...")
    try:
        learner.learn_snippet(
            name="async fetch",
            code="async def fetch(url):\n    async with aiohttp.ClientSession() as session:\n        async with session.get(url) as resp:\n            return await resp.text()",
            language="python",
            description="Async HTTP fetch",
            tags=["async", "http", "aiohttp"]
        )
        
        assert len(learner.snippets) > 0
        
        # Cerca snippet
        results = learner.search_snippets("async", language="python")
        assert len(results) > 0
        
        print(f"  ✓ Snippet salvato e trovato nella ricerca")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Errore: {e}")
        tests_failed += 1
    
    # Test 9: Uso snippet
    print("\n[9/12] Test uso snippet...")
    try:
        snippet_id = list(learner.snippets.keys())[0]
        initial_count = learner.snippets[snippet_id].get("used_count", 0)
        
        snippet = learner.get_snippet(snippet_id)
        assert snippet is not None
        assert snippet["used_count"] == initial_count + 1
        
        print(f"  ✓ Snippet usato, counter incrementato: {snippet['used_count']}")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Errore: {e}")
        tests_failed += 1
    
    # Test 10: Preferenze
    print("\n[10/12] Test apprendimento preferenze...")
    try:
        learner.learn_preference("editor", "tab_size", 4)
        learner.learn_preference("editor", "font_size", 14)
        learner.learn_preference("terminal", "shell", "bash")
        
        tab_size = learner.get_preference("editor", "tab_size")
        assert tab_size == 4
        
        all_prefs = learner.get_all_preferences()
        assert "editor" in all_prefs
        assert "terminal" in all_prefs
        
        print(f"  ✓ {len(all_prefs)} categorie di preferenze salvate")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Errore: {e}")
        tests_failed += 1
    
    # Test 11: Generazione insights
    print("\n[11/12] Test generazione insights...")
    try:
        insights = learner.generate_insights()
        
        assert "summary" in insights
        assert "patterns" in insights["summary"]
        assert "errors" in insights["summary"]
        assert "commands" in insights["summary"]
        
        print(f"  ✓ Insights generati:")
        print(f"     • Pattern: {insights['summary']['patterns']['total']}")
        print(f"     • Errori: {insights['summary']['errors']['unique_errors']}")
        print(f"     • Comandi: {insights['summary']['commands']['total_executed']}")
        
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Errore: {e}")
        tests_failed += 1
    
    # Test 12: Export/Import knowledge base
    print("\n[12/12] Test export/import knowledge base...")
    try:
        # Export
        export_file = test_dir / "knowledge_export.json"
        exported = learner.export_knowledge_base(str(export_file))
        
        assert Path(exported).exists()
        
        # Verifica contenuto
        with open(exported, 'r') as f:
            kb = json.load(f)
        
        assert "patterns" in kb
        assert "errors" in kb
        assert "snippets" in kb
        assert "stats" in kb
        
        print(f"  ✓ Knowledge base esportata: {Path(exported).name}")
        print(f"     • Size: {Path(exported).stat().st_size} bytes")
        
        # Test import
        learner2 = VSCodeLearningSystem(str(test_dir / "test2"))
        learner2.import_knowledge_base(exported)
        
        assert len(learner2.patterns) > 0
        assert len(learner2.errors) > 0
        
        print(f"  ✓ Knowledge base importata in nuovo learner")
        
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Errore: {e}")
        tests_failed += 1
    
    # Statistiche finali
    print("\n" + "=" * 60)
    print("STATISTICHE APPRENDIMENTO")
    print("=" * 60)
    stats = learner.get_learning_stats()
    print(f"Pattern totali: {stats['patterns']['total']}")
    print(f"Errori registrati: {stats['errors']['total']}")
    print(f"Comandi eseguiti: {stats['commands']['total']}")
    print(f"Snippets salvati: {stats['snippets']['total']}")
    print(f"Categorie preferenze: {stats['preferences']['categories']}")
    
    # Cleanup
    print("\n" + "=" * 60)
    print("CLEANUP")
    print("=" * 60)
    try:
        shutil.rmtree(test_dir)
        print("✓ Test directory rimossa")
    except Exception as e:
        print(f"⚠ Impossibile rimuovere test directory: {e}")
    
    # Riepilogo
    print("\n" + "=" * 60)
    print("RIEPILOGO TEST")
    print("=" * 60)
    print(f"✓ Test passati: {tests_passed}/12")
    print(f"✗ Test falliti: {tests_failed}/12")
    
    if tests_failed == 0:
        print("\n🎉 Tutti i test sono passati!")
    else:
        print(f"\n⚠️  {tests_failed} test falliti")
    
    return tests_failed == 0


if __name__ == "__main__":
    success = test_vscode_learning()
    sys.exit(0 if success else 1)
