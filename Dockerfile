FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV PYTHONUNBUFFERED=1

# Create a non-root user for running the app
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser || \
	(adduser --disabled-password --gecos '' appuser)
USER appuser

CMD ["python", "-m", "uno"]
