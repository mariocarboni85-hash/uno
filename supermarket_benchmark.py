import time
from supermarket_manager import SalumeriaLatticiniAgent, OrtofruttaAgent, SalaOrdiniAgent, UfficioAgent

def benchmark_agents(num_agents=100, num_tasks=1000):
    print(f"\n[TEST DI CARICO] {num_agents} agenti, {num_tasks} task ciascuno")
    agent_types = [SalumeriaLatticiniAgent, OrtofruttaAgent, SalaOrdiniAgent, UfficioAgent]
    agents = []
    for i in range(num_agents):
        t = agent_types[i % 4]
        agents.append(t(f"Agente_{i+1}_{t.__name__}"))
    tasks = ['gestisci banco', 'prepara ordine', 'segnala scadenze',
             'gestisci ortofrutta', 'prepara esposizione', 'segnala rimozione',
             'gestisci ordini sala', 'coordina consegne', 'segnala ritardi',
             'gestisci ufficio', 'prepara report', 'gestisci personale', 'contatta fornitori']
    start = time.time()
    for agent in agents:
        for j in range(num_tasks):
            task = tasks[j % len(tasks)]
            agent.run_task(task)
    end = time.time()
    print(f"Tempo totale: {end-start:.2f} secondi")
    print(f"Task totali eseguiti: {num_agents * num_tasks}")
    print(f"Task/sec: {(num_agents * num_tasks)/(end-start):.2f}")

def main():
    benchmark_agents(num_agents=100, num_tasks=1000)

if __name__ == '__main__':
    main()
