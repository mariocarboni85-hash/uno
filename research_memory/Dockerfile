FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y curl sqlite3

COPY . .
RUN pip install -r requirements.txt

CMD ["python", "research_memory.py"]
