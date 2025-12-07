import os
import requests

url = "https://gpt4all.io/models/ggml-gpt4all-j-v1.3-groovy.bin"
dest_folder = os.path.expanduser("~/.gpt4all")
os.makedirs(dest_folder, exist_ok=True)
dest_path = os.path.join(dest_folder, "ggml-gpt4all-j-v1.3-groovy.bin")

print("Scaricamento modello, attendi...")
r = requests.get(url, stream=True)
with open(dest_path, "wb") as f:
    for chunk in r.iter_content(chunk_size=8192):
        if chunk:
            f.write(chunk)
print("Modello scaricato in:", dest_path)
