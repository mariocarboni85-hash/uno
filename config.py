"""Configuration for SuperAgent."""
import os

# Root folder for the project
ROOT = os.path.dirname(__file__)
DEFAULT_OUTPUT = os.path.join(ROOT, 'output')

# OpenAI configuration: prefer explicit values set here, otherwise fall back to
# environment variables. Leave as None to force usage of environment vars.
# You can set these here or export `OPENAI_API_KEY` and `MODEL` in your shell.
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', None)  # Sostituire con la propria chiave o impostare variabile d'ambiente
# Default model can be overridden by setting MODEL env var or editing this file.
MODEL = os.getenv('MODEL', 'gpt-4o-mini')  # Modelli validi: gpt-4o-mini, gpt-4o, gpt-4-turbo
