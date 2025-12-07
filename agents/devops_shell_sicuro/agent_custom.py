"""Custom agent: Agente DevOps Shell Sicuro

This module defines a simple wrapper class around SuperAgent
specialized for: Agente per eseguire comandi shell con filtri di sicurezza e log.
"""
from agent import SuperAgent


class CustomAgent(SuperAgent):
    """Agente custom generato automaticamente."""

    def __init__(self, tools: dict):
        super().__init__(tools, name="Agente DevOps Shell Sicuro")
