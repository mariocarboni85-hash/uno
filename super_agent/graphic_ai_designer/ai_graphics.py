# Modulo AI per generazione grafica avanzata

from PIL import Image, ImageDraw
import svgwrite
import imageio
from diffusers import StableDiffusionPipeline
import torch

class AIGraphics:
    def create_icon(self, filename="ai_icon.png", color="purple"):
        img = Image.new('RGBA', (128, 128), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse((32, 32, 96, 96), fill=color)
        img.save(filename)
        return filename

    def create_svg(self, filename="ai_logo.svg", color="orange"):
        dwg = svgwrite.Drawing(filename, size=(128, 128))
        dwg.add(dwg.circle(center=(64, 64), r=32, fill=color))
        dwg.save()
        return filename

    def create_gif(self, filename="ai_anim.gif"):
        frames = []
        for i in range(10):
            img = Image.new('RGBA', (128, 128), (255, 255, 255, 0))
            draw = ImageDraw.Draw(img)
            draw.ellipse((i*10, i*10, 128-i*10, 128-i*10), fill="cyan")
            frames.append(img)
        frames[0].save(filename, save_all=True, append_images=frames[1:], duration=200, loop=0)
        return filename

    def generate_ai_image(self, prompt, filename="ai_generated.png"):
        print(f"[AI Designer] Generazione immagine AI per prompt: {prompt}")
        pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
        pipe = pipe.to("cpu")
        image = pipe(prompt).images[0]
        image.save(filename)
        print(f"✅ Immagine AI generata: {filename}")
        return filename

def genera_immagine(prompt, nome_file):
    designer = AIGraphics()
    return designer.generate_ai_image(prompt, nome_file)

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        prompt = sys.argv[1]
        nome_file = sys.argv[2]
        genera_immagine(prompt, nome_file)
        print(f"✅ Immagine generata: {nome_file}")
    else:
        print("Usage: python ai_graphics.py '<prompt>' '<nome_file>'")
