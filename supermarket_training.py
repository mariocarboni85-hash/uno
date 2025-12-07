import time
from supermarket_manager import SalumeriaLatticiniAgent, OrtofruttaAgent, SalaOrdiniAgent, UfficioAgent

class TrainingEnvironment:
    def __init__(self, agent, tasks):
        self.agent = agent
        self.tasks = tasks
        self.results = []
    def run_training(self):
        print(f"\n[TRAINING] Ambiente: {self.agent.name}")
        self.results = []
        for task in self.tasks:
            print(f"- Eseguo task: {task}")
            result = self.agent.run_task(task)
            print(f"  Risultato: {result}")
            self.results.append((task, result))
            time.sleep(0.5)
        print(f"[FINE TRAINING] {self.agent.name}\n")

    def autonomy_score(self):
        # Metrica: % task riusciti senza "errore" o "non gestito"
        success = sum('errore' not in r[1] and 'non gestito' not in r[1] for r in self.results)
        return round(100 * success / len(self.results), 1) if self.results else 0

    def train_until_ready(self, max_attempts=10):
        attempt = 0
        while attempt < max_attempts:
            self.run_training()
            score = self.autonomy_score()
            print(f"Autonomy Score {self.agent.name}: {score}%\n")
            if score >= 100:
                print(f"{self.agent.name} è pronto per lavorare in autonomia!\n")
                break
            else:
                print(f"{self.agent.name} necessita di ulteriore training. Ripeto...\n")
                attempt += 1
        if attempt == max_attempts and score < 100:
            print(f"{self.agent.name} non ha raggiunto il 100% dopo {max_attempts} tentativi.\n")

def main():
    # Definizione task per ogni agente
    salumeria_tasks = ['gestisci banco', 'prepara ordine', 'segnala scadenze']
    ortofrutta_tasks = ['gestisci ortofrutta', 'prepara esposizione', 'segnala rimozione']
    sala_tasks = ['gestisci ordini sala', 'coordina consegne', 'segnala ritardi']
    ufficio_tasks = ['gestisci ufficio', 'prepara report', 'gestisci personale', 'contatta fornitori']

    # Creazione agenti
    salumeria_agent = SalumeriaLatticiniAgent('SalumeriaLatticini')
    ortofrutta_agent = OrtofruttaAgent('Ortofrutta')
    sala_agent = SalaOrdiniAgent('SalaOrdini')
    ufficio_agent = UfficioAgent('Ufficio')

    # Ambienti di allenamento
    envs = [
        TrainingEnvironment(salumeria_agent, salumeria_tasks),
        TrainingEnvironment(ortofrutta_agent, ortofrutta_tasks),
        TrainingEnvironment(sala_agent, sala_tasks),
        TrainingEnvironment(ufficio_agent, ufficio_tasks)
    ]

    # Allenamento iterativo fino a 100%
    for env in envs:
        env.train_until_ready(max_attempts=10)

if __name__ == '__main__':
    main()
