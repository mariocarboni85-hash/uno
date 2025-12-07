import sys
import time
from pathlib import Path
from datetime import datetime

results = {'passed': [], 'failed': [], 'metrics': {}}
try:
    print("\n" + "="*80)
    print("TEST INTERFACCIA DIRETTA CON SUPERAGENT")
    print("="*80)
    from core.brain import interfaccia_superagent
    risposta = interfaccia_superagent("Dev_1", "Qual è il tuo stato?")
    if risposta:
        results["passed"].append("Interfaccia Diretta con SuperAgent")
    else:
        results["failed"].append("Interfaccia Diretta con SuperAgent: nessuna risposta")
except Exception as e:
    print(f"Errore interfaccia diretta: {e}")
    results["failed"].append(f"Interfaccia Diretta con SuperAgent: {e}")
try:
    print("\n=== DEMO: Evoluzione SuperAgent ===")
    from core.brain import demo_evoluzione_super_agent
    demo_evoluzione_super_agent()
    results["passed"].append("Demo Evoluzione SuperAgent")
except Exception as e:
    print(f"Errore demo evoluzione: {e}")
    results["failed"].append(f"Demo Evoluzione SuperAgent: {e}")
try:
    print("\n=== FASE DI APPRENDIMENTO REALE (NN) ===")
    from core.brain import SuperAgent
    agent = SuperAgent("NNTester")
    import numpy as np
    X = np.random.rand(200, 6)
    y = np.random.choice([0,1,2], size=200)
    loss = agent.train_on_tasks(X, y)
    print(f"Loss finale addestramento NN: {loss:.4f}")
    nuovo_task = np.random.rand(6)
    pred = agent.predict_task(nuovo_task)
    print(f"Predizione classe task (0=info,1=elettrica,2=fisica): {pred}")
    results["passed"].append("Training e Predizione NN Interna")
except Exception as e:
    print(f"Errore training NN: {e}")
    results["failed"].append(f"Training e Predizione NN Interna: {e}")
print("\n" + "="*80)
print(f"Test completato: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)
"""
Test Capacità Reali Super Agent
Test approfondito di tutte le funzionalità in scenari reali
"""

import sys
import time
from pathlib import Path
from datetime import datetime

"""
Test Capacità Reali Super Agent
Test approfondito di tutte le funzionalità in scenari reali
"""

import sys
import time
from pathlib import Path
from datetime import datetime

if sys.platform == 'win32':
    from core.brain import SuperAgent

def test_superagent_specialist_solutions():
    agent = SuperAgent("SuperExpert")
    problemi = [
        ("Trova il bug in un algoritmo", "informatica"),
        ("Calcola la resistenza equivalente di tre resistenze", "elettrica"),
        ("Simula il moto parabolico di un oggetto", "fisica"),
        ("Calcola l'integrale di x^2 da 0 a 2", "meccanica"),
    ]
    for testo, ambito in problemi:
        soluzione = agent.propose_solution(testo, ambito)
        print(f"[{ambito}] {soluzione}")

def test_superagent_autoallineamento():
    agent = SuperAgent("SelfAligner")
    print("-- SuperAgent esegue autoallineamento --")
    agent.autoallineamento()
    print("Log autoallineamento:")

if __name__ == "__main__":
    test_superagent_specialist_solutions()
    test_superagent_autoallineamento()

# ============================================================================
# TEST 3: LIBRARY UPDATE DETECTION
# ============================================================================
print("\n" + "="*80)
print("TEST 3: LIBRARY UPDATER - Rilevamento aggiornamenti disponibili")
print("="*80)

try:
    from tools.library_updater import LibraryUpdater
    updater = LibraryUpdater()
    start = time.time()
    venv_name = ".venv" if (updater.venvs_dir / ".venv").exists() else "super_agent_advanced"
    outdated = updater.list_outdated_packages(venv_name)
    print(f"Pacchetti obsoleti trovati: {len(outdated)}")
    results["passed"].append("Library Updater")
except Exception as e:
    print(f"Errore nel test library updater: {e}")
    results["failed"].append(f"Library Updater: {e}")


if __name__ == "__main__":
    # Dashboard evolutiva finale
    print("\n=== DASHBOARD EVOLUTIVA SUPERAGENT ===")
    agent = SuperAgent("SuperEvolver")
    problemi = [
        ("Trova il bug in un algoritmo di ordinamento", "informatica"),
        ("Calcola la resistenza equivalente di tre resistenze in parallelo", "elettrica"),
        ("Simula il moto parabolico di un oggetto lanciato", "fisica"),
        ("Calcola l'integrale di x^2 da 0 a 2", "meccanica"),
    ]
    cicli = 5
    for ciclo in range(1, cicli+1):
        print(f"\n=== CICLO DI MIGLIORAMENTO {ciclo} ===")
        for testo, ambito in problemi:
            print(f"\n--- PROBLEMA ({ambito}) ---")
            soluzione = agent.propose_solution(testo, ambito)
            print(f"Soluzione: {soluzione}")
            agent.learn_from_chat(testo, feedback=f"Risolto: {ambito} - ciclo {ciclo}")
        print(f"\nSkill attuali: {agent.skills}")
        print(f"Task completati: {agent.completed_tasks}")
        print("Log evolutivo:")
        for entry in agent.log[-5:]:
            print(entry)

    # Addestramento rete neurale interna sui task risolti
    print("\n=== FASE DI APPRENDIMENTO REALE (NN) ===")
    import numpy as np
    X = np.random.rand(200, 6)
    # output_size=3 -> classi 0,1,2
    y = np.random.choice([0,1,2], size=200)
    loss = agent.train_on_tasks(X, y)
    print(f"Loss finale addestramento NN: {loss:.4f}")
    nuovo_task = np.random.rand(6)
    pred = agent.predict_task(nuovo_task)
    print(f"Predizione classe task (0=info,1=elettrica,2=fisica): {pred}")

    # Valutazione finale
    total_tests = 5
    passed_tests = agent.completed_tasks
    success_rate = (passed_tests / total_tests) * 100
    if success_rate == 100:
        grade = "A+ (ECCELLENTE)"
        status = "🌟 SUPER AGENT: FULLY OPERATIONAL"
    elif success_rate >= 80:
        grade = "A (OTTIMO)"
        status = "✓ SUPER AGENT: OPERATIONAL"
    elif success_rate >= 60:
        grade = "B (BUONO)"
    status = "⚠ SUPER AGENT: MOSTLY OPERATIONAL"
else:
    grade = "C (SUFFICIENTE)"
    status = "⚠ SUPER AGENT: NEEDS ATTENTION"

print(f"Voto: {grade}")
print(f"\n{status}")

print("\n" + "="*80)

print(f"Test completato: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

# Inizializza il dizionario risultati
results = {'passed': [], 'failed': [], 'metrics': {}}

# Salva rapporto
report_file = Path("REAL_CAPABILITIES_REPORT.txt")
with open(report_file, "w", encoding="utf-8") as f:
    f.write("="*80 + "\n")
    f.write("SUPER AGENT - RAPPORTO CAPACITÀ REALI\n")
    f.write("="*80 + "\n\n")
    f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Python: {sys.version.split()[0]}\n\n")
    
    f.write("RISULTATI:\n")
    f.write(f"  Test Passati: {len(results['passed'])}/{total_tests}\n")
    f.write(f"  Success Rate: {success_rate:.1f}%\n")
    f.write(f"  Voto: {grade}\n\n")
    
    f.write("CAPACITÀ TESTATE:\n")
    for cap in results['passed']:
        f.write(f"  ✓ {cap}\n")
    


# Dati fittizi: classificazione (4 feature, 3 classi)
import torch
from core.brain import AdvancedSuperAgentNN
X = torch.randn(50, 4)
y = torch.randint(0, 3, (50,))

# Inizializza la rete
nn_agent = AdvancedSuperAgentNN(input_size=4, hidden_sizes=[64, 32], output_size=3, dropout=0.2)

# Training
loss = nn_agent.train_model(X, y, epochs=50, lr=0.01, classification=True, verbose=True)
print(f"Loss finale: {loss:.4f}")

# Predizione
pred = nn_agent.predict(X, classification=True)
print(f"Predizioni: {pred.tolist()}")

# Valutazione
metrics = nn_agent.evaluate(X, y, classification=True)
print(f"Accuratezza: {metrics['accuracy']:.2f}")
print("==== FINE ESEMPIO RETE NEURALE ====")

# ============================================================================
# TEST INTERFACCIA DIRETTA CON SUPERAGENT
# ============================================================================
print("\n" + "="*80)
print("TEST INTERFACCIA DIRETTA CON SUPERAGENT")
print("="*80)

for cap in results['passed']:
    print(f"  ✓ {cap}")

if results['failed']:
    print(f"\n{'CAPACITÀ CON PROBLEMI':^80}")
    for fail in results['failed']:
        print(f"  ✗ {fail}")

print(f"\n{'METRICHE PERFORMANCE':^80}")
print("-" * 80)
speed_metrics = {k: v for k, v in results['metrics'].items() if '_time' in k}
count_metrics = {k: v for k, v in results['metrics'].items() if '_time' not in k}

if speed_metrics:
    print("\nVelocità:")
    for key, value in speed_metrics.items():
        label = key.replace('_', ' ').title()
        print(f"  • {label}: {value}")

if count_metrics:
    print("\nStatistiche:")
    for key, value in count_metrics.items():
        label = key.replace('_', ' ').title()
        print(f"  • {label}: {value}")

# Calcola score complessivo
total_tests = 8
passed_tests = len(results['passed'])
success_rate = (passed_tests / total_tests) * 100

print(f"\n{'VALUTAZIONE COMPLESSIVA':^80}")
print("-" * 80)
print(f"Success Rate: {success_rate:.1f}%")
print(f"Capacità Operative: {passed_tests}/{total_tests}")

if success_rate == 100:
    grade = "A+ (ECCELLENTE)"
    status = "🌟 SUPER AGENT: FULLY OPERATIONAL"
elif success_rate >= 80:
    grade = "A (OTTIMO)"
    status = "✓ SUPER AGENT: OPERATIONAL"
elif success_rate >= 60:
    grade = "B (BUONO)"
    status = "⚠ SUPER AGENT: MOSTLY OPERATIONAL"
else:
    grade = "C (SUFFICIENTE)"
    status = "⚠ SUPER AGENT: NEEDS ATTENTION"

print(f"Voto: {grade}")
print(f"\n{status}")

print("\n" + "="*80)
print(f"Test completato: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

# Salva rapporto aggiornato dopo test chat
report_file = Path("REAL_CAPABILITIES_REPORT_CHAT_UPDATED.txt")
with open(report_file, "w", encoding="utf-8") as f:
    f.write("="*80 + "\n")
    f.write("SUPER AGENT - RAPPORTO CAPACITÀ REALI AGGIORNATO DOPO TEST CHAT\n")
    f.write("="*80 + "\n\n")
    f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Python: {sys.version.split()[0]}\n\n")
    
    f.write("RISULTATI:\n")
    f.write(f"  Test Passati: {len(results['passed'])}/{total_tests}\n")
    f.write(f"  Success Rate: {success_rate:.1f}%\n")
    f.write(f"  Voto: {grade}\n\n")
    
    f.write("CAPACITÀ TESTATE:\n")
    for cap in results['passed']:
        f.write(f"  ✓ {cap}\n")
    
    for fail in results['failed']:
        f.write(f"  ✗ {fail}\n")
    
    f.write("\nMETRICHE:\n")
    for key, value in results['metrics'].items():
        f.write(f"  {key}: {value}\n")
    
    f.write(f"\nSTATUS: {status}\n")

print(f"\n📄 Rapporto salvato in: {report_file}")

# ============================================================================
# TEST CHAT AVANZATA CON SUPERAGENT
# ============================================================================
print("\n" + "="*80)
print("TEST CHAT AVANZATA CON SUPERAGENT")
print("="*80)

try:
    from core.brain import chat_superagent_avanzata
    print("\n[Test Vocale] Invio input vocale")
    response = chat_superagent_avanzata(agent_name="Dev_1", voce="Ciao, ho trovato un bug nel sistema.")
    print(f"  ✓ Risposta a input vocale: {response}")
    print("\n[Test Visivo] Invio input visivo")
    response = chat_superagent_avanzata(agent_name="Dev_1", immagine="Diagramma di flusso con errore nel nodo 3.")
    print(f"  ✓ Risposta a input visivo: {response}")
    print("\n[Test Testo] Invio input testuale")
    response = chat_superagent_avanzata(agent_name="Dev_1", testo="Devi aiutarmi con la documentazione.")
    print(f"  ✓ Risposta a input testuale: {response}")
    print("\n[Test Combinato] Invio input combinato")
    response = chat_superagent_avanzata(agent_name="Dev_1", testo="Ciao!", voce="Puoi risolvere questo errore?", immagine="Screenshot di un crash.")
    print(f"  ✓ Risposta a input combinato: {response}")
    results["passed"].append("Chat Avanzata con SuperAgent")
    
except Exception as e:
    print(f"  ✗ FAIL: {e}")
    results["failed"].append(f"Chat Avanzata con SuperAgent: {e}")

# ============================================================================
# RAPPORTO FINALE AGGIORNATO DOPO TEST CHAT AVANZATA
# ============================================================================
print("\n" + "="*80)
print("RAPPORTO FINALE AGGIORNATO DOPO TEST CHAT AVANZATA - CAPACITÀ REALI SUPER AGENT")
print("="*80)

print(f"\n{'RISULTATI TEST':^80}")
print("-" * 80)
print(f"✓ Test Passati: {len(results['passed'])}/9")
print(f"✗ Test Falliti: {len(results['failed'])}/9")

if results['passed']:
    print(f"\n{'CAPACITÀ FUNZIONANTI':^80}")
    for cap in results['passed']:
        print(f"  ✓ {cap}")

if results['failed']:
    print(f"\n{'CAPACITÀ CON PROBLEMI':^80}")
    for fail in results['failed']:
        print(f"  ✗ {fail}")

print(f"\n{'METRICHE PERFORMANCE':^80}")
print("-" * 80)

# Raggruppa metriche
speed_metrics = {k: v for k, v in results['metrics'].items() if '_time' in k}
count_metrics = {k: v for k, v in results['metrics'].items() if '_time' not in k}

if speed_metrics:
    print("\nVelocità:")
    for key, value in speed_metrics.items():
        label = key.replace('_', ' ').title()
        print(f"  • {label}: {value}")

if count_metrics:
    print("\nStatistiche:")
    for key, value in count_metrics.items():
        label = key.replace('_', ' ').title()
        print(f"  • {label}: {value}")

# Calcola score complessivo
total_tests = 9
passed_tests = len(results['passed'])
success_rate = (passed_tests / total_tests) * 100

print(f"\n{'VALUTAZIONE COMPLESSIVA':^80}")
print("-" * 80)
print(f"Success Rate: {success_rate:.1f}%")
print(f"Capacità Operative: {passed_tests}/{total_tests}")

if success_rate == 100:
    grade = "A+ (ECCELLENTE)"
    status = "🌟 SUPER AGENT: FULLY OPERATIONAL"
elif success_rate >= 80:
    grade = "A (OTTIMO)"
    status = "✓ SUPER AGENT: OPERATIONAL"
elif success_rate >= 60:
    grade = "B (BUONO)"
    status = "⚠ SUPER AGENT: MOSTLY OPERATIONAL"
else:
    grade = "C (SUFFICIENTE)"
    status = "⚠ SUPER AGENT: NEEDS ATTENTION"

print(f"Voto: {grade}")
print(f"\n{status}")

print("\n" + "="*80)
print(f"Test completato: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

# Salva rapporto aggiornato dopo test chat avanzata
report_file = Path("REAL_CAPABILITIES_REPORT_CHAT_AVANZATA_UPDATED.txt")
with open(report_file, "w", encoding="utf-8") as f:
    f.write("="*80 + "\n")
    f.write("SUPER AGENT - RAPPORTO CAPACITÀ REALI AGGIORNATO DOPO TEST CHAT AVANZATA\n")
    f.write("="*80 + "\n\n")
    f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Python: {sys.version.split()[0]}\n\n")
    
    f.write("RISULTATI:\n")
    f.write(f"  Test Passati: {len(results['passed'])}/{total_tests}\n")
    f.write(f"  Success Rate: {success_rate:.1f}%\n")
    f.write(f"  Voto: {grade}\n\n")
    
    f.write("CAPACITÀ TESTATE:\n")
    for cap in results['passed']:
        f.write(f"  ✓ {cap}\n")
    
    for fail in results['failed']:
        f.write(f"  ✗ {fail}\n")
    
    f.write("\nMETRICHE:\n")
    for key, value in results['metrics'].items():
        f.write(f"  {key}: {value}\n")
    
    f.write(f"\nSTATUS: {status}\n")

print(f"\n📄 Rapporto salvato in: {report_file}")

# ============================================================================
# TEST SOLUZIONI SPECIALISTICHE CON SUPERAGENT
# ============================================================================
print("\n" + "="*80)
print("TEST SOLUZIONI SPECIALISTICHE CON SUPERAGENT")
print("="*80)

try:
    from core.brain import SuperAgent
    agent = SuperAgent("SuperExpert")
    problemi = [
        ("Trova il bug in un algoritmo", "informatica"),
        ("Calcola la resistenza equivalente di tre resistenze", "elettrica"),
        ("Simula il moto parabolico di un oggetto", "fisica"),
        ("Calcola l'integrale di x^2 da 0 a 2", "meccanica"),
    ]
    for testo, ambito in problemi:
        soluzione = agent.propose_solution(testo, ambito)
        print(f"[{ambito}] {soluzione}")
    results["passed"].append("Soluzioni Specialistiche con SuperAgent")
    
except Exception as e:
    print(f"  ✗ FAIL: {e}")
    results["failed"].append(f"Soluzioni Specialistiche con SuperAgent: {e}")

# ============================================================================
# RAPPORTO FINALE AGGIORNATO DOPO TEST SOLUZIONI SPECIALISTICHE
# ============================================================================
print("\n" + "="*80)
print("RAPPORTO FINALE AGGIORNATO DOPO TEST SOLUZIONI SPECIALISTICHE - CAPACITÀ REALI SUPER AGENT")
print("="*80)

print(f"\n{'RISULTATI TEST':^80}")
print("-" * 80)
print(f"✓ Test Passati: {len(results['passed'])}/10")
print(f"✗ Test Falliti: {len(results['failed'])}/10")

if results['passed']:
    print(f"\n{'CAPACITÀ FUNZIONANTI':^80}")
    for cap in results['passed']:
        print(f"  ✓ {cap}")

if results['failed']:
    print(f"\n{'CAPACITÀ CON PROBLEMI':^80}")
    for fail in results['failed']:
        print(f"  ✗ {fail}")

print(f"\n{'METRICHE PERFORMANCE':^80}")
print("-" * 80)

# Raggruppa metriche
speed_metrics = {k: v for k, v in results['metrics'].items() if '_time' in k}
count_metrics = {k: v for k, v in results['metrics'].items() if '_time' not in k}

if speed_metrics:
    print("\nVelocità:")
    for key, value in speed_metrics.items():
        label = key.replace('_', ' ').title()
        print(f"  • {label}: {value}")

if count_metrics:
    print("\nStatistiche:")
    for key, value in count_metrics.items():
        label = key.replace('_', ' ').title()
        print(f"  • {label}: {value}")

# Calcola score complessivo
total_tests = 10
passed_tests = len(results['passed'])
success_rate = (passed_tests / total_tests) * 100

print(f"\n{'VALUTAZIONE COMPLESSIVA':^80}")
print("-" * 80)
print(f"Success Rate: {success_rate:.1f}%")
print(f"Capacità Operative: {passed_tests}/{total_tests}")

if success_rate == 100:
    grade = "A+ (ECCELLENTE)"
    status = "🌟 SUPER AGENT: FULLY OPERATIONAL"
elif success_rate >= 80:
    grade = "A (OTTIMO)"
    status = "✓ SUPER AGENT: OPERATIONAL"
elif success_rate >= 60:
    grade = "B (BUONO)"
    status = "⚠ SUPER AGENT: MOSTLY OPERATIONAL"
else:
    grade = "C (SUFFICIENTE)"
    status = "⚠ SUPER AGENT: NEEDS ATTENTION"

print(f"Voto: {grade}")
print(f"\n{status}")

print("\n" + "="*80)
print(f"Test completato: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

# Salva rapporto aggiornato dopo test soluzioni specialistiche
report_file = Path("REAL_CAPABILITIES_REPORT_SPECIALIST_UPDATED.txt")
with open(report_file, "w", encoding="utf-8") as f:
    f.write("="*80 + "\n")
    f.write("SUPER AGENT - RAPPORTO CAPACITÀ REALI AGGIORNATO DOPO TEST SOLUZIONI SPECIALISTICHE\n")
    f.write("="*80 + "\n\n")
    f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Python: {sys.version.split()[0]}\n\n")
    
    f.write("RISULTATI:\n")
    f.write(f"  Test Passati: {len(results['passed'])}/{total_tests}\n")
    f.write(f"  Success Rate: {success_rate:.1f}%\n")
    f.write(f"  Voto: {grade}\n\n")
    
    f.write("CAPACITÀ TESTATE:\n")
    for cap in results['passed']:
        f.write(f"  ✓ {cap}\n")
    
    for fail in results['failed']:
        f.write(f"  ✗ {fail}\n")
    
    f.write("\nMETRICHE:\n")
    for key, value in results['metrics'].items():
        f.write(f"  {key}: {value}\n")
    
    f.write(f"\nSTATUS: {status}\n")

print(f"\n📄 Rapporto salvato in: {report_file}")

# ============================================================================
# TEST APPRENDIMENTO SUPERAGENT TRAMITE CHAT
# ============================================================================
print("\n" + "="*80)
print("TEST APPRENDIMENTO SUPERAGENT TRAMITE CHAT")
print("="*80)

try:
    from core.brain import SuperAgent
    agent = SuperAgent(name="ChatLearner")
    print("-- Chat diretta con SuperAgent --")
    messaggi = [
        ("Come posso ottimizzare questo algoritmo?", "algoritmi avanzati"),
        ("Qual è la soluzione migliore per il backup?", "backup sicuro"),
        ("Come si migliora la sicurezza di un server?", "cybersecurity"),
    ]
    for msg, feedback in messaggi:
        agent.learn_from_chat(msg, feedback)
        print(f"Chat: {msg} | Feedback: {feedback}")
        print(f"Log: {agent.log[-2:]}")
    print("-- Knowledge finale --")
    print(agent.get_knowledge())
    print("-- Skills finali --")
    print(agent.skills)
    results["passed"].append("Apprendimento SuperAgent tramite Chat")
    
except Exception as e:
    print(f"  ✗ FAIL: {e}")
    results["failed"].append(f"Apprendimento SuperAgent tramite Chat: {e}")

# ============================================================================
# RAPPORTO FINALE AGGIORNATO DOPO TEST APPRENDIMENTO SUPERAGENT TRAMITE CHAT
# ============================================================================
print("\n" + "="*80)
print("RAPPORTO FINALE AGGIORNATO DOPO TEST APPRENDIMENTO SUPERAGENT TRAMITE CHAT - CAPACITÀ REALI SUPER AGENT")
print("="*80)

print(f"\n{'RISULTATI TEST':^80}")
print("-" * 80)
print(f"✓ Test Passati: {len(results['passed'])}/10")
print(f"✗ Test Falliti: {len(results['failed'])}/10")

if results['passed']:
    print(f"\n{'CAPACITÀ FUNZIONANTI':^80}")
    for cap in results['passed']:
        print(f"  ✓ {cap}")

if results['failed']:
    print(f"\n{'CAPACITÀ CON PROBLEMI':^80}")
    for fail in results['failed']:
        print(f"  ✗ {fail}")

print(f"\n{'METRICHE PERFORMANCE':^80}")
print("-" * 80)

# Raggruppa metriche
speed_metrics = {k: v for k, v in results['metrics'].items() if '_time' in k}
count_metrics = {k: v for k, v in results['metrics'].items() if '_time' not in k}

if speed_metrics:
    print("\nVelocità:")
    for key, value in speed_metrics.items():
        label = key.replace('_', ' ').title()
        print(f"  • {label}: {value}")

if count_metrics:
    print("\nStatistiche:")
    for key, value in count_metrics.items():
        label = key.replace('_', ' ').title()
        print(f"  • {label}: {value}")

# Calcola score complessivo
total_tests = 10
passed_tests = len(results['passed'])
success_rate = (passed_tests / total_tests) * 100

print(f"\n{'VALUTAZIONE COMPLESSIVA':^80}")
print("-" * 80)
print(f"Success Rate: {success_rate:.1f}%")
print(f"Capacità Operative: {passed_tests}/{total_tests}")

if success_rate == 100:
    grade = "A+ (ECCELLENTE)"
    status = "🌟 SUPER AGENT: FULLY OPERATIONAL"
elif success_rate >= 80:
    grade = "A (OTTIMO)"
    status = "✓ SUPER AGENT: OPERATIONAL"
elif success_rate >= 60:
    grade = "B (BUONO)"
    status = "⚠ SUPER AGENT: MOSTLY OPERATIONAL"
else:
    grade = "C (SUFFICIENTE)"
    status = "⚠ SUPER AGENT: NEEDS ATTENTION"

print(f"Voto: {grade}")
print(f"\n{status}")

print("\n" + "="*80)
print(f"Test completato: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

# Salva rapporto aggiornato dopo test apprendimento tramite chat
report_file = Path("REAL_CAPABILITIES_REPORT_APPRENDIMENTO_CHAT_UPDATED.txt")
with open(report_file, "w", encoding="utf-8") as f:
    f.write("="*80 + "\n")
    f.write("SUPER AGENT - RAPPORTO CAPACITÀ REALI AGGIORNATO DOPO TEST APPRENDIMENTO TRAMITE CHAT\n")
    f.write("="*80 + "\n\n")
    f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Python: {sys.version.split()[0]}\n\n")
    
    f.write("RISULTATI:\n")
    f.write(f"  Test Passati: {len(results['passed'])}/{total_tests}\n")
    f.write(f"  Success Rate: {success_rate:.1f}%\n")
    f.write(f"  Voto: {grade}\n\n")
    
    f.write("CAPACITÀ TESTATE:\n")
    for cap in results['passed']:
        f.write(f"  ✓ {cap}\n")
    
    for fail in results['failed']:
        f.write(f"  ✗ {fail}\n")
    
    f.write("\nMETRICHE:\n")
    for key, value in results['metrics'].items():
        f.write(f"  {key}: {value}\n")
    
    f.write(f"\nSTATUS: {status}\n")

print(f"\n📄 Rapporto salvato in: {report_file}")

# ============================================================================
# TEST SUPERAGENT RIFERITO ALL'APP
# ============================================================================
print("\n" + "="*80)
print("TEST SUPERAGENT RIFERITO ALL'APP")
print("="*80)

try:
    from core.brain import SuperAgent
    agent = SuperAgent(name="AppFixer")
    problemi_app = [
        "Errore di importazione libreria torch",
        "Modulo jedi non trovato nell'ambiente attivo",
        "Divisione per zero nello stress test",
        "Ambiente Python non allineato con le dipendenze",
        "Configurazione venv non corretta",
    ]
    print("-- SuperAgent risolve problemi dell'app --")
    for problema in problemi_app:
        soluzione = agent.propose_solution(problema, ambito="informatica")
        print(f"Problema: {problema}")
        print(f"Soluzione proposta: {soluzione}")
    print("-- Log finale --")
    print(agent.log[-5:])
    results["passed"].append("SuperAgent Risoluzione App")
    
except Exception as e:
    print(f"  ✗ FAIL: {e}")
    results["failed"].append(f"SuperAgent Risoluzione App: {e}")

# ============================================================================
# RAPPORTO FINALE AGGIORNATO DOPO TEST SUPERAGENT RIFERITO ALL'APP
# ============================================================================
print("\n" + "="*80)
print("RAPPORTO FINALE AGGIORNATO DOPO TEST SUPERAGENT RIFERITO ALL'APP - CAPACITÀ REALI SUPER AGENT")
print("="*80)

print(f"\n{'RISULTATI TEST':^80}")
print("-" * 80)
print(f"✓ Test Passati: {len(results['passed'])}/10")
print(f"✗ Test Falliti: {len(results['failed'])}/10")

if results['passed']:
    print(f"\n{'CAPACITÀ FUNZIONANTI':^80}")
    for cap in results['passed']:
        print(f"  ✓ {cap}")

if results['failed']:
    print(f"\n{'CAPACITÀ CON PROBLEMI':^80}")
    for fail in results['failed']:
        print(f"  ✗ {fail}")

print(f"\n{'METRICHE PERFORMANCE':^80}")
print("-" * 80)

# Raggruppa metriche
speed_metrics = {k: v for k, v in results['metrics'].items() if '_time' in k}
count_metrics = {k: v for k, v in results['metrics'].items() if '_time' not in k}

if speed_metrics:
    print("\nVelocità:")
    for key, value in speed_metrics.items():
        label = key.replace('_', ' ').title()
        print(f"  • {label}: {value}")

if count_metrics:
    print("\nStatistiche:")
    for key, value in count_metrics.items():
        label = key.replace('_', ' ').title()
        print(f"  • {label}: {value}")

# Calcola score complessivo
total_tests = 10
passed_tests = len(results['passed'])
success_rate = (passed_tests / total_tests) * 100

print(f"\n{'VALUTAZIONE COMPLESSIVA':^80}")
print("-" * 80)
print(f"Success Rate: {success_rate:.1f}%")
print(f"Capacità Operative: {passed_tests}/{total_tests}")

if success_rate == 100:
    grade = "A+ (ECCELLENTE)"
    status = "🌟 SUPER AGENT: FULLY OPERATIONAL"
elif success_rate >= 80:
    grade = "A (OTTIMO)"
    status = "✓ SUPER AGENT: OPERATIONAL"
elif success_rate >= 60:
    grade = "B (BUONO)"
    status = "⚠ SUPER AGENT: MOSTLY OPERATIONAL"
else:
    grade = "C (SUFFICIENTE)"
    status = "⚠ SUPER AGENT: NEEDS ATTENTION"

print(f"Voto: {grade}")
print(f"\n{status}")

print("\n" + "="*80)
print(f"Test completato: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

# Salva rapporto aggiornato dopo test superagent riferito all'app
report_file = Path("REAL_CAPABILITIES_REPORT_SUPERAGENT_APP_UPDATED.txt")
with open(report_file, "w", encoding="utf-8") as f:
    f.write("="*80 + "\n")
    f.write("SUPER AGENT - RAPPORTO CAPACITÀ REALI AGGIORNATO DOPO TEST SUPERAGENT RIFERITO ALL'APP\n")
    f.write("="*80 + "\n\n")
    f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Python: {sys.version.split()[0]}\n\n")
    
    f.write("RISULTATI:\n")
    f.write(f"  Test Passati: {len(results['passed'])}/{total_tests}\n")
    f.write(f"  Success Rate: {success_rate:.1f}%\n")
    f.write(f"  Voto: {grade}\n\n")
    
    f.write("CAPACITÀ TESTATE:\n")
    for cap in results['passed']:
        f.write(f"  ✓ {cap}\n")
    
    for fail in results['failed']:
        f.write(f"  ✗ {fail}\n")
    
    f.write("\nMETRICHE:\n")
    for key, value in results['metrics'].items():
        f.write(f"  {key}: {value}\n")
    
    f.write(f"\nSTATUS: {status}\n")

print(f"\n📄 Rapporto salvato in: {report_file}")

# ============================================================================
# TEST CREAZIONE CHAT APP CON SUPERAGENT
# ============================================================================
print("\n" + "="*80)
print("TEST CREAZIONE CHAT APP CON SUPERAGENT")
print("="*80)

speed_metrics = {k: v for k, v in results['metrics'].items() if '_time' in k}
count_metrics = {k: v for k, v in results['metrics'].items() if '_time' not in k}

if speed_metrics:
    print("\nVelocità:")
    for key, value in speed_metrics.items():
        label = key.replace('_', ' ').title()
        print(f"  • {label}: {value}")

if count_metrics:
    print("\nStatistiche:")
    for key, value in count_metrics.items():
        label = key.replace('_', ' ').title()
        print(f"  • {label}: {value}")

# Calcola score complessivo
total_tests = 10
passed_tests = len(results['passed'])
success_rate = (passed_tests / total_tests) * 100

print(f"\n{'VALUTAZIONE COMPLESSIVA':^80}")
print("-" * 80)
print(f"Success Rate: {success_rate:.1f}%")
print(f"Capacità Operative: {passed_tests}/{total_tests}")

if success_rate == 100:
    grade = "A+ (ECCELLENTE)"
    status = "🌟 SUPER AGENT: FULLY OPERATIONAL"
elif success_rate >= 80:
    grade = "A (OTTIMO)"
    status = "✓ SUPER AGENT: OPERATIONAL"
elif success_rate >= 60:
    grade = "B (BUONO)"
    status = "⚠ SUPER AGENT: MOSTLY OPERATIONAL"
else:
    grade = "C (SUFFICIENTE)"
    status = "⚠ SUPER AGENT: NEEDS ATTENTION"

print(f"Voto: {grade}")
print(f"\n{status}")

print("\n" + "="*80)
print(f"Test completato: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

# Salva rapporto aggiornato dopo test creazione chat app
report_file = Path("REAL_CAPABILITIES_REPORT_CREAZIONE_CHAT_APP_UPDATED.txt")
with open(report_file, "w", encoding="utf-8") as f:
    f.write("="*80 + "\n")
    f.write("SUPER AGENT - RAPPORTO CAPACITÀ REALI AGGIORNATO DOPO TEST CREAZIONE CHAT APP\n")
    f.write("="*80 + "\n\n")
    f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Python: {sys.version.split()[0]}\n\n")
    
    f.write("RISULTATI:\n")
    f.write(f"  Test Passati: {len(results['passed'])}/{total_tests}\n")
    f.write(f"  Success Rate: {success_rate:.1f}%\n")
    f.write(f"  Voto: {grade}\n\n")
    
    f.write("CAPACITÀ TESTATE:\n")
    for cap in results['passed']:
        f.write(f"  ✓ {cap}\n")
    
    for fail in results['failed']:
        f.write(f"  ✗ {fail}\n")
    
    f.write("\nMETRICHE:\n")
    for key, value in results['metrics'].items():
        f.write(f"  {key}: {value}\n")
    
    f.write(f"\nSTATUS: {status}\n")

print(f"\n📄 Rapporto salvato in: {report_file}")

# ============================================================================
# TEST AUTOALLINEAMENTO SUPERAGENT
# ============================================================================
print("\n" + "="*80)
print("TEST AUTOALLINEAMENTO SUPERAGENT")
print("="*80)

try:
    from core.brain import SuperAgent
    agent = SuperAgent("SelfAligner")
    print("-- SuperAgent esegue autoallineamento --")
    agent.autoallineamento()
    print("Log autoallineamento:")
    for entry in agent.log[-10:]:
        print(entry)
    results["passed"].append("Autoallineamento SuperAgent")
    
except Exception as e:
    print(f"  ✗ FAIL: {e}")
    results["failed"].append(f"Autoallineamento SuperAgent: {e}")

# ============================================================================
# RAPPORTO FINALE AGGIORNATO DOPO TEST AUTOALLINEAMENTO
# ============================================================================
print("\n" + "="*80)
print("RAPPORTO FINALE AGGIORNATO DOPO TEST AUTOALLINEAMENTO - CAPACITÀ REALI SUPER AGENT")
print("="*80)

print(f"\n{'RISULTATI TEST':^80}")
print("-" * 80)
print(f"✓ Test Passati: {len(results['passed'])}/10")
print(f"✗ Test Falliti: {len(results['failed'])}/10")

if results['passed']:
    print(f"\n{'CAPACITÀ FUNZIONANTI':^80}")
    for cap in results['passed']:
        print(f"  ✓ {cap}")

if results['failed']:
    print(f"\n{'CAPACITÀ CON PROBLEMI':^80}")
    for fail in results['failed']:
        print(f"  ✗ {fail}")

print(f"\n{'METRICHE PERFORMANCE':^80}")
print("-" * 80)

# Raggruppa metriche
speed_metrics = {k: v for k, v in results['metrics'].items() if '_time' in k}
count_metrics = {k: v for k, v in results['metrics'].items() if '_time' not in k}

if speed_metrics:
    print("\nVelocità:")
    for key, value in speed_metrics.items():
        label = key.replace('_', ' ').title()
        print(f"  • {label}: {value}")

if count_metrics:
    print("\nStatistiche:")
    for key, value in count_metrics.items():
        label = key.replace('_', ' ').title()
        print(f"  • {label}: {value}")

# Calcola score complessivo
total_tests = 10
passed_tests = len(results['passed'])
success_rate = (passed_tests / total_tests) * 100

print(f"\n{'VALUTAZIONE COMPLESSIVA':^80}")
print("-" * 80)
print(f"Success Rate: {success_rate:.1f}%")
print(f"Capacità Operative: {passed_tests}/{total_tests}")

if success_rate == 100:
    grade = "A+ (ECCELLENTE)"
    status = "🌟 SUPER AGENT: FULLY OPERATIONAL"
elif success_rate >= 80:
    grade = "A (OTTIMO)"
    status = "✓ SUPER AGENT: OPERATIONAL"
elif success_rate >= 60:
    grade = "B (BUONO)"
    status = "⚠ SUPER AGENT: MOSTLY OPERATIONAL"
else:
    grade = "C (SUFFICIENTE)"
    status = "⚠ SUPER AGENT: NEEDS ATTENTION"

print(f"Voto: {grade}")
print(f"\n{status}")

print("\n" + "="*80)
print(f"Test completato: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

# Salva rapporto aggiornato dopo test autoallineamento
report_file = Path("REAL_CAPABILITIES_REPORT_AUTOALLINEAMENTO_UPDATED.txt")
with open(report_file, "w", encoding="utf-8") as f:
    f.write("="*80 + "\n")
    f.write("SUPER AGENT - RAPPORTO CAPACITÀ REALI AGGIORNATO DOPO TEST AUTOALLINEAMENTO\n")
    f.write("="*80 + "\n\n")
    f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Python: {sys.version.split()[0]}\n\n")
    
    f.write("RISULTATI:\n")
    f.write(f"  Test Passati: {len(results['passed'])}/{total_tests}\n")
    f.write(f"  Success Rate: {success_rate:.1f}%\n")
    f.write(f"  Voto: {grade}\n\n")
    
    f.write("CAPACITÀ TESTATE:\n")
    for cap in results['passed']:
        f.write(f"  ✓ {cap}\n")
    
    for fail in results['failed']:
        f.write(f"  ✗ {fail}\n")
    
    f.write("\nMETRICHE:\n")
    for key, value in results['metrics'].items():
        f.write(f"  {key}: {value}\n")
    
    f.write(f"\nSTATUS: {status}\n")

print(f"\n📄 Rapporto salvato in: {report_file}")

# ============================================================================
# TEST AUTOALLINEAMENTO SUPERAGENT CON CHAT
# ============================================================================
print("\n" + "="*80)
print("TEST AUTOALLINEAMENTO SUPERAGENT CON CHAT")
print("="*80)

try:
    from core.brain import SuperAgent
    agent = SuperAgent(name="ChatSelfAligner")
    print("-- SuperAgent esegue autoallineamento con chat --")
    agent.autoallineamento()
    print("Log autoallineamento:")
    for entry in agent.log[-10:]:
        print(entry)
    results["passed"].append("Autoallineamento SuperAgent con Chat")
    
except Exception as e:
    print(f"  ✗ FAIL: {e}")
    results["failed"].append(f"Autoallineamento SuperAgent con Chat: {e}")

# ============================================================================
# RAPPORTO FINALE AGGIORNATO DOPO TEST AUTOALLINEAMENTO SUPERAGENT CON CHAT
# ============================================================================
print("\n" + "="*80)
print("RAPPORTO FINALE AGGIORNATO DOPO TEST AUTOALLINEAMENTO SUPERAGENT CON CHAT - CAPACITÀ REALI SUPER AGENT")
print("="*80)

print(f"\n{'RISULTATI TEST':^80}")
print("-" * 80)
print(f"✓ Test Passati: {len(results['passed'])}/10")
print(f"✗ Test Falliti: {len(results['failed'])}/10")

if results['passed']:
    print(f"\n{'CAPACITÀ FUNZIONANTI':^80}")
    for cap in results['passed']:
        print(f"  ✓ {cap}")

if results['failed']:
    print(f"\n{'CAPACITÀ CON PROBLEMI':^80}")
    for fail in results['failed']:
        print(f"  ✗ {fail}")

print(f"\n{'METRICHE PERFORMANCE':^80}")
print("-" * 80)

# Raggruppa metriche
speed_metrics = {k: v for k, v in results['metrics'].items() if '_time' in k}
count_metrics = {k: v for k, v in results['metrics'].items() if '_time' not in k}

if speed_metrics:
    print("\nVelocità:")
    for key, value in speed_metrics.items():
        label = key.replace('_', ' ').title()
        print(f"  • {label}: {value}")

if count_metrics:
    print("\nStatistiche:")
    for key, value in count_metrics.items():
        label = key.replace('_', ' ').title()
        print(f"  • {label}: {value}")

# Calcola score complessivo
total_tests = 10
passed_tests = len(results['passed'])
success_rate = (passed_tests / total_tests) * 100

print(f"\n{'VALUTAZIONE COMPLESSIVA':^80}")
print("-" * 80)
print(f"Success Rate: {success_rate:.1f}%")
print(f"Capacità Operative: {passed_tests}/{total_tests}")

if success_rate == 100:
    grade = "A+ (ECCELLENTE)"
    status = "🌟 SUPER AGENT: FULLY OPERATIONAL"
elif success_rate >= 80:
    grade = "A (OTTIMO)"
    status = "✓ SUPER AGENT: OPERATIONAL"
elif success_rate >= 60:
    grade = "B (BUONO)"
    status = "⚠ SUPER AGENT: MOSTLY OPERATIONAL"
else:
    grade = "C (SUFFICIENTE)"
    status = "⚠ SUPER AGENT: NEEDS ATTENTION"

print(f"Voto: {grade}")
print(f"\n{status}")

print("\n" + "="*80)
print(f"Test completato: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

# Salva rapporto aggiornato dopo test autoallineamento con chat
report_file = Path("REAL_CAPABILITIES_REPORT_AUTOALLINEAMENTO_CHAT_UPDATED.txt")
with open(report_file, "w", encoding="utf-8") as f:
    f.write("="*80 + "\n")
    f.write("SUPER AGENT - RAPPORTO CAPACITÀ REALI AGGIORNATO DOPO TEST AUTOALLINEAMENTO CON CHAT\n")
    f.write("="*80 + "\n\n")
    f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Python: {sys.version.split()[0]}\n\n")
    
    f.write("RISULTATI:\n")
    f.write(f"  Test Passati: {len(results['passed'])}/{total_tests}\n")
    f.write(f"  Success Rate: {success_rate:.1f}%\n")
    f.write(f"  Voto: {grade}\n\n")
    
    f.write("CAPACITÀ TESTATE:\n")
    for cap in results['passed']:
        f.write(f"  ✓ {cap}\n")
    
    for fail in results['failed']:
        f.write(f"  ✗ {fail}\n")
    
    f.write("\nMETRICHE:\n")
    for key, value in results['metrics'].items():
        f.write(f"  {key}: {value}\n")
    
    f.write(f"\nSTATUS: {status}\n")

print(f"\n📄 Rapporto salvato in: {report_file}")