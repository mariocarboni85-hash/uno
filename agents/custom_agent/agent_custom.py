"""Custom agent: custom_agent

This module defines a simple wrapper class around SuperAgent
specialized for: Agente custom generato da SuperAgent.
"""
from agent import SuperAgent


class CustomAgent(SuperAgent):
    """Agente custom generato automaticamente."""

    def __init__(self, tools: dict):
        super().__init__(tools, name="custom_agent")
