"""
Demo SuperAgent con PowerShell Avanzato
"""

import sys
import io
from pathlib import Path

# Fix encoding per Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, '.')

from run_super_agent import SuperAgent


def demo_powershell_generation():
    """Demo generazione script PowerShell"""
    print("🤖 SUPER AGENT - POWERSHELL ADVANCED DEMO")
    print("=" * 80)
    
    agent = SuperAgent()
    
    # Test 1: Genera cmdlet
    print("\n📝 TEST 1: Generate PowerShell Cmdlet")
    print("-" * 80)
    
    script = agent.generate_powershell(
        "Get user information from Active Directory",
        script_type="cmdlet"
    )
    
    print(f"✅ Generated {len(script)} characters")
    print(f"\nPreview (first 600 chars):")
    print(script[:600])
    print("...")
    
    # Test 2: Analizza script
    print("\n\n🔍 TEST 2: Analyze PowerShell Script")
    print("-" * 80)
    
    analysis = agent.analyze_powershell(script)
    
    print(f"\n📊 Analysis Summary:")
    print(f"  Total Lines: {analysis['metrics']['total_lines']}")
    print(f"  Code Lines: {analysis['metrics']['code_lines']}")
    print(f"  Comment Ratio: {analysis['metrics']['comment_ratio']:.1%}")
    print(f"  Unique Cmdlets: {analysis['cmdlets']['unique']}")
    print(f"  Unique Variables: {analysis['variables']['unique']}")
    print(f"  Complexity: {analysis['complexity']['total']} ({analysis['complexity']['rating']})")
    
    if analysis['cmdlets']['top']:
        print(f"\n🏆 Top Cmdlets:")
        for cmdlet, count in analysis['cmdlets']['top'][:5]:
            print(f"  • {cmdlet}: {count} uses")
    
    if analysis['best_practices']:
        print(f"\n💡 Best Practices Issues:")
        for issue in analysis['best_practices'][:3]:
            print(f"  • {issue}")
    
    # Test 3: Genera function
    print("\n\n📝 TEST 3: Generate PowerShell Function")
    print("-" * 80)
    
    func_script = agent.generate_powershell(
        "Process log files in directory",
        script_type="function"
    )
    
    print(f"✅ Generated function: {len(func_script)} characters")
    print(f"\nPreview (first 500 chars):")
    print(func_script[:500])
    print("...")
    
    # Test 4: Genera script completo
    print("\n\n📝 TEST 4: Generate Complete PowerShell Script")
    print("-" * 80)
    
    full_script = agent.generate_powershell(
        "Backup files to remote location",
        script_type="script"
    )
    
    print(f"✅ Generated script with logging: {len(full_script)} characters")
    
    # Test 5: PowerShell Learning
    print("\n\n🧠 TEST 5: PowerShell Learning System")
    print("-" * 80)
    
    # Simula alcuni comandi
    test_commands = [
        "Get-Process | Where-Object {$_.CPU -gt 100}",
        "Get-Service -Name 'wuauserv' | Start-Service",
        "Get-ChildItem -Path C:\\Logs -Recurse -Filter *.log",
        "New-Item -Path C:\\Temp -ItemType Directory",
        "Test-Path C:\\Windows"
    ]
    
    for cmd in test_commands:
        agent.ps_learning.learn_command(cmd, context="demo", success=True)
    
    insights = agent.ps_learning.get_insights()
    
    print(f"\n📊 Learning Insights:")
    print(f"  Commands learned: {insights['summary']['total_commands_learned']}")
    print(f"  Success rate: {insights['summary']['success_rate']:.1f}%")
    
    if insights['top_cmdlets']:
        print(f"\n🏆 Top Cmdlets Learned:")
        for item in insights['top_cmdlets'][:5]:
            print(f"  • {item['cmdlet']}: {item['usage']} uses")
    
    if insights['top_verbs']:
        print(f"\n📝 Top Verbs:")
        for item in insights['top_verbs'][:5]:
            print(f"  • {item['verb']}: {item['usage']} uses")
    
    # Test 6: Suggestions
    print("\n\n💡 TEST 6: Command Suggestions")
    print("-" * 80)
    
    suggestions = agent.ps_learning.get_command_suggestions(verb="Get")
    
    if suggestions:
        print(f"\n🔍 Suggestions for 'Get-*' cmdlets:")
        for sug in suggestions[:3]:
            print(f"  • {sug['cmdlet']}: {sug['usage_count']} uses, {sug['success_rate']*100:.0f}% success")
    
    # Summary
    print("\n\n" + "=" * 80)
    print("✅ DEMO COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    
    print("\n📊 Capabilities Demonstrated:")
    print("  ✅ PowerShell Cmdlet Generation")
    print("  ✅ PowerShell Function Generation")
    print("  ✅ Complete Script Generation with logging")
    print("  ✅ Script Analysis (metrics, complexity, best practices)")
    print("  ✅ Learning from PowerShell commands")
    print("  ✅ Command suggestions and insights")
    
    print("\n🎯 Super Agent è pronto per:")
    print("  • Generare script PowerShell avanzati")
    print("  • Analizzare codice esistente")
    print("  • Apprendere dai comandi eseguiti")
    print("  • Suggerire best practices")
    print("  • Integrare Python e PowerShell")


if __name__ == "__main__":
    try:
        demo_powershell_generation()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
