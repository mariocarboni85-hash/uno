from PIL import Image, ImageDraw, ImageFont
import svgwrite
import imageio
import os

# --- Funzione per creare icona raster ---
def crea_icona(nome_file="icona_app.png", colore="red"):
    img = Image.new('RGBA', (128, 128), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((32, 32, 96, 96), fill=colore)
    img.save(nome_file)
    print(f"✅ Icona creata: {nome_file}")

# --- Funzione per creare SVG vettoriale ---
def crea_svg(nome_file="logo_app.svg", colore="blue"):
    dwg = svgwrite.Drawing(nome_file, size=(128, 128))
    dwg.add(dwg.circle(center=(64, 64), r=32, fill=colore))
    dwg.save()
    print(f"✅ SVG creato: {nome_file}")

# --- Funzione per creare GIF animata semplice ---
def crea_gif(nome_file="animazione.gif"):
    frames = []
    for i in range(10):
        img = Image.new('RGBA', (128, 128), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse((i*10, i*10, 128-i*10, 128-i*10), fill="green")
        frames.append(img)
    frames[0].save(nome_file, save_all=True, append_images=frames[1:], duration=200, loop=0)
    print(f"✅ GIF creata: {nome_file}")

# --- Test del modulo ---
if __name__ == "__main__":
    crea_icona()
    crea_svg()
    crea_gif()
