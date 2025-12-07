import sys
from agent_backend import Agent

class SalumeriaLatticiniAgent(Agent):
    def run_task(self, task):
        if task == 'gestisci banco':
            return f'{self.name}: scorte e prezzi aggiornati'
        elif task == 'prepara ordine':
            return f'{self.name}: ordine salumi/latticini preparato'
        elif task == 'segnala scadenze':
            return f'{self.name}: prodotti in scadenza segnalati'
        return super().run_task(task)

class OrtofruttaAgent(Agent):
    def run_task(self, task):
        if task == 'gestisci ortofrutta':
            return f'{self.name}: freschezza e inventario aggiornati'
        elif task == 'prepara esposizione':
            return f'{self.name}: cassette ortofrutta pronte'
        elif task == 'segnala rimozione':
            return f'{self.name}: prodotti da rimuovere segnalati'
        return super().run_task(task)

class SalaOrdiniAgent(Agent):
    def run_task(self, task):
        if task == 'gestisci ordini sala':
            return f'{self.name}: ordini gestiti e aggiornati'
        elif task == 'coordina consegne':
            return f'{self.name}: consegne coordinate'
        elif task == 'segnala ritardi':
            return f'{self.name}: ritardi segnalati'
        return super().run_task(task)

class UfficioAgent(Agent):
    def run_task(self, task):
        if task == 'gestisci ufficio':
            return f'{self.name}: pratiche amministrative gestite'
        elif task == 'prepara report':
            return f'{self.name}: report vendite preparato'
        elif task == 'gestisci personale':
            return f'{self.name}: personale gestito'
        elif task == 'contatta fornitori':
            return f'{self.name}: fornitori contattati'
        return super().run_task(task)

AGENT_TYPES = {
    'salumeria': SalumeriaLatticiniAgent,
    'ortofrutta': OrtofruttaAgent,
    'sala': SalaOrdiniAgent,
    'ufficio': UfficioAgent
}

def main():
    print("Supermarket CLI Manager")
    print("="*40)
    agents = {
        'salumeria': SalumeriaLatticiniAgent('SalumeriaLatticini'),
        'ortofrutta': OrtofruttaAgent('Ortofrutta'),
        'sala': SalaOrdiniAgent('SalaOrdini'),
        'ufficio': UfficioAgent('Ufficio')
    }
    while True:
        print("\nAgenti disponibili:")
        for k in agents:
            print(f"- {k}")
        print("Comandi: esci | assegna <agente> <task>")
        cmd = input("> ").strip()
        if cmd == 'esci':
            print("Uscita...")
            break
        if cmd.startswith('assegna '):
            parts = cmd.split()
            if len(parts) < 3:
                print("Formato: assegna <agente> <task>")
                continue
            agente, task = parts[1], ' '.join(parts[2:])
            if agente in agents:
                result = agents[agente].run_task(task)
                print(f"Risultato: {result}")
            else:
                print("Agente non trovato.")
        else:
            print("Comando non riconosciuto.")

if __name__ == '__main__':
    main()
