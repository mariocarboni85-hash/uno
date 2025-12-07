# Agente Analista Requisiti

Questo agente è pensato per supportare l'analisi dei requisiti
software: raccoglie input dagli stakeholder, li chiarisce, li
struttura in requisiti funzionali e non funzionali e propone
domande di approfondimento.

## Requisiti

- Python 3.10+
- Una chiave API valida per il provider LLM (es. OpenAI)

## Configurazione

1. Apri `config/requirements_config.py` e:
   - imposta la tua `OPENAI_API_KEY` (oppure gestiscila tramite
     variabili d'ambiente nel tuo progetto principale),
   - verifica `MODEL_NAME` e gli altri parametri.

2. (Opzionale) Prepara un file di contesto con descrizioni di
   dominio o linee guida di progetto (es. `data/contesto_progetto.md`).

## Uso

Dalla root del progetto principale:

```powershell
python agents\analista_requisiti\run_custom.py
```

In alternativa, puoi usare lo SDK:

```python
from sdk.loader import load_custom_agent

agent = load_custom_agent("analista_requisiti")
risposta = agent.reply("Raccogli i requisiti per un gestionale HR")
```

## Limitazioni

- L'agente non sostituisce un analista umano esperto: le proposte
  vanno sempre riviste e validate dal team.
- Non ha accesso automatico ai sistemi aziendali o ai documenti:
  devi fornirgli il contesto tramite prompt o integrazioni esterne.
