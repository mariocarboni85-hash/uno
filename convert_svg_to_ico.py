# Conversione automatica SVG -> ICO per SuperAgent
# Richiede: pip install cairosvg pillow

import cairosvg
from PIL import Image
import os

svg_path = r'C:/Users/user/Desktop/m/SuperAgent/superagent_icon.svg'
png_path = r'C:/Users/user/Desktop/m/SuperAgent/superagent_icon.png'
ico_path = r'C:/Users/user/Desktop/m/SuperAgent/icon.ico'

# Converti SVG in PNG
cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=256, output_height=256)

# Converti PNG in ICO
img = Image.open(png_path)
img.save(ico_path, format='ICO', sizes=[(256,256), (128,128), (64,64), (32,32), (16,16)])

print('Icona .ico generata con successo!')
