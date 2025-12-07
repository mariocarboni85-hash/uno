FROM python:3.11

WORKDIR /app
COPY . .
RUN pip install docker schedule requests

CMD ["python", "self_healing.py"]
