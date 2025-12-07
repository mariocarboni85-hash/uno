"""Custom agent: Demo

This module defines a simple wrapper class around SuperAgent
specialized for: Test
"""
from agent import SuperAgent


class CustomAgent(SuperAgent):
    """Agente custom generato automaticamente."""

    def __init__(self, tools: dict):
        super().__init__(tools, name="Demo")
