"""Configurazione base per l'agente Copy Marketing."""

import os


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL_NAME = os.getenv("LLM_MODEL", "gpt-4o-mini")

SYSTEM_PROMPT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "prompts", "system_prompt.txt"
)
"""File generato automaticamente.

Descrizione: configurazione modelli e toni di voce
"""
