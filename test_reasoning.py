"""
Test sistema di ragionamento avanzato
"""
from core.reasoning import (AdvancedReasoner, ReasoningType, LogicalReasoner, 
                            CausalReasoner, ProblemDecomposer, reason, explain_reasoning)

print("="*70)
print(" "*15 + "🧠 TEST RAGIONAMENTO AVANZATO")
print("="*70)

reasoner = AdvancedReasoner()

# Test 1: Decomposizione problemi
print("\n1️⃣  DECOMPOSIZIONE PROBLEMI")
print("-"*70)

complex_problems = [
    "Read config file and then analyze data and create report",
    "If the file exists then read it and process the content",
    "Search for Python tutorials and download examples and test the code"
]

decomposer = ProblemDecomposer()
for problem in complex_problems:
    subproblems = decomposer.decompose(problem)
    print(f"\nProblema: {problem}")
    print(f"Subproblemi identificati: {len(subproblems)}")
    for sub in subproblems:
        deps = f" (dipende da {sub['dependencies']})" if sub['dependencies'] else ""
        print(f"  {sub['id']}. [{sub['type']}] {sub['description']}{deps}")

# Test 2: Ragionamento logico deduttivo
print("\n\n2️⃣  RAGIONAMENTO LOGICO DEDUTTIVO")
print("-"*70)

logical = LogicalReasoner()

# Aggiungi regole logiche
logical.add_rule("file_exists", "can_read_file", confidence=0.95)
logical.add_rule("can_read_file", "can_analyze_data", confidence=0.9)
logical.add_rule("has_data", "can_create_report", confidence=0.85)

# Aggiungi fatti
logical.add_fact("file_exists")
logical.add_fact("has_data")

# Deduzioni
goals = ["can_read_file", "can_analyze_data", "can_create_report"]

print("Regole e fatti configurati\n")
for goal in goals:
    is_true, confidence, path = logical.deduce(goal)
    print(f"Goal: {goal}")
    print(f"  Risultato: {'✓ Vero' if is_true else '✗ Falso'} (confidence: {confidence:.1%})")
    if path:
        print(f"  Ragionamento:")
        for step in path:
            print(f"    • {step}")
    print()

# Test 3: Ragionamento abduttivo
print("\n3️⃣  RAGIONAMENTO ABDUTTIVO (Migliore Spiegazione)")
print("-"*70)

logical.add_rule("network_error", "connection_failed", confidence=0.8)
logical.add_rule("server_down", "connection_failed", confidence=0.9)
logical.add_rule("wrong_credentials", "connection_failed", confidence=0.7)

observation = "connection_failed"
explanations = logical.abductive_reasoning(observation)

print(f"Osservazione: {observation}")
print(f"Possibili spiegazioni:")
for explanation, conf in explanations:
    print(f"  • {explanation} (confidence: {conf:.1%})")

# Test 4: Ragionamento causale
print("\n\n4️⃣  RAGIONAMENTO CAUSALE")
print("-"*70)

causal = CausalReasoner()

# Costruisci grafo causale
causal.add_causal_link("high_load", "slow_response", strength=0.9)
causal.add_causal_link("high_load", "memory_issues", strength=0.7)
causal.add_causal_link("memory_issues", "crashes", strength=0.85)
causal.add_causal_link("slow_response", "user_complaints", strength=0.8)

print("Grafo causale costruito\n")

# Predici effetti
cause = "high_load"
effects = causal.predict_effects(cause)
print(f"Causa: {cause}")
print(f"Effetti previsti:")
for effect, strength in effects:
    print(f"  → {effect} (strength: {strength:.1%})")

# Trova cause
print(f"\nEffetto: crashes")
causes = causal.find_causes("crashes")
print(f"Possibili cause:")
for cause, strength in causes:
    print(f"  ← {cause} (strength: {strength:.1%})")

# Catene causali
print(f"\nCatena causale da 'high_load' a 'crashes':")
chains = causal.causal_chain("high_load", "crashes")
for i, chain in enumerate(chains, 1):
    print(f"  {i}. {' → '.join(chain)}")

# Test 5: Ragionamento completo su problema
print("\n\n5️⃣  RAGIONAMENTO COMPLETO")
print("-"*70)

problem = "Analyze log files and identify errors and create summary report"
chain = reasoner.reason(problem)

print(chain.get_chain_summary())

# Test 6: Analisi What-If
print("\n\n6️⃣  ANALISI WHAT-IF")
print("-"*70)

reasoner.causal.add_causal_link("increase_cache", "faster_response", strength=0.85)
reasoner.causal.add_causal_link("increase_cache", "higher_memory_usage", strength=0.9)

scenario = "Current system performance"
changes = {
    "increase_cache": True,
    "high_load": True
}

results = reasoner.what_if_analysis(scenario, changes)
print(f"Scenario: {results['scenario']}")
print(f"Modifiche: {results['changes']}")
print(f"\nRisultati previsti:")
for outcome in results['predicted_outcomes']:
    print(f"  • {outcome['effect']} (likelihood: {outcome['likelihood']:.1%})")
    print(f"    Reasoning: {outcome['reasoning']}")

# Test 7: Comparazione opzioni
print("\n\n7️⃣  COMPARAZIONE OPZIONI")
print("-"*70)

options = [
    {"name": "Solution A", "fast": True, "reliable": True, "cost": "high"},
    {"name": "Solution B", "fast": True, "reliable": False, "cost": "low"},
    {"name": "Solution C", "fast": False, "reliable": True, "cost": "medium"}
]

criteria = ["fast", "reliable"]

comparison = reasoner.compare_options(options, criteria)
print("Criteri di valutazione:", criteria)
print("\nComparazione:")
for comp in comparison['comparisons']:
    print(f"\n{comp['option']['name']}")
    print(f"  Score: {comp['score']}/{comp['max_score']} ({comp['percentage']:.0f}%)")
    print(f"  Dettagli:")
    for detail in comp['details']:
        print(f"    • {detail}")

print(f"\n🏆 Raccomandazione: {comparison['recommendation']['name']}")
print(f"   {comparison['reasoning']}")

# Test 8: Ragionamento per analogia
print("\n\n8️⃣  RAGIONAMENTO PER ANALOGIA")
print("-"*70)

analogy = reasoner.analogy_reasoning(
    "Binary search in sorted array",
    "Searching in phone book"
)

print(f"Source: {analogy['source']}")
print(f"Target: {analogy['target']}")
print(f"Mapping: {analogy['mapping']}")
print(f"Confidence: {analogy['confidence']:.1%}")

# Test 9: Spiegazione ragionamento
print("\n\n9️⃣  SPIEGAZIONE RAGIONAMENTO")
print("-"*70)

problem = "Download data from API and validate schema and save to database"
explanation = explain_reasoning(problem)
print(explanation)

# Test 10: Statistiche ragionamento
print("\n\n🔟 STATISTICHE RAGIONAMENTO")
print("-"*70)

stats = reasoner.get_reasoning_stats()
print(f"Ragionamenti totali: {stats['total_reasonings']}")
print(f"Step medi: {stats['average_steps']:.1f}")
print(f"Confidence media: {stats['average_confidence']:.1%}")
print(f"Tipi di ragionamento usati: {', '.join(stats['reasoning_types'])}")

# Test 11: Ragionamento multi-step complesso
print("\n\n1️⃣1️⃣  RAGIONAMENTO MULTI-STEP COMPLESSO")
print("-"*70)

complex_problem = """
Check if config file exists, if yes read it and parse JSON,
then validate the data structure, connect to database,
query existing records, merge with new data, and finally
update the database and log the operation
"""

chain = reasoner.reason(complex_problem.strip())
print(f"\nProblema complesso con {len(chain.steps)} step di ragionamento")
print(f"Confidence finale: {chain.overall_confidence:.1%}")
print(f"\nConclusione:")
print(chain.conclusion)

print("\n" + "="*70)
print("✅ TUTTI I TEST COMPLETATI!")
print("\n🧠 CAPACITÀ DI RAGIONAMENTO AVANZATO:")
print("  • Decomposizione problemi complessi")
print("  • Ragionamento logico deduttivo con regole")
print("  • Ragionamento abduttivo (best explanation)")
print("  • Ragionamento causale con grafi")
print("  • Catene causali multi-step")
print("  • Analisi what-if con predizioni")
print("  • Comparazione opzioni multi-criterio")
print("  • Ragionamento per analogia")
print("  • Spiegazioni dettagliate del processo")
print("  • Tracking confidenza propagata")
print("  • Gestione dipendenze sequenziali/parallele")
print("  • Identificazione pattern nei problemi")
print("="*70)
