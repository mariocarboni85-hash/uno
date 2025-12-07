FROM python:3.11

WORKDIR /app
COPY . .
RUN pip install flask requests schedule

CMD ["python", "optimizer_advanced.py"]
