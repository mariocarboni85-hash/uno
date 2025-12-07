FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
# non eseguire app come root in produzione; creare utente
RUN adduser --disabled-password --gecos '' appuser
USER appuser
ENV PYTHONUNBUFFERED=1
CMD ["python", "super_agent_workspace_main.py"]
