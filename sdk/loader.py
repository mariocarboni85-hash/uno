"""SDK locale per caricare agenti custom in modo uniforme.

Fornisce funzioni di utilità per istanziare un agente custom da
una cartella `agents/<nome>/` e ottenere un oggetto con metodi
standardizzati `reply(message: str)` e `act(message: str)`.
"""
from pathlib import Path
from importlib import import_module
from typing import Any


def load_custom_agent(agent_name: str, tools: dict | None = None) -> Any:
    """Carica dinamicamente `CustomAgent` da agents/<agent_name>/agent_custom.py.

    Restituisce un'istanza di CustomAgent. Solleva ImportError se
    il modulo o la classe non sono disponibili.
    """
    base_package = f"agents.{agent_name}.agent_custom"
    module = import_module(base_package)

    if not hasattr(module, "CustomAgent"):
        raise ImportError(f"CustomAgent non trovato in {base_package}")

    CustomAgent = getattr(module, "CustomAgent")
    tools = tools or {}
    return CustomAgent(tools)


__all__ = ["load_custom_agent"]
