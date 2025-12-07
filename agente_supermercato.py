# agente_supermercato.py

class AgenteSupermercato:
    def __init__(self, nome):
        self.nome = nome
        self.status = 'Pronto'
        self.last_task = None
        self.last_result = None
    def run_task(self, task):
        self.last_task = task
        self.status = 'Lavorando'
        result = None
        if task == 'gestisci banco':
            result = f'{self.nome}: banco gestito'
        elif task == 'gestisci ortofrutta':
            result = f'{self.nome}: ortofrutta gestito'
        elif task == 'gestisci ordini sala':
            result = f'{self.nome}: ordini sala gestiti'
        elif task == 'gestisci ufficio':
            result = f'{self.nome}: ufficio gestito'
        else:
            result = f'{self.nome}: task sconosciuto'
        self.last_result = result
        self.status = 'Pronto'
        return result

if __name__ == "__main__":
    agente = AgenteSupermercato('AgenteSupermercato')
    print(agente.run_task('gestisci banco'))
    print(agente.run_task('gestisci ortofrutta'))
    print(agente.run_task('gestisci ordini sala'))
    print(agente.run_task('gestisci ufficio'))
