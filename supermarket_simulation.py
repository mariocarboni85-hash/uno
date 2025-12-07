import random
import time
from supermarket_manager import SalumeriaLatticiniAgent, OrtofruttaAgent, SalaOrdiniAgent, UfficioAgent

class SimulatedEnvironment:
    def __init__(self, agent, tasks, scenarios):
        self.agent = agent
        self.tasks = tasks
        self.scenarios = scenarios
        self.results = []
    def run_simulation(self):
        print(f"\n[SIMULAZIONE] Ambiente: {self.agent.name}")
        for scenario in self.scenarios:
            print(f"Scenario: {scenario['descrizione']}")
            for task in self.tasks:
                # Simula variabilità e imprevisti
                if random.random() < scenario.get('errore_prob', 0.1):
                    print(f"- Task: {task} [ERRORE SIMULATO]")
                    result = f"{self.agent.name}: errore nel task '{task}'"
                else:
                    print(f"- Task: {task}")
                    result = self.agent.run_task(task)
                print(f"  Risultato: {result}")
                self.results.append((scenario['descrizione'], task, result))
                time.sleep(0.5)
        print(f"[FINE SIMULAZIONE] {self.agent.name}\n")
    def autonomy_score(self):
        # Semplice metrica: % task riusciti senza errori
        success = sum('errore' not in r[2] for r in self.results)
        return round(100 * success / len(self.results), 1) if self.results else 0

def main():
    # Task e scenari per ogni agente
    salumeria_tasks = ['gestisci banco', 'prepara ordine', 'segnala scadenze']
    ortofrutta_tasks = ['gestisci ortofrutta', 'prepara esposizione', 'segnala rimozione']
    sala_tasks = ['gestisci ordini sala', 'coordina consegne', 'segnala ritardi']
    ufficio_tasks = ['gestisci ufficio', 'prepara report', 'gestisci personale', 'contatta fornitori']

    salumeria_scenarios = [
        {'descrizione': 'Giornata normale', 'errore_prob': 0.05},
        {'descrizione': 'Picco clienti', 'errore_prob': 0.15},
        {'descrizione': 'Problema fornitura', 'errore_prob': 0.25}
    ]
    ortofrutta_scenarios = [
        {'descrizione': 'Freschezza ottimale', 'errore_prob': 0.05},
        {'descrizione': 'Arrivo merce', 'errore_prob': 0.10},
        {'descrizione': 'Prodotti deteriorati', 'errore_prob': 0.20}
    ]
    sala_scenarios = [
        {'descrizione': 'Ordini regolari', 'errore_prob': 0.05},
        {'descrizione': 'Ritardo consegne', 'errore_prob': 0.20},
        {'descrizione': 'Afflusso elevato', 'errore_prob': 0.15}
    ]
    ufficio_scenarios = [
        {'descrizione': 'Routine amministrativa', 'errore_prob': 0.05},
        {'descrizione': 'Audit esterno', 'errore_prob': 0.20},
        {'descrizione': 'Problema personale', 'errore_prob': 0.15}
    ]

    # Creazione agenti
    salumeria_agent = SalumeriaLatticiniAgent('SalumeriaLatticini')
    ortofrutta_agent = OrtofruttaAgent('Ortofrutta')
    sala_agent = SalaOrdiniAgent('SalaOrdini')
    ufficio_agent = UfficioAgent('Ufficio')

    # Ambienti simulati
    envs = [
        SimulatedEnvironment(salumeria_agent, salumeria_tasks, salumeria_scenarios),
        SimulatedEnvironment(ortofrutta_agent, ortofrutta_tasks, ortofrutta_scenarios),
        SimulatedEnvironment(sala_agent, sala_tasks, sala_scenarios),
        SimulatedEnvironment(ufficio_agent, ufficio_tasks, ufficio_scenarios)
    ]

    # Esecuzione simulazione e report
    for env in envs:
        env.run_simulation()
        score = env.autonomy_score()
        print(f"Autonomy Score {env.agent.name}: {score}%\n")
        if score >= 80:
            print(f"{env.agent.name} è pronto per lavorare in autonomia!\n")
        else:
            print(f"{env.agent.name} necessita di ulteriore training.\n")

if __name__ == '__main__':
    main()
