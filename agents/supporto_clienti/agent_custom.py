"""Custom agent: Agente Supporto Clienti

This module defines a simple wrapper class around SuperAgent
specialized for: Agente per rispondere a email/FAQ in italiano usando file FAQ locali.
"""
from agent import SuperAgent


class CustomAgent(SuperAgent):
    """Agente custom generato automaticamente."""

    def __init__(self, tools: dict):
        super().__init__(tools, name="Agente Supporto Clienti")
