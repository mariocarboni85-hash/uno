def call_llm(model, prompt):
    """
    Chiama il modello LLM/API specificato.
    model: 'default', 'mock', 'ollama', ...
    prompt: string
    """
    if model == 'mock':
        return f"[MOCK] Risposta a: {prompt}"
    elif model == 'ollama':
        try:
            import ollama
            return ollama.generate(model='llama2', prompt=prompt)['response']
        except Exception:
            return '[OLLAMA] Errore o non disponibile.'
    else:
        # Default: echo
        return f"[DEFAULT] {prompt}"
"""LLM helper wrapper for OpenAI Python SDK.

Provides `think(prompt: str)` which returns the assistant reply text.
It tries to import `OPENAI_API_KEY` and `MODEL` from the project's `config` module;
if not found, it reads `OPENAI_API_KEY` and `MODEL` from environment variables.

Usage:
    from tools.llm import think
    text = think("Write a short haiku about code.")

Note: requires the official `openai` package (`pip install openai`).
"""
import os
from typing import Optional

try:
    # prefer project config if available
    from config import OPENAI_API_KEY, MODEL  # type: ignore
except Exception:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL = os.getenv("MODEL", "gpt-4o-mini")

try:
    from openai import OpenAI
except Exception as e:
    OpenAI = None  # type: ignore


def _get_client():
    """Restituisce un client OpenAI oppure None se non configurato.

    Invece di alzare sempre eccezione, qui gestiamo in modo più
    morbido la mancanza di pacchetto o chiave, così il resto del
    sistema può usare un fallback mock (vedi `think`).
    """

    if OpenAI is None:
        return None

    api_key = globals().get("OPENAI_API_KEY")
    if not api_key:
        return None

    return OpenAI(api_key=api_key)


def think(prompt: str, model: Optional[str] = None) -> str:
    """Send `prompt` to the chat completion API and return assistant content.

    - `model`: optional override for the model name. If omitted, will use `MODEL`.

    Returns the assistant reply string.
    """
    client = _get_client()
    model_name = model or globals().get("MODEL") or "gpt-4o-mini"

    # Fallback mock se il client non è disponibile (niente openai o niente chiave)
    if client is None:
        return (
            "[MOCK LLM] Nessun client LLM configurato. Rispondo in modo "
            "fittizio. Prompt ricevuto:\n\n" + prompt[:500]
        )

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": (
                "Se l'utente vuole fare un'azione, rispondi nel formato "
                "ACTION:<tool>:<parametri>. Altrimenti rispondi normalmente."
            )},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1024,
    )

    # navigate response structure: choices[0].message.content
    try:
        return response.choices[0].message.content
    except Exception:
        # fallback: return raw text if structure differs
        return str(response)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        p = " ".join(sys.argv[1:])
    else:
        p = input("Prompt: ")

    try:
        out = think(p)
        print("\nAssistant reply:\n", out)
    except Exception as ex:
        print("Error:", ex)
