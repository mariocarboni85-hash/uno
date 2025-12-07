"""Client locale per LLM (es. Ollama) usato da Super Agent.

Questo modulo è pensato per convivere con altri agenti che usano
lo stesso server LLM locale. Non mantiene stato globale e legge
endpoint/modello da variabili d'ambiente opzionali.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import urllib.request
import urllib.error


DEFAULT_ENDPOINT = os.getenv("SUPER_AGENT_LLM_ENDPOINT", "http://localhost:11434/api/generate")
DEFAULT_MODEL = os.getenv("SUPER_AGENT_LLM_MODEL", "llama3")


@dataclass
class LLMResponse:
    """Risposta semplificata dal modello LLM locale."""

    text: str
    raw: Dict[str, Any]


class LocalLLMClient:
    """Client minimale per LLM locale compatibile con Ollama.

    Questo client:
    - usa solo HTTP POST,
    - è stateless e quindi non entra in conflitto con altri agenti,
    - permette di selezionare endpoint/modello via env senza toccare codice.
    """

    def __init__(
        self,
        endpoint: str = DEFAULT_ENDPOINT,
        model: str = DEFAULT_MODEL,
        timeout: float = 60.0,
    ) -> None:
        self.endpoint = endpoint
        self.model = model
        self.timeout = timeout

    def generate(self, prompt: str, model: Optional[str] = None) -> LLMResponse:
        """Invia un prompt al modello locale e restituisce il testo generato.

        Il parametro ``model`` permette a Super Agent di usare un modello
        diverso da altri agenti, se necessario, evitando conflitti.
        """

        payload: Dict[str, Any] = {
            "model": model or self.model,
            "prompt": prompt,
            # Per default teniamo una generazione semplice, senza streaming.
            "stream": False,
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.endpoint,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = resp.read().decode("utf-8")
        except urllib.error.URLError as exc:  # tipo rete/endpoint non raggiungibile
            raise RuntimeError(f"Errore di connessione al LLM locale: {exc}") from exc

        try:
            parsed = json.loads(body)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Risposta LLM non valida: {body[:200]}") from exc

        # Formato tipico Ollama: { "response": "...", ... }
        text = parsed.get("response") or parsed.get("message") or ""
        return LLMResponse(text=text, raw=parsed)


# Client di default usato da Super Agent; stateless e condivisibile.
def get_default_client() -> LocalLLMClient:
    return LocalLLMClient()
