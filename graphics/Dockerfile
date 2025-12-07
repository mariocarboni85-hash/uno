FROM python:3.11

WORKDIR /app
COPY . .

RUN pip install pillow svgwrite cairosvg imageio opencv-python

CMD ["python", "graphics.py"]
