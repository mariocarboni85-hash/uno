from agent import SuperAgent


class CustomAgent(SuperAgent):
    """Agente specializzato nell'analisi dei requisiti software.

    Espone una semplice interfaccia `reply`/`act` pensata per
    l'integrazione in prodotti esterni (API, UI web, CLI, ecc.).
    """

    def __init__(self, tools=None):
        super().__init__(tools=tools, name="analista_requisiti", config=None)

    def reply(self, message: str) -> str:
        """Genera una risposta testuale data una richiesta utente."""
        return self.ask(message)

    def act(self, message: str):
        """Restituisce sia il testo della risposta che un semplice payload."""
        answer = self.reply(message)
        return {
            "role": "analista_requisiti",
            "input": message,
            "answer": answer,
        }
