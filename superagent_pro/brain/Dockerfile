FROM python:3.11

RUN apt-get update && \
    apt-get install -y portaudio19-dev ffmpeg python3-opencv xdotool

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "brain.py"]
