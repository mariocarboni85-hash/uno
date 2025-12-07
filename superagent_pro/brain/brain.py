from flask import Flask, request
import requests
import speech_recognition as sr
try:
    import pyttsx3
except ImportError:
    pyttsx3 = None
try:
    import cv2
except ImportError:
    cv2 = None
try:
    from pynput.keyboard import Controller as KeyController
except ImportError:
    KeyController = None
try:
    from pynput.mouse import Controller as MouseController
except ImportError:
    MouseController = None
try:
    import openai
except ImportError:
    openai = None

app = Flask(__name__)

keyboard = KeyController() if KeyController else None
mouse = MouseController() if MouseController else None
if openai:
    openai.api_key = "INSERISCI_TUA_API_KEY"

# --- AUDIO INPUT ---
def ascolta():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ascolto...")
        audio = r.listen(source)
        try:
            # Verifica che il metodo esista
            if hasattr(r, "recognize_google"):
                text = r.recognize_google(audio, language="it-IT")
            else:
                text = "Metodo recognize_google non disponibile."
            return text
        except Exception as e:
            return f"Errore: {e}"

# --- AUDIO OUTPUT ---
tts = pyttsx3.init()
def parla(testo):
    if pyttsx3:
        tts = pyttsx3.init()
        tts.say(testo)
        tts.runAndWait()
    else:
        print(f"Sintesi vocale non disponibile: {testo}")

# --- VISIONE ---
def analizza_camera():
    if cv2:
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        cam.release()
        return frame
    else:
        print("OpenCV non disponibile")
        return None

# --- CONTROLLO PC ---
def scrivi_testo(t):
    if keyboard:
        for c in t:
            keyboard.press(c)
            keyboard.release(c)
    else:
        print(f"Keyboard non disponibile: {t}")

def muovi_mouse(x, y):
    if mouse:
        mouse.position = (x, y)
    else:
        print(f"Mouse non disponibile: ({x}, {y})")

# --- API ---
@app.route("/voice", methods=["GET"])
def voice_cmd():
    text = ascolta()
    parla(f"Hai detto: {text}")
    return {"msg": text}

@app.route("/vision", methods=["GET"])
def vision_cmd():
    frame = analizza_camera()
    if frame is not None and cv2:
        cv2.imwrite("frame.jpg", frame)
        return {"status": "ok", "file": "frame.jpg"}
    else:
        return {"status": "errore", "file": None}

@app.route("/pc", methods=["POST"])
def pc_cmd():
    data = request.json or {}
    action = data.get("action")
    value = data.get("value")

    if action == "type" and value:
        scrivi_testo(value)
    if action == "mouse" and value and isinstance(value, (list, tuple)) and len(value) == 2:
        muovi_mouse(value[0], value[1])

    return {"status": "done"}

@app.route("/research", methods=["POST"])
def research_data():
    data = request.json
    print("\n[RICERCA] Dati ricevuti:", data)
    return {"status": "ok"}

@app.route("/brain/query", methods=["POST"])
def brain_query():
    req = request.json or {}
    query_text = req.get("query", "")

    # 1️⃣ Consulta la memoria
    try:
        memory_results = requests.get("http://research_memory:5000/memory").json()
    except:
        memory_results = {}

    # 2️⃣ Consulta dati freschi dal container research_memory
    try:
        fresh_data = requests.get("http://research_memory:5000/alive").json()
    except:
        fresh_data = {}

    # 3️⃣ Risposta integrata
    response = {
        "memory": memory_results,
        "fresh_data_status": fresh_data.get("status", "offline"),
        "query": query_text
    }

    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
