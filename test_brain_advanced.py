"""
Test del cervello potenziato del SuperAgent
"""
from core.brain import Brain, Memory, think, analyze_task, reason

print("="*70)
print(" "*20 + "🧠 TEST BRAIN AVANZATO")
print("="*70)

brain = Brain()

# Test 1: Memory System
print("\n1️⃣  TEST SISTEMA MEMORIA")
print("-"*70)
brain.memory.add_interaction('user', 'Come ti chiami?')
brain.memory.add_interaction('assistant', 'Sono SuperAgent')
brain.memory.store_knowledge('agent_name', 'SuperAgent')
brain.memory.store_knowledge('version', '2.0')

print("✓ Interazioni memorizzate:", len(brain.memory.short_term))
print("✓ Conoscenze memorizzate:", len(brain.memory.long_term))
print("\nContesto attuale:")
print(brain.memory.get_context())

# Test 2: Task Analysis
print("\n\n2️⃣  TEST ANALISI TASK")
print("-"*70)
tasks = [
    "Read a file from disk and analyze its content",
    "Search the web for Python tutorials",
    "Execute a shell command to list files",
    "Calculate the factorial of 10"
]

for task in tasks:
    analysis = brain.analyze_task(task)
    print(f"\n📋 Task: {task}")
    print(f"   Tipo: {analysis['task_type']}")
    print(f"   Complessità: {analysis['complexity']}")
    print(f"   Tool richiesti: {', '.join(analysis['required_tools']) if analysis['required_tools'] else 'nessuno'}")
    print(f"   Step stimati: {analysis['estimated_steps']}")

# Test 3: Reasoning
print("\n\n3️⃣  TEST RAGIONAMENTO")
print("-"*70)
problem = "The agent needs to analyze stock data. Which approach is best?"
options = [
    "Download CSV file and parse it locally",
    "Use API to fetch real-time data",
    "Scrape website for data",
    "Use pre-downloaded dataset"
]

selected, confidence = brain.reason(problem, options)
print(f"Problema: {problem}")
print(f"Opzioni disponibili: {len(options)}")
print(f"✓ Opzione selezionata: {selected}")
print(f"✓ Confidenza: {confidence:.0%}")

# Test 4: Multi-model Thinking
print("\n\n4️⃣  TEST MULTI-MODEL THINKING")
print("-"*70)

# Test con Ollama (locale)
print("\n🤖 Ollama (locale):")
response = brain.think("What is 2+2?", model='ollama', use_memory=False)
print(f"   Risposta: {response[:100]}...")

# Test con local reasoning
print("\n💡 Local reasoning:")
response = brain.think("Create a file called test.txt", model='local', use_memory=False)
print(f"   Risposta: {response}")

# Test 5: Learning from Outcomes
print("\n\n5️⃣  TEST APPRENDIMENTO")
print("-"*70)
brain.learn_from_outcome('file_write', 'success', True)
brain.learn_from_outcome('file_write', 'success', True)
brain.learn_from_outcome('file_write', 'error', False)

stats = brain.memory.retrieve_knowledge('action_file_write')
print(f"Statistiche 'file_write':")
print(f"   ✓ Successi: {stats['successes']}")
print(f"   ✗ Fallimenti: {stats['failures']}")
print(f"   Ultimo esito: {stats['last_outcome']}")

# Test 6: Tool Recommendation
print("\n\n6️⃣  TEST RACCOMANDAZIONE TOOL")
print("-"*70)
test_tasks = [
    "Save JSON data to a file",
    "Search for Python documentation online",
    "Run a Python script"
]

for task in test_tasks:
    tools = brain.get_tool_recommendation(task)
    print(f"Task: {task}")
    print(f"   → Tool raccomandati: {', '.join(tools) if tools else 'nessuno'}")

# Test 7: Context-aware Thinking
print("\n\n7️⃣  TEST PENSIERO CON CONTESTO")
print("-"*70)
brain.memory.clear_short_term()
brain.memory.add_interaction('user', 'My name is Mario')
brain.memory.add_interaction('assistant', 'Nice to meet you, Mario!')

response = brain.think("What is my name?", model='local', use_memory=True)
print(f"Domanda con contesto: 'What is my name?'")
print(f"Risposta: {response}")

# Test 8: Memory Persistence
print("\n\n8️⃣  TEST PERSISTENZA MEMORIA")
print("-"*70)
memory_file = "test_files/brain_memory.json"
brain.memory.save_to_file(memory_file)
print(f"✓ Memoria salvata in: {memory_file}")

new_brain = Brain()
new_brain.memory.load_from_file(memory_file)
print(f"✓ Memoria caricata: {len(new_brain.memory.short_term)} interazioni, {len(new_brain.memory.long_term)} conoscenze")

print("\n" + "="*70)
print("✅ TUTTI I TEST COMPLETATI!")
print("\n🧠 CAPACITÀ DEL CERVELLO POTENZIATO:")
print("  • Sistema di memoria (short-term e long-term)")
print("  • Analisi automatica task con classificazione")
print("  • Ragionamento e selezione opzioni")
print("  • Multi-model support (OpenAI, Ollama, Local)")
print("  • Apprendimento da risultati")
print("  • Raccomandazione tool intelligente")
print("  • Pensiero context-aware")
print("  • Persistenza memoria su file")
print("  • Confidence scoring")
print("  • Pattern recognition")
print("="*70)
