"""Custom agent: Agente Copy Marketing

This module defines a simple wrapper class around SuperAgent
specialized for: Agente per generare testi marketing (email, landing, social) in italiano.
"""
from agent import SuperAgent


class CustomAgent(SuperAgent):
    """Agente custom generato automaticamente."""

    def __init__(self, tools: dict):
        super().__init__(tools, name="Agente Copy Marketing")
