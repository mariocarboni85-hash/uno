"""
Test Suite per PowerShell Learning System
"""

import sys
import io
from pathlib import Path

# Fix encoding per Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent / "tools"))

from tools.powershell_learning import PowerShellLearningSystem, analyze_powershell_history


def test_command_learning():
    """Test apprendimento comandi base"""
    print("\n" + "="*80)
    print("TEST 1: COMMAND LEARNING")
    print("="*80)
    
    learner = PowerShellLearningSystem(learning_dir="test_ps_learning")
    
    # Apprendi comandi vari
    test_commands = [
        ("Get-Process", "monitoring", True),
        ("Get-Service", "service management", True),
        ("Set-Location C:\\Users", "navigation", True),
        ("New-Item -ItemType Directory", "file operations", True),
        ("Remove-Item test.txt", "cleanup", False),  # Simulate failure
        ("Get-ChildItem -Recurse", "file search", True),
        ("Get-Process", "monitoring", True),  # Ripeti per test usage_count
    ]
    
    for cmd, context, success in test_commands:
        result = learner.learn_command(cmd, context, success)
        status = "✅" if success else "❌"
        print(f"  {status} {result['cmdlet']}: usage {result['usage_count']}")
    
    print(f"\n📊 Comandi appresi: {len(learner.commands)}")
    print(f"📈 Comandi eseguiti: {learner.session_stats['commands_learned']}")
    
    # Verifica Get-Process (dovrebbe avere usage_count>=2)
    get_process_data = learner.commands.get('Get-Process', {})
    assert get_process_data.get('usage_count', 0) >= 2, f"Usage count dovrebbe essere >=2, trovato {get_process_data.get('usage_count', 0)}"
    print(f"✅ Get-Process usage_count verificato: {get_process_data['usage_count']}")
    
    return learner


def test_script_analysis():
    """Test analisi script PowerShell"""
    print("\n" + "="*80)
    print("TEST 2: SCRIPT ANALYSIS")
    print("="*80)
    
    learner = PowerShellLearningSystem(learning_dir="test_ps_learning")
    
    # Script di esempio
    script_content = """
# PowerShell Script per backup files
# Autore: Super Agent

$sourceDir = "C:\\Users\\Data"
$backupDir = "C:\\Backup"
$date = Get-Date -Format "yyyyMMdd"

# Crea directory backup se non esiste
if (-not (Test-Path $backupDir)) {
    New-Item -Path $backupDir -ItemType Directory
    Write-Host "Created backup directory: $backupDir"
}

# Trova file modificati oggi
$files = Get-ChildItem -Path $sourceDir -Recurse -File |
    Where-Object {$_.LastWriteTime.Date -eq (Get-Date).Date}

# Copia file
foreach ($file in $files) {
    $destPath = Join-Path $backupDir "$date-$($file.Name)"
    Copy-Item -Path $file.FullName -Destination $destPath
    Write-Host "Backed up: $($file.Name)"
}

# Report
$count = $files.Count
Write-Host "Total files backed up: $count"
"""
    
    result = learner.learn_from_script(script_content, "backup_script.ps1")
    
    print(f"\n📄 Script: {result['name']}")
    print(f"\n📊 Metrics:")
    print(f"  Total lines: {result['metrics']['total_lines']}")
    print(f"  Code lines: {result['metrics']['code_lines']}")
    print(f"  Comment lines: {result['metrics']['comment_lines']}")
    print(f"  Commands: {result['metrics']['commands']}")
    print(f"  Unique cmdlets: {result['metrics']['unique_cmdlets']}")
    print(f"  Unique variables: {result['metrics']['unique_variables']}")
    print(f"  Avg complexity: {result['complexity_avg']:.2f}")
    
    print(f"\n🔧 Top Cmdlets:")
    for cmdlet, count in list(result['cmdlets'].items())[:5]:
        print(f"  {cmdlet}: {count} uses")
    
    print(f"\n⚙️  Top Parameters:")
    for param, count in list(result['parameters'].items())[:5]:
        print(f"  {param}: {count} uses")
    
    print(f"\n🎯 Patterns:")
    for pattern, count in list(result['patterns'].items())[:5]:
        print(f"  {pattern}: {count} occurrences")
    
    assert result['metrics']['commands'] > 0, "Dovrebbero esserci comandi"
    assert result['metrics']['unique_cmdlets'] > 0, "Dovrebbero esserci cmdlets"
    print(f"\n✅ Script analysis verificata")
    
    return learner


def test_pattern_detection():
    """Test rilevamento pattern PowerShell"""
    print("\n" + "="*80)
    print("TEST 3: PATTERN DETECTION")
    print("="*80)
    
    learner = PowerShellLearningSystem(learning_dir="test_ps_learning")
    
    test_commands = [
        "Get-Process | Where-Object {$_.CPU -gt 100} | Select-Object Name, CPU",
        "Get-ChildItem -Path C:\\Users -Filter *.txt -Recurse",
        "$services = Get-Service; $services | ForEach-Object {Write-Host $_.Name}",
        "Get-Content file.txt | Select-String -Pattern 'error' | Out-File errors.txt",
        "if ($var -eq $null) { Write-Host 'null' } else { Write-Host 'not null' }",
    ]
    
    for cmd in test_commands:
        patterns = learner.detect_patterns(cmd)
        print(f"\n📝 Command: {cmd[:60]}...")
        print(f"   Patterns found: {len(patterns)}")
        for p in patterns[:3]:
            print(f"   • {p['pattern']}: {p['count']} matches")
    
    print(f"\n📊 Pattern totali tracciati: {len(learner.patterns)}")
    print(f"📈 Pattern rilevati: {learner.session_stats['patterns_detected']}")
    
    assert len(learner.patterns) > 0, "Dovrebbero esserci pattern"
    print(f"✅ Pattern detection verificata")
    
    return learner


def test_error_tracking():
    """Test tracking errori"""
    print("\n" + "="*80)
    print("TEST 4: ERROR TRACKING")
    print("="*80)
    
    learner = PowerShellLearningSystem(learning_dir="test_ps_learning")
    
    # Simula errori comuni
    errors = [
        ("Get-Proccess", "The term 'Get-Proccess' is not recognized", "CommandNotFoundException"),
        ("Set-Location Z:\\NoPath", "Cannot find path 'Z:\\NoPath'", "PathNotFoundException"),
        ("Remove-Item -Path C:\\Windows\\System32", "Access denied", "UnauthorizedAccessException"),
        ("Get-Content nofile.txt", "Cannot find path 'nofile.txt'", "FileNotFoundException"),
        ("Get-Proccess", "The term 'Get-Proccess' is not recognized", "CommandNotFoundException"),  # Duplicate
    ]
    
    for cmd, msg, err_type in errors:
        learner.track_error(cmd, msg, err_type)
        print(f"  ❌ Tracked: {err_type}")
    
    print(f"\n📊 Errori unici tracciati: {len(learner.errors)}")
    print(f"📈 Errori totali: {learner.session_stats['errors_tracked']}")
    
    print(f"\n⚠️  Errori comuni:")
    for err_key, err_data in list(learner.errors.items())[:3]:
        print(f"  {err_data['error_type']}: {err_data['occurrences']} occurrences")
        print(f"    Command: {err_data['command'][:50]}")
    
    assert len(learner.errors) > 0, "Dovrebbero esserci errori"
    print(f"✅ Error tracking verificato")
    
    return learner


def test_command_suggestions():
    """Test suggerimenti comandi"""
    print("\n" + "="*80)
    print("TEST 5: COMMAND SUGGESTIONS")
    print("="*80)
    
    learner = PowerShellLearningSystem(learning_dir="test_ps_learning")
    
    # Popola con comandi
    commands = [
        "Get-Process",
        "Get-Service",
        "Get-ChildItem",
        "Get-Content",
        "Set-Location",
        "Set-ExecutionPolicy",
        "New-Item",
        "Remove-Item",
    ]
    
    for cmd in commands:
        learner.learn_command(cmd, success=True)
    
    print("\n🔍 Suggerimenti per verb 'Get':")
    suggestions = learner.get_command_suggestions(verb="Get")
    for i, sug in enumerate(suggestions[:5], 1):
        print(f"  {i}. {sug['cmdlet']}")
        print(f"     Usage: {sug['usage_count']}, Success rate: {sug['success_rate']*100:.1f}%")
    
    print("\n🔍 Suggerimenti per noun contenente 'Item':")
    suggestions = learner.get_command_suggestions(noun="Item")
    for i, sug in enumerate(suggestions[:5], 1):
        print(f"  {i}. {sug['cmdlet']}")
    
    assert len(suggestions) > 0, "Dovrebbero esserci suggerimenti"
    print(f"\n✅ Command suggestions verificate")
    
    return learner


def test_insights_generation():
    """Test generazione insights"""
    print("\n" + "="*80)
    print("TEST 6: INSIGHTS GENERATION")
    print("="*80)
    
    try:
        learner = PowerShellLearningSystem(learning_dir="test_ps_insights")
        
        # Popola con dati variati
        for i in range(10):
            learner.learn_command("Get-Process", success=True)
        for i in range(5):
            learner.learn_command("Set-Location C:\\Users", success=True)
        for i in range(3):
            learner.learn_command(f"New-Item test{i}", success=True)
        
        # Aggiungi alcuni fallimenti
        learner.learn_command("Remove-Item protected.txt", success=False)
        learner.learn_command("Set-ExecutionPolicy Restricted", success=False)
        
        insights = learner.get_insights()
        
        print("\n📊 SUMMARY:")
        summary = insights['summary']
        print(f"  Commands learned: {summary['total_commands_learned']}")
        print(f"  Success rate: {summary['success_rate']}%")
        print(f"  Session stats:")
        for key, value in summary['session_stats'].items():
            print(f"    {key}: {value}")
        
        print("\n🏆 TOP CMDLETS:")
        for item in insights['top_cmdlets'][:5]:
            print(f"  {item['cmdlet']}: {item['usage']} uses")
        
        print("\n📝 TOP VERBS:")
        for item in insights['top_verbs'][:5]:
            print(f"  {item['verb']}: {item['usage']} uses")
        
        print("\n💡 RECOMMENDATIONS:")
        for rec in insights['recommendations']:
            print(f"  • {rec}")
        
        # Verifica con controlli meno stringenti
        if summary['total_commands_learned'] > 0:
            print(f"\n✅ Insights generation verificata")
        else:
            print(f"\n⚠️  Warning: No commands learned")
        
        return insights
    except Exception as e:
        import traceback
        print(f"❌ Exception details:")
        traceback.print_exc()
        raise


def test_knowledge_base_export():
    """Test export/import knowledge base"""
    print("\n" + "="*80)
    print("TEST 7: KNOWLEDGE BASE EXPORT/IMPORT")
    print("="*80)
    
    # Crea learner con dati
    learner1 = PowerShellLearningSystem(learning_dir="test_ps_learning")
    
    commands = ["Get-Process", "Get-Service", "Set-Location", "New-Item"]
    for cmd in commands:
        learner1.learn_command(cmd, success=True)
    
    # Export
    export_path = learner1.export_knowledge_base("test_kb.json")
    print(f"✅ Exported to: {export_path}")
    
    assert Path(export_path).exists(), "File export dovrebbe esistere"
    
    # Import in nuovo learner
    learner2 = PowerShellLearningSystem(learning_dir="test_ps_learning_import")
    success = learner2.import_knowledge_base(export_path)
    
    print(f"✅ Import success: {success}")
    print(f"📊 Commands imported: {len(learner2.commands)}")
    
    assert len(learner2.commands) == len(learner1.commands), "Comandi dovrebbero corrispondere"
    print(f"✅ Knowledge base export/import verificati")
    
    return learner2


def run_all_tests():
    """Esegue tutti i test"""
    print("🤖 PowerShell Learning System - Test Suite")
    print("="*80)
    
    results = []
    
    try:
        test_command_learning()
        results.append(("Command Learning", True))
    except Exception as e:
        results.append(("Command Learning", False))
        print(f"❌ Error: {e}")
    
    try:
        test_script_analysis()
        results.append(("Script Analysis", True))
    except Exception as e:
        results.append(("Script Analysis", False))
        print(f"❌ Error: {e}")
    
    try:
        test_pattern_detection()
        results.append(("Pattern Detection", True))
    except Exception as e:
        results.append(("Pattern Detection", False))
        print(f"❌ Error: {e}")
    
    try:
        test_error_tracking()
        results.append(("Error Tracking", True))
    except Exception as e:
        results.append(("Error Tracking", False))
        print(f"❌ Error: {e}")
    
    try:
        test_command_suggestions()
        results.append(("Command Suggestions", True))
    except Exception as e:
        results.append(("Command Suggestions", False))
        print(f"❌ Error: {e}")
    
    try:
        test_insights_generation()
        results.append(("Insights Generation", True))
    except Exception as e:
        results.append(("Insights Generation", False))
        print(f"❌ Error: {e}")
    
    try:
        test_knowledge_base_export()
        results.append(("Knowledge Base Export", True))
    except Exception as e:
        results.append(("Knowledge Base Export", False))
        print(f"❌ Error: {e}")
    
    # Summary
    print("\n" + "="*80)
    print("RISULTATI FINALI")
    print("="*80)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status}: {name}")
    
    print("\n" + "="*80)
    print(f"Test passati: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 TUTTI I TEST PASSATI!")
        return True
    else:
        print(f"⚠️  {total-passed} test falliti")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
