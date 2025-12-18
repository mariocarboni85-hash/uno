import socket
import time

# Verifica se il server Flask è attivo su localhost:5000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)
try:
    s.connect(("127.0.0.1", 5050))
    print("SERVER ATTIVO su localhost:5000")
    s.close()
    time.sleep(2)  # Attendi che il server sia pronto
    import subprocess
    subprocess.run(["C:/Python314/python.exe", "c:/Users/user/Desktop/m/super_agent/test_api_backend.py"])
except Exception as e:
    print("SERVER NON ATTIVO:", e)
    exit(1)
