"""
Test del sistema di autoapprendimento avanzato
"""
from core.learning import SelfLearningAgent, learn_from_execution, get_recommendation, get_learning_report
import time
import random

print("="*70)
print(" "*15 + "🎓 TEST SISTEMA AUTOAPPRENDIMENTO")
print("="*70)

agent = SelfLearningAgent()

# Test 1: Simulazione apprendimento
print("\n1️⃣  SIMULAZIONE APPRENDIMENTO DA ESPERIENZE")
print("-"*70)

# Simula varie esecuzioni di task
tasks = [
    ("read config file", "files", {"path": "config.json"}, 0.5, 0.9),
    ("search python docs", "browser", {"query": "python"}, 1.2, 0.8),
    ("list directory", "shell", {"cmd": "ls"}, 0.3, 0.95),
    ("read config file", "files", {"path": "config.json"}, 0.4, 0.95),
    ("search javascript docs", "browser", {"query": "js"}, 1.5, 0.7),
    ("read data file", "files", {"path": "data.txt"}, 0.6, 0.85),
    ("execute python script", "shell", {"cmd": "python test.py"}, 2.0, 0.6),
    ("read config file", "files", {"path": "config.json"}, 0.45, 0.95),
]

print("Simulazione di 8 esecuzioni...")
for task, tool, action, duration, success_prob in tasks:
    success = random.random() < success_prob
    outcome = "completed" if success else "failed"
    
    agent.learn_from_execution(
        task=task,
        tool=tool,
        action=action,
        outcome=outcome,
        success=success,
        duration=duration,
        context={'task_type': agent._classify_task(task)}
    )
    
    status = "✓" if success else "✗"
    print(f"  {status} {task} [{tool}] - {duration}s - {outcome}")

# Test 2: Metriche di performance
print("\n\n2️⃣  METRICHE DI PERFORMANCE")
print("-"*70)
print(f"Success Rate: {agent.metrics.get_overall_success_rate():.1%}")
print(f"Average Speed: {agent.metrics.get_average_speed():.2f}s")
print(f"Total Experiences: {len(agent.memory.experiences)}")
print(f"Patterns Learned: {len(agent.patterns.patterns)}")
print(f"\nTool Usage:")
for tool, count in agent.metrics.metrics['tool_usage'].items():
    reliability = agent.metrics.get_tool_reliability(tool)
    print(f"  {tool}: {count} uses (reliability: {reliability:.1%})")

# Test 3: Riconoscimento pattern
print("\n\n3️⃣  RICONOSCIMENTO PATTERN")
print("-"*70)
test_patterns = [
    ("file_operation", "files"),
    ("web_operation", "browser"),
    ("shell_operation", "shell")
]

for context, action in test_patterns:
    predicted = agent.patterns.predict_outcome(context, action)
    confidence = agent.patterns.get_confidence(context, action)
    if predicted:
        print(f"{context} + {action}:")
        print(f"  → Predicted: {predicted} (confidence: {confidence:.1%})")
    else:
        print(f"{context} + {action}: No pattern yet")

# Test 4: Memoria esperienze
print("\n\n4️⃣  MEMORIA ESPERIENZE")
print("-"*70)
similar = agent.memory.find_similar_experiences("read config file", limit=3)
print(f"Esperienze simili per 'read config file': {len(similar)}")
for i, exp in enumerate(similar, 1):
    print(f"  {i}. Tool: {exp['tool']}, Success: {exp['success']}, Duration: {exp['duration']}s")

success_rate = agent.memory.get_success_rate_for_task("read config file", "files")
print(f"\nSuccess rate per 'read config file' con 'files': {success_rate:.1%}")

best_tool, rate = agent.memory.get_best_tool_for_task("read config file")
print(f"Miglior tool per 'read config file': {best_tool} ({rate:.1%})")

# Test 5: Raccomandazioni intelligenti
print("\n\n5️⃣  RACCOMANDAZIONI INTELLIGENTI")
print("-"*70)
available_tools = ["files", "browser", "shell", "arduino"]

test_tasks = [
    "read config file",
    "search python tutorials",
    "execute system command"
]

for task in test_tasks:
    rec = agent.get_recommendation(task, available_tools)
    print(f"\nTask: {task}")
    print(f"  → Tool raccomandato: {rec['recommended_tool']}")
    print(f"  → Confidence: {rec['confidence']:.1%}")
    if rec['predicted_outcome']:
        print(f"  → Outcome previsto: {rec['predicted_outcome']}")
    print(f"  → Reasoning:")
    for reason in rec['reasoning']:
        print(f"     • {reason}")

# Test 6: Strategie adaptive
print("\n\n6️⃣  STRATEGIE ADAPTIVE")
print("-"*70)
agent.strategy.register_strategy("fast_execution", {"timeout": 5, "retries": 1})
agent.strategy.register_strategy("reliable_execution", {"timeout": 30, "retries": 3})

# Simula utilizzo strategie
agent.strategy.update_strategy_performance("fast_execution", True, 1.0)
agent.strategy.update_strategy_performance("fast_execution", True, 0.8)
agent.strategy.update_strategy_performance("reliable_execution", True, 3.0)
agent.strategy.update_strategy_performance("reliable_execution", False, 4.0)

print(f"Exploration Rate: {agent.strategy.exploration_rate:.1%}")
print(f"\nStrategie registrate:")
for name, data in agent.strategy.strategies.items():
    if data['uses'] > 0:
        success_rate = data['successes'] / data['uses']
        print(f"  {name}:")
        print(f"    Uses: {data['uses']}, Success: {success_rate:.1%}, Avg time: {data['avg_duration']:.2f}s")

selected = agent.strategy.select_strategy("file_operation")
print(f"\nStrategia selezionata per file_operation: {selected}")

# Test 7: Report di apprendimento
print("\n\n7️⃣  REPORT APPRENDIMENTO")
print("-"*70)
report = agent.get_learning_report()
print(f"Overall Success Rate: {report['overall_success_rate']:.1%}")
print(f"Average Speed: {report['average_speed']:.2f}s")
print(f"Total Experiences: {report['total_experiences']}")
print(f"Patterns Learned: {report['patterns_learned']}")
print(f"Exploration Rate: {report['exploration_rate']:.1%}")

print(f"\nTop Tools:")
for tool, score in report['most_reliable_tools']:
    print(f"  {tool}: {score:.2f}")

print(f"\nAree di miglioramento:")
for area in report['improvement_areas']:
    print(f"  • {area}")

# Test 8: Persistenza dati
print("\n\n8️⃣  PERSISTENZA DATI DI APPRENDIMENTO")
print("-"*70)
save_path = "test_files/learning_data.json"
agent.save_learning_data(save_path)
print(f"✓ Dati salvati in: {save_path}")

# Carica in un nuovo agente
new_agent = SelfLearningAgent()
success = new_agent.load_learning_data(save_path)
if success:
    print(f"✓ Dati caricati con successo")
    print(f"  Esperienze ripristinate: {len(new_agent.memory.experiences)}")
    print(f"  Pattern ripristinati: {len(new_agent.patterns.patterns)}")
    print(f"  Success rate: {new_agent.metrics.get_overall_success_rate():.1%}")

# Test 9: Miglioramento continuo
print("\n\n9️⃣  SIMULAZIONE MIGLIORAMENTO CONTINUO")
print("-"*70)
print("Prima fase - Performance iniziale:")
initial_success = agent.metrics.get_overall_success_rate()
print(f"  Success rate: {initial_success:.1%}")
print(f"  Exploration rate: {agent.strategy.exploration_rate:.1%}")

# Simula più esperienze di successo
print("\nAggiunta di 10 nuove esperienze positive...")
for i in range(10):
    agent.learn_from_execution(
        task="optimized task",
        tool="files",
        action={"optimized": True},
        outcome="completed",
        success=True,
        duration=0.3,
        context={'task_type': 'file_operation'}
    )

print("\nDopo apprendimento:")
final_success = agent.metrics.get_overall_success_rate()
print(f"  Success rate: {final_success:.1%} ({(final_success-initial_success)*100:+.1f}%)")
print(f"  Exploration rate: {agent.strategy.exploration_rate:.1%}")
print(f"  Total experiences: {len(agent.memory.experiences)}")

improvement = (final_success - initial_success) / initial_success * 100
print(f"\n🎯 Miglioramento: {improvement:+.1f}%")

print("\n" + "="*70)
print("✅ TUTTI I TEST COMPLETATI!")
print("\n🎓 CAPACITÀ DI AUTOAPPRENDIMENTO:")
print("  • Tracking metriche performance in tempo reale")
print("  • Riconoscimento pattern automatico")
print("  • Memoria esperienze con indici ottimizzati")
print("  • Raccomandazioni intelligenti basate su esperienza")
print("  • Strategie adaptive con exploration/exploitation")
print("  • Predizione outcome con confidence score")
print("  • Report apprendimento dettagliati")
print("  • Persistenza e ripristino stato")
print("  • Identificazione aree di miglioramento")
print("  • Miglioramento continuo automatico")
print("="*70)
