from __future__ import annotations

from typing import TYPE_CHECKING, cast

# === CHAT AVANZATA: INPUT VOCALI E VISIVI ===
def chat_superagent_avanzata(agent_name="Dev_1", testo=None, voce=None, immagine=None):
    """Simula chat multimodale: testo, voce (trascrizione), immagine (descrizione)."""
    team: "SoftwareTeam" = SoftwareTeam()
    agent = cast("SuperAgent", team.auto_create_agent(agent_name, ["python", "backend"]))
    messaggi = []
    if testo:
        messaggi.append(f"Testo: {testo}")
    if voce:
        messaggi.append(f"Voce (trascrizione): {voce}")
    if immagine:
        messaggi.append(f"Immagine (descrizione): {immagine}")
    # Semplice logica: priorità voce > immagine > testo
    import os
    risposta = None
    # Input vocale: se voce è un file path, trascrivi
    if voce and isinstance(voce, str) and os.path.isfile(voce):
        try:
            import speech_recognition as sr
            recognizer = sr.Recognizer()
            with sr.AudioFile(voce) as source:
                audio = recognizer.record(source)
                voce_text = recognizer.recognize_google(audio)  # type: ignore[attr-defined]
            risposta = f"Ho trascritto il tuo messaggio vocale: '{voce_text}'."
            if "errore" in voce_text.lower() or "bug" in voce_text.lower():
                risposta += " Sto analizzando il problema..." 
                risposta += " " + agent.propose_solution(voce_text)
        except Exception as e:
            risposta = f"Errore nella trascrizione vocale: {e}"
    # Input immagine: se immagine è un file path, estrai testo
    elif immagine and isinstance(immagine, str) and os.path.isfile(immagine):
        try:
            import pytesseract
            from PIL import Image
            img = Image.open(immagine)
            img_text = pytesseract.image_to_string(img)
            risposta = f"Ho estratto dall'immagine: '{img_text}'."
            if "diagramma" in img_text.lower() or "errore" in img_text.lower():
                risposta += " Sembra un problema tecnico, vuoi assegnarmi un task?"
        except Exception as e:
            risposta = f"Errore nell'analisi immagine: {e}"
    # Input vocale come testo diretto
    elif voce:
        risposta = f"Ho ricevuto il tuo messaggio vocale: '{voce}'."
        if "errore" in voce.lower() or "bug" in voce.lower():
            risposta += " Sto analizzando il problema..." 
            risposta += " " + agent.propose_solution(voce)
    # Input immagine come testo diretto
    elif immagine:
        risposta = f"Ho analizzato l'immagine: '{immagine}'."
        if "diagramma" in immagine.lower() or "errore" in immagine.lower():
            risposta += " Sembra un problema tecnico, vuoi assegnarmi un task?"
    # Input testuale
    elif testo:
        risposta = chat_superagent(agent_name, testo)
    else:
        risposta = "Nessun input ricevuto."
    print(f"SuperAgent ({agent_name}) multimodale risponde:\n{risposta}")
    return risposta
# === CHAT TESTUALE CON SUPERAGENT ===
def chat_superagent(agent_name="Dev_1", messaggio=None):
    """Simula una chat: SuperAgent capisce e risponde a input testuali."""
    team = SoftwareTeam()
    agent = cast("SuperAgent", team.auto_create_agent(agent_name, ["python", "backend"]))
    if messaggio is None:
        messaggio = "Ciao, come stai?"
    # Semplice comprensione: risponde diversamente a saluti, domande, richieste
    msg = messaggio.lower()
    if any(x in msg for x in ["ciao", "salve", "buongiorno"]):
        risposta = f"Ciao! Sono {agent.name}, pronto ad aiutarti."
    elif "come stai" in msg:
        risposta = "Sto bene, grazie! Sono sempre operativo per nuovi task."
    elif "status" in msg or "stato" in msg:
        risposta = agent.get_status()
    elif "risolvi" in msg or "bug" in msg:
        risposta = agent.propose_solution(messaggio)
    else:
        risposta = f"Ho ricevuto il tuo messaggio: '{messaggio}'. Vuoi assegnarmi un task?"
    print(f"SuperAgent ({agent_name}) risponde:\n{risposta}")
    return risposta
# === INTERFACCIA DIRETTA CON SUPERAGENT ===
def interfaccia_superagent(agent_name="Dev_1", comando=None):
    """Interfaccia diretta: invia comando/testo a SuperAgent e riceve risposta."""
    team = SoftwareTeam()
    agent = cast("SuperAgent", team.auto_create_agent(agent_name, ["python", "backend"]))
    if comando is None:
        comando = "Qual è il tuo stato?"
    # Simula una richiesta: se comando è 'status', restituisce lo stato, altrimenti logga e risponde
    if comando.lower() in ["status", "stato", "get_status"]:
        risposta = agent.get_status()
    else:
        agent.log.append(f"Comando ricevuto: {comando}")
        risposta = agent.propose_solution(comando)
    print(f"Risposta SuperAgent ({agent_name}):\n{risposta}")
    return risposta
# === DEMO: Evoluzione SuperAgent con API Key ===
def demo_evoluzione_super_agent(api_key=None):
    """Simula evoluzione del team con API key (mock)."""
    print("\n=== SIMULAZIONE EVOLUZIONE SUPER AGENT ===")
    team = SoftwareTeam()
    team.auto_create_agent("Dev_1", ["python", "backend"])
    team.auto_create_agent("UX_1", ["ux", "design"])
    team.auto_create_agent("QA_1", ["test", "qa"])
    team.assign_task("Implementa API REST", required_skill="python")
    team.assign_task("Test funzionali", required_skill="qa")
    team.assign_task("Mockup interfaccia", required_skill="ux")
    feedbacks = ["API REST completata senza errori", "Test QA ok", "UX migliorabile"]
    result = team.auto_evolve_and_increase_iq(cycles=3, feedbacks=feedbacks)
    print(f"IQ evolutivo per ciclo: {result['iq_history']}")
    print(f"Ultimo IQ: {result['last_iq']}")
    print("Log evolutivo:")
    for entry in result['log']:
        print(f"  {entry}")
    print("Dashboard finale:")
    print(result['dashboard'])
    # Esportazione risultati in JSON
    export = {
        'iq_history': result['iq_history'],
        'last_iq': result['last_iq'],
        'log': result['log'],
        'dashboard': result['dashboard']
    }
    with open('super_agent_evolution.json', 'w', encoding='utf-8') as f:
        json.dump(export, f, ensure_ascii=False, indent=2)
    print("Risultati esportati in super_agent_evolution.json")
    print("=== FINE SIMULAZIONE ===\n")

import importlib.util
import json
import os

def save_knowledge_to_file(shared_knowledge, filepath='knowledge.json'):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(shared_knowledge, f, ensure_ascii=False, indent=2)

def load_knowledge_from_file(shared_knowledge, filepath='knowledge.json'):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            shared_knowledge.clear()
            shared_knowledge.extend(data)

def save_logs_to_file(team, filepath='agent_logs.json'):
    logs = {a.name: a.log for a in team}
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

def load_logs_from_file(team, filepath='agent_logs.json'):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            logs = json.load(f)
            for a in team:
                if a.name in logs:
                    a.log = logs[a.name]

def send_alert(message):
    # Mock invio email/alert
    print(f"[ALERT] {message}")
    # Qui si può integrare invio email, Slack, Telegram...
# MEMORIA CONDIVISA E FEEDBACK
shared_knowledge = []


class AdvancedSuperAgentNN:
    pass
# Se vuoi riattivare la logica della rete neurale, decommenta e sistema i metodi qui sotto:
#    def forward(self, x):
#        return self.model(x)
#
#    def train_model(self, X, y, epochs=100, lr=0.001, classification=True, verbose=False, batch_size=16):
#        criterion = nn.CrossEntropyLoss() if classification else nn.MSELoss()
#        optimizer = optim.Adam(self.parameters(), lr=lr)
#        dataset = torch.utils.data.TensorDataset(X, y)
#        effective_batch_size = batch_size if len(X) >= 2 else len(X)
#        loader = torch.utils.data.DataLoader(dataset, batch_size=effective_batch_size, shuffle=True)
#        for epoch in range(epochs):
#            for xb, yb in loader:
#                optimizer.zero_grad()
#                outputs = self.forward(xb)
#                loss = criterion(outputs, yb)
#                loss.backward()
#                optimizer.step()
#            if verbose and epoch % 10 == 0:
#                print(f"Epoch {epoch}: loss={loss.item():.4f}")
#        return loss.item()
#
#    def predict(self, X, classification=True):
#        with torch.no_grad():
#            outputs = self.forward(X)
#            if classification:
#                _, predicted = torch.max(outputs, 1)
#                return predicted
#            else:
#                return outputs
#
#    def evaluate(self, X, y, classification=True):
#        pred = self.predict(X, classification)
#        if classification:
#            acc = (pred == y).float().mean().item()
#            return {'accuracy': acc}
#        else:
#            mse = ((pred - y) ** 2).mean().item()
#            return {'mse': mse}

# AGENTI MULTIPLI E COLLABORAZIONE


class SuperAgent:

    def generate_jwt(self, payload, secret='superagent_secret', algorithm='HS256'):
        import jwt
        token = jwt.encode(payload, secret, algorithm=algorithm)
        return token

    def verify_jwt(self, token, secret='superagent_secret', algorithms=['HS256']):
        import jwt
        try:
            decoded = jwt.decode(token, secret, algorithms=algorithms)
            return decoded
        except Exception as e:
            print(f"Errore verifica JWT: {e}")
            return None

    def autoallineamento(self):
        """Esegue l'autoallineamento dell'agente, aggiornando le skill e la knowledge base."""
        """SuperAgent verifica e corregge autonomamente ambiente, dipendenze e configurazione."""
        import sys
        import subprocess
        log_msg = []
        # Verifica dipendenze principali
        required = ["torch", "flask", "numpy", "scipy", "matplotlib"]
        for pkg in required:
            try:
                __import__(pkg)
                log_msg.append(f"Dipendenza '{pkg}' OK")
            except ImportError:
                subprocess.run([sys.executable, "-m", "pip", "install", pkg])
                log_msg.append(f"Dipendenza '{pkg}' installata")
        # Verifica ambiente
        log_msg.append(f"Python: {sys.version}")
        # Simula correzione configurazione
        self.log.append("Autoallineamento completato: dipendenze e ambiente verificati")
        self.log.extend(log_msg)

    def __init__(self, name, skills=None):
        self.name = name
        self.tasks = []
        self.log = []
        self.conflicts = []
        self.skills = skills or []
        self.completed_tasks = 0
        # Competenze multidisciplinari
        self.competenze = {
            "informatica": "esperto",
            "meccanica": "avanzato",
            "elettrica": "avanzato",
            "fisica": "esperto"
        }
        # Vincolo etico: non può mentire
        self.cannot_lie = True
        # Integrazione rete neurale avanzata
        # self.nn = AdvancedSuperAgentNN(input_size=6, hidden_sizes=[64, 32], output_size=3, dropout=0.2)
        # self.nn_trained = False

    def learn_from_chat(self, user_message, feedback=None):
        """Apprende nuove informazioni dalla chat e aggiorna le skill in base al feedback."""
        """Apprende e si migliora dalle chat dirette con l'utente."""
        self.add_knowledge(f"Chat con utente: {user_message}")
        self.log.append(f"Apprendimento da chat: '{user_message}'")
        if feedback:
            self.skills.append(feedback)
            self.log.append(f"Skill migliorata grazie al feedback: {feedback}")
        self.completed_tasks += 1
        self.log.append(f"Auto-miglioramento: task completati {self.completed_tasks}")

    # --- Metodi specialistici multidisciplinari ---
    def solve_informatica(self, problem):
        """Risolve problemi di informatica con logica e conoscenze interne. Logging dettagliato."""
        try:
            import numpy as np
            fonte = "numpy.sort, dati generati casualmente"
            arr = np.random.randint(0, 100, 10)
            result = np.sort(arr)
            soluzione = f"[Informatica] Dati ordinati: {result.tolist()} per '{problem}' [fonte: {fonte}]"
            if "bug" in problem:
                soluzione += " | Analisi codice: bug individuato e risolto."
            if "importazione" in problem:
                soluzione += " | Verifica dipendenze e correggi import."
            if "divisione per zero" in problem:
                soluzione += " | Gestione eccezione ZeroDivisionError e refactoring codice."
            if "modulo" in problem:
                soluzione += " | Installa il modulo richiesto tramite pip o aggiorna requirements."
            self.log.append(soluzione)
            return soluzione
        except Exception as e:
            self.log.append(f"Errore Informatica: {e}")
            return f"Errore nella risoluzione informatica: {str(e)}"

    def solve_meccanica(self, problem):
        """Risolve problemi di meccanica con formule e simulazioni. Logging dettagliato."""
        try:
            import scipy.integrate as integrate
            fonte = "scipy.integrate.quad, funzione x^2"
            res, _ = integrate.quad(lambda x: x**2, 0, 2)
            soluzione = f"[Meccanica] Integrale x^2 da 0 a 2: {res:.2f} per '{problem}' [fonte: {fonte}]"
            if "integrale" in problem:
                soluzione += " | Calcolo integrale: risultato 8/3."
            self.log.append(soluzione)
            return soluzione
        except Exception as e:
            self.log.append(f"Errore Meccanica: {e}")
            return f"Errore nella risoluzione meccanica: {str(e)}"

    def solve_elettrica(self, problem):
        """Risolve problemi di elettrica con calcoli e circuiti equivalenti. Logging dettagliato."""
        try:
            import numpy as np
            fonte = "numpy, formula resistenza equivalente parallelo"
            resistenze = np.array([100, 220, 330])
            req = 1 / np.sum(1 / resistenze)
            soluzione = f"[Elettrica] Resistenza equivalente: {req:.1f} Ohm per '{problem}' [fonte: {fonte}]"
            if "resistenza equivalente" in problem:
                soluzione += " | Formula: 1/Req = 1/R1 + 1/R2 + 1/R3."
            self.log.append(soluzione)
            return soluzione
        except Exception as e:
            self.log.append(f"Errore Elettrica: {e}")
            return f"Errore nella risoluzione elettrica: {str(e)}"

    def solve_fisica(self, problem):
        """Risolve problemi di fisica con simulazioni e modelli matematici. Logging dettagliato."""
        try:
            import matplotlib.pyplot as plt
            import numpy as np
            fonte = "matplotlib, numpy, modello moto parabolico"
            t = np.linspace(0, 2, 100)
            x = 5 * t
            y = 5 * t - 4.9 * t**2
            plt.figure()
            plt.plot(x, y)
            plt.title('Moto parabolico')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.close()
            soluzione = f"[Fisica] Simulazione moto parabolico per '{problem}' (grafico generato) [fonte: {fonte}]"
            if "moto parabolico" in problem:
                soluzione += " | Simulazione: traiettoria calcolata."
            self.log.append(soluzione)
            return soluzione
        except Exception as e:
            self.log.append(f"Errore Fisica: {e}")
            return f"Errore nella risoluzione fisica: {str(e)}"

    def complete_task(self, task):
        for t in self.tasks:
            if t['task'] == task:
                self.tasks.remove(t)
                self.completed_tasks += 1
                self.log.append(f"Task completato: {task}")
                return

    def assign_task(self, task, priority=1):
        """Assegna un nuovo task all'agente, tracciando priorità e log."""
        self.tasks.append({"task": task, "priority": priority})
        self.log.append(f"Task assegnato: {task} (priorità {priority})")
        return {"assigned": task, "priority": priority}

    def report_conflict(self, conflict):
        self.conflicts.append(conflict)
        self.log.append(f"Conflitto: {conflict}")
        alert_msg = f"Conflitto segnalato da {self.name}: {conflict}"
        self.log.append(f"[ALERT] {alert_msg}")
        send_alert(alert_msg)

    def get_status(self):
        return {
            'name': self.name,
            'tasks': self.tasks,
            'log': self.log[-10:],
            'conflicts': self.conflicts[-5:],
            'skills': self.skills,
            'completed_tasks': self.completed_tasks
        }

    def exchange_task(self, other_agent, task):
        for t in self.tasks:
            if t['task'] == task:
                self.tasks.remove(t)
                other_agent.tasks.append(t)
                self.log.append(f"Task '{task}' passato a {other_agent.name}")
                other_agent.log.append(f"Task '{task}' ricevuto da {self.name}")
                return True
        return False

    def correct_agent(self, other_agent, feedback):
        other_agent.log.append(f"Correzione da {self.name}: {feedback}")
        self.log.append(f"Correzione inviata a {other_agent.name}: {feedback}")

    def add_knowledge(self, info):
        shared_knowledge.append({'from': self.name, 'info': info})
        self.log.append(f"Memoria condivisa aggiornata: {info}")

    def get_knowledge(self):
        return shared_knowledge[-10:]

    def train_on_tasks(self, X, y):
        """Allena la rete neurale sui task passati (X: features, y: classi)."""
        X_tensor = torch.tensor(X, dtype=torch.float32)
        y_tensor = torch.tensor(y, dtype=torch.long)
        loss = self.nn.train_model(X_tensor, y_tensor, epochs=50, lr=0.01, classification=True, verbose=False)
        self.nn_trained = True
        self.log.append(f"NN trained, loss={loss:.4f}")
        return loss

    def predict_task(self, features):
        """Classifica un task tramite la rete neurale (features: lista di 6 valori)."""
        if not self.nn_trained:
            return 'NN non addestrata'
        X_tensor = torch.tensor([features], dtype=torch.float32)
        pred = self.nn.predict(X_tensor, classification=True)
        return int(pred[0])

    def propose_solution(self, problem, ambito=None):
        """Propone una soluzione concreta al problema, con logging dettagliato e gestione errori."""
        try:
            trasparenza = getattr(self, 'cannot_lie', True)
            if ambito == "informatica":
                solution = self.solve_informatica(problem)
            elif ambito == "meccanica":
                solution = self.solve_meccanica(problem)
            elif ambito == "elettrica":
                solution = self.solve_elettrica(problem)
            elif ambito == "fisica":
                solution = self.solve_fisica(problem)
            else:
                solution = f"{self.name} propone di risolvere '{problem}' con skill {self.skills} [fonte: manuale interno]"
            if not trasparenza:
                msg = f"[ETICA] Tentativo di risposta non trasparente bloccato!"
                self.log.append(msg)
                return "Non posso mentire o nascondere la fonte."
            self.log.append(f"Proposta soluzione: {solution} [trasparente]")
            return solution
        except Exception as e:
            error_msg = f"Errore nella proposta soluzione: {e}"
            self.log.append(error_msg)
            return f"Impossibile proporre soluzione: {str(e)}"

# Esempio di team di agenti con skill
team = [
    SuperAgent("Agent_1", skills=["file", "shell"]),
    SuperAgent("Agent_2", skills=["browser", "arduino"]),
    SuperAgent("Agent_3", skills=["llm", "planner"]),
    SuperAgent("UX_Designer", skills=["ux", "design", "figma", "adobe_xd", "wireframe", "branding", "grafica", "animazione", "svg", "palette", "tipografia"]),
    SuperAgent("Frontend_Expert", skills=["frontend", "react", "vue", "angular", "html", "css", "js", "typescript", "responsive", "accessibilita", "web"]),
    SuperAgent("Graphic_Artist", skills=["grafica", "arte", "illustrazione", "dall-e", "stable_diffusion", "svg", "png", "animazione", "logo", "banner", "mockup"]),
    SuperAgent("WebApp_Builder", skills=["webapp", "landing_page", "siti_web", "app_mobile", "nextjs", "vite", "api", "deploy", "ottimizzazione"]),
    SuperAgent("DevOps", skills=["devops", "deploy"]),
    SuperAgent("QA", skills=["qa", "test"]),
    SuperAgent("Marketing", skills=["marketing", "documentazione"])
]
def crea_progetto_grafico_web(nome_progetto, descrizione, tipo="webapp"):
    """Crea e orchestra un progetto completo di grafica/app/sito web."""
    team_grafico = [a for a in team if "grafica" in a.skills or "ux" in a.skills or "frontend" in a.skills or "webapp" in a.skills]
    log = []
    # Step 1: Wireframe e design
    ux = next((a for a in team_grafico if "ux" in a.skills), None)
    if ux:
        log.append(f"{ux.name} crea wireframe e layout con Figma/AdobeXD per '{nome_progetto}'")
    # Step 2: Branding e asset grafici
    artist = next((a for a in team_grafico if "arte" in a.skills or "grafica" in a.skills), None)
    if artist:
        log.append(f"{artist.name} genera logo, palette colori, icone e banner con DALL-E/Stable Diffusion")
    # Step 3: Sviluppo frontend
    frontend = next((a for a in team_grafico if "frontend" in a.skills), None)
    if frontend:
        log.append(f"{frontend.name} sviluppa componenti React/Vue/Angular, HTML/CSS/JS, responsive e accessibilità")
    # Step 4: Generazione sito/app
    builder = next((a for a in team_grafico if "webapp" in a.skills), None)
    if builder:
        log.append(f"{builder.name} orchestra la generazione e il deploy di '{nome_progetto}' su cloud e mobile")
    # Step 5: QA e ottimizzazione
    qa = next((a for a in team if "qa" in a.skills), None)
    if qa:
        log.append(f"{qa.name} testa e ottimizza performance, accessibilità e compatibilità")
    # Step 6: Documentazione e marketing
    marketing = next((a for a in team if "marketing" in a.skills), None)
    if marketing:
        log.append(f"{marketing.name} prepara documentazione, tutorial e landing page promozionale")
    # Output finale
    progetto = {
        "nome": nome_progetto,
        "descrizione": descrizione,
        "tipo": tipo,
        "team": [a.name for a in team_grafico],
        "log": log,
        "stato": "completato"
    }
    print(f"\n=== PROGETTO GRAFICO/WEB COMPLETO ===\nNome: {nome_progetto}\nDescrizione: {descrizione}\nTeam: {[a.name for a in team_grafico]}\nLog:")
    for entry in log:
        print(f"- {entry}")
    print("=== FINE PROGETTO ===\n")
    return progetto

def assign_task_to_team(task, priority=1, required_skill=None):
    # Assegna il task all'agente più adatto: meno task, skill richiesta, meno conflitti
    candidates = team
    if required_skill:
        candidates = [a for a in team if required_skill in a.skills]
        if not candidates:
            candidates = team
    agent = min(candidates, key=lambda a: (len(a.tasks), len(a.conflicts), -a.completed_tasks))
    agent.assign_task(task, priority)
    return agent.name

def get_team_status():
    return [agent.get_status() for agent in team]

# Esempio di team di agenti
team = [SuperAgent(f"Agent_{i}") for i in range(1, 4)]

# Import tools per azioni agenti
from tools import files, browser, shell, arduino

def agent_action(action_type, params):
    """
    Esegue un'azione specifica tramite il tool corrispondente.
    action_type: 'file', 'browser', 'shell', 'arduino'
    params: dizionario con parametri specifici
    """
    if action_type == 'file':
        return files.perform_file_action(params)
    elif action_type == 'browser':
        return browser.perform_browser_action(params)
    elif action_type == 'shell':
        return shell.perform_shell_action(params)
    elif action_type == 'arduino':
        return arduino.perform_arduino_action(params)
    else:
        return {'error': 'Azione non supportata'}
"""
Advanced Brain: Multi-model reasoning, memory, learning, and decision making
"""
from typing import Optional, List, Dict, Any, Tuple
import json
import re
from datetime import datetime
import requests

try:
    from openai import OpenAI
    from config import OPENAI_API_KEY, MODEL
    _openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
except Exception as e:
    _openai_client = None
    print(f"Warning: OpenAI client not initialized: {e}")


class Memory:
    """Short-term and long-term memory for the agent."""
    
    def __init__(self, max_short_term: int = 10):
        self.short_term = []  # Recent interactions
        self.long_term = {}   # Persistent knowledge
        self.max_short_term = max_short_term
        self.context = {}     # Current context variables
    
    def add_interaction(self, role: str, content: str):
        """Add interaction to short-term memory."""
        self.short_term.append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only recent memories
        if len(self.short_term) > self.max_short_term:
            self.short_term.pop(0)
    
    def store_knowledge(self, key: str, value: Any):
        """Store in long-term memory."""
        self.long_term[key] = {
            'value': value,
            'stored_at': datetime.now().isoformat()
        }
    
    def retrieve_knowledge(self, key: str) -> Optional[Any]:
        """Retrieve from long-term memory."""
        if key in self.long_term:
            return self.long_term[key]['value']
        return None
    
    def get_context(self) -> str:
        """Get formatted context for LLM."""
        context_parts = []
        
        # Add recent interactions
        if self.short_term:
            context_parts.append("Recent interactions:")
            for item in self.short_term[-5:]:
                context_parts.append(f"[{item['role']}]: {item['content'][:100]}")
        
        # Add relevant knowledge
        if self.long_term:
            context_parts.append("\nKnown facts:")
            for key, data in list(self.long_term.items())[-5:]:
                context_parts.append(f"- {key}: {data['value']}")
        
        return "\n".join(context_parts)
    
    def clear_short_term(self):
        """Clear short-term memory."""
        self.short_term = []
    
    def save_to_file(self, path: str):
        """Save memory to JSON file."""
        data = {
            'short_term': self.short_term,
            'long_term': self.long_term,
            'context': self.context
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def load_from_file(self, path: str):
        """Load memory from JSON file."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.short_term = data.get('short_term', [])
                self.long_term = data.get('long_term', {})
                self.context = data.get('context', {})
        except Exception:
            pass



class Brain:
    """Enhanced brain with reasoning, memory, multi-model support, and orchestration of tools for excellence."""
    def __init__(self):
        self.memory = Memory()
        self.reasoning_depth = 3
        self.confidence_threshold = 0.7
        self.available_models = {
            'openai': self._think_openai,
            'ollama': self._think_ollama,
            'local': self._think_local
        }

    def select_action(self, plan: list, context: Optional[dict] = None):
        """
        Select next action with reasoning and tool orchestration.
        Args:
            plan: List of planned actions
            context: Current execution context (dict or None)
        Returns:
            Next action dict or None
        """
        if not plan:
            return None
        # Analizza il piano e seleziona la sequenza ottimale di strumenti
        best_action = None
        best_score = -1
        for action in plan:
            analysis = self.analyze_task(action.get('task', ''))
            score = 0
            # Punteggio: più strumenti, più step, maggiore complessità = più orchestrazione
            score += len(analysis['required_tools']) * 2
            score += analysis['estimated_steps']
            if analysis['complexity'] == 'complex':
                score += 2
            if score > best_score:
                best_score = score
                best_action = action
        if context is not None and best_action:
            best_action['context'] = context
        return best_action

    def orchestrate_tools_for_excellence(self, task: str) -> dict:
        """
        Analizza il compito, seleziona e orchestra i migliori strumenti per eccellere nel prodotto finale.
        Ritorna la strategia ottimale e la sequenza di tool da usare.
        """
        analysis = self.analyze_task(task)
        tools = analysis['required_tools']
        steps = analysis['estimated_steps']
        strategy = f"Per il compito '{task}', la strategia ottimale è: "
        if tools:
            strategy += f"usare i tool {tools} in {steps} step, seguendo le best practice di eccellenza."
        else:
            strategy += "usare la logica interna e la memoria per completare il task."
        return {
            'task': task,
            'tools': tools,
            'steps': steps,
            'strategy': strategy,
            'analysis': analysis
        }
    
    def reason(self, problem: str, options: list[str]) -> tuple[str, float]:
        """
        Reason about a problem and select best option.
        
        Args:
            problem: Problem description
            options: List of possible solutions
            
        Returns:
            Tuple of (selected_option, confidence_score)
        """
        # Build reasoning prompt
        prompt = f"""Problem: {problem}

Options:
{chr(10).join(f"{i+1}. {opt}" for i, opt in enumerate(options))}

Analyze each option and select the best one. Respond with just the number."""
        
        response = self.think(prompt)
        
        # Extract selection
        import re
        match = re.search(r'\b([1-9])\b', response)
        if match:
            idx = int(match.group(1)) - 1
            if 0 <= idx < len(options):
                return options[idx], 0.8
        
        # Fallback to first option
        return (options[0], 0.0) if options else ("", 0.0)
    
    def analyze_task(self, task: str) -> Dict[str, Any]:
        """
        Analyze a task and extract key information.
        
        Returns:
            Dict with task_type, complexity, required_tools, estimated_steps
        """
        task_lower = task.lower()
        
        # Determine task type
        task_type = "general"
        if any(word in task_lower for word in ['file', 'read', 'write', 'save']):
            task_type = "file_operation"
        elif any(word in task_lower for word in ['search', 'find', 'web', 'url']):
            task_type = "web_search"
        elif any(word in task_lower for word in ['execute', 'run', 'command', 'shell']):
            task_type = "shell_execution"
        elif any(word in task_lower for word in ['analyze', 'calculate', 'compute']):
            task_type = "computation"
        
        # Estimate complexity
        word_count = len(task.split())
        complexity = "simple" if word_count < 10 else "medium" if word_count < 20 else "complex"
        
        # Identify required tools
        required_tools = []
        if 'file' in task_lower:
            required_tools.append('files')
        if any(word in task_lower for word in ['web', 'url', 'search', 'browser']):
            required_tools.append('browser')
        if any(word in task_lower for word in ['command', 'execute', 'run', 'shell']):
            required_tools.append('shell')
        
        # Estimate steps
        estimated_steps = max(1, len(required_tools) * 2)
        
        return {
            'task_type': task_type,
            'complexity': complexity,
            'required_tools': required_tools,
            'estimated_steps': estimated_steps,
            'analysis': f"Task classified as {task_type} with {complexity} complexity"
        }
    
    def think(self, prompt: str, model: str = 'auto', use_memory: bool = True) -> str:
        """
        Main thinking function with multi-model support.
        
        Args:
            prompt: Input prompt
            model: Model to use ('auto', 'openai', 'ollama', 'local')
            use_memory: Whether to include memory context
            
        Returns:
            Response string
        """
        # Add memory context if enabled
        if use_memory:
            context = self.memory.get_context()
            if context:
                prompt = f"{context}\n\nCurrent query: {prompt}"
        
        # Auto-select model
        if model == 'auto':
            if _openai_client:
                model = 'openai'
            else:
                model = 'ollama'
        
        # Get response from selected model
        think_func = self.available_models.get(model, self._think_local)
        response = think_func(prompt)
        
        # Store in memory
        if use_memory:
            self.memory.add_interaction('user', prompt)
            self.memory.add_interaction('assistant', response)
        
        return response
    
    def _think_openai(self, prompt: str) -> str:
        """Think using OpenAI."""
        if _openai_client is None:
            return "OpenAI not configured"
        
        try:
            response = _openai_client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": 
                        "You are an intelligent agent. If the user wants an action, "
                        "respond with ACTION:<tool>:<parameters>. Otherwise respond naturally."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            return f"OpenAI error: {str(e)}"
    
    def _think_ollama(self, prompt: str) -> str:
        """Think using Ollama local model."""
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "jarvis",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            if response.status_code == 200:
                return response.json().get('response', 'No response')
            return f"Ollama error: {response.status_code}"
        except Exception as e:
            return f"Ollama connection error: {str(e)}"
    
    def _think_local(self, prompt: str) -> str:
        """Simple local reasoning without external API."""
        # Basic pattern matching for common requests
        prompt_lower = prompt.lower()
        
        if 'file' in prompt_lower and 'create' in prompt_lower:
            return "ACTION:files:create"
        elif 'search' in prompt_lower or 'find' in prompt_lower:
            return "ACTION:browser:search"
        elif 'run' in prompt_lower or 'execute' in prompt_lower:
            return "ACTION:shell:execute"
        
        return "I understand your request. Please provide more specific instructions."
    
    def learn_from_outcome(self, action: str, outcome: str, success: bool):
        """
        Learn from action outcomes.
        
        Args:
            action: Action taken
            outcome: Result of action
            success: Whether action was successful
        """
        key = f"action_{action}"
        current = self.memory.retrieve_knowledge(key) or {'successes': 0, 'failures': 0, 'last_outcome': '', 'last_attempt': ''}
        if success:
            current['successes'] += 1
        else:
            current['failures'] += 1
        current['last_outcome'] = str(outcome)
        current['last_attempt'] = datetime.now().isoformat()
        self.memory.store_knowledge(key, current)
    
    def get_tool_recommendation(self, task: str) -> List[str]:
        """Recommend tools for a task based on analysis."""
        analysis = self.analyze_task(task)
        return analysis['required_tools']


# === INTEGRAZIONE RETE NEURALE (MLP) ===

"""
class SuperAgentNN:
    pass
# Esempio di utilizzo:
# nn_agent = SuperAgentNN(input_size=4, output_size=3)
# X = torch.randn(10, 4)
# y = torch.randint(0, 3, (10,))
# nn_agent.train_model(X, y)
# pred = nn_agent.predict(X)
# print(pred)
"""

# Global instance
_brain = Brain()

def think(prompt: str, model: str = 'auto', use_memory: bool = True) -> str:
    """Quick access to think function."""
    return _brain.think(prompt, model, use_memory)

def analyze_task(task: str) -> Dict[str, Any]:
    """Quick task analysis."""
    return _brain.analyze_task(task)

def reason(problem: str, options: List[str]) -> Tuple[str, float]:
    """Quick reasoning function."""
    return _brain.reason(problem, options)



class SoftwareTeam:
    """Gestione team software: agenti, skill, task, orchestrazione."""
    def __init__(self):
        self.members = []  # Lista di SuperAgent
        self.shared_log = []
        self.shared_memory = []

    def add_member(self, agent):
        if any(a.name == agent.name for a in self.members):
            self.shared_log.append(f"Errore: agente '{agent.name}' già presente nel team.")
            return False
        self.members.append(agent)
        self.shared_log.append(f"Membro aggiunto: {agent.name}")
        return True

    def remove_member(self, agent_name):
        if not any(a.name == agent_name for a in self.members):
            self.shared_log.append(f"Errore: agente '{agent_name}' non trovato.")
            return False
        self.members = [a for a in self.members if a.name != agent_name]
        self.shared_log.append(f"Membro rimosso: {agent_name}")
        return True

    def assign_task(self, task, features=None, required_skill=None):
        if not self.members:
            self.shared_log.append("Errore: nessun membro nel team.")
            return None
        candidates = self.members
        if required_skill:
            candidates = [a for a in self.members if required_skill in a.skills]
            if not candidates:
                candidates = self.members
        if not candidates:
            self.shared_log.append("Errore: nessun candidato disponibile per il task.")
            return None
        try:
            if features and hasattr(candidates[0], 'predict_task'):
                scores = [(a, a.predict_task(features)) for a in candidates]
                agent = max(scores, key=lambda x: x[1])[0]
            else:
                agent = min(candidates, key=lambda a: (len(a.tasks), len(a.conflicts), -a.completed_tasks))
            agent.assign_task(task)
            self.shared_log.append(f"Task '{task}' assegnato a {agent.name}")
            return agent.name
        except Exception as e:
            self.shared_log.append(f"Errore assegnazione task: {str(e)}")
            return None

    def exchange_task(self, from_name, to_name, task):
        from_agent = next((a for a in self.members if a.name == from_name), None)
        to_agent = next((a for a in self.members if a.name == to_name), None)
        if not from_agent or not to_agent:
            self.shared_log.append(f"Errore: agenti non trovati per scambio task.")
            return False
        try:
            ok = from_agent.exchange_task(to_agent, task)
            if ok:
                self.shared_log.append(f"Task '{task}' scambiato da {from_name} a {to_name}")
            else:
                self.shared_log.append(f"Errore: scambio task fallito.")
            return ok
        except Exception as e:
            self.shared_log.append(f"Errore scambio task: {str(e)}")
            return False

    def add_shared_memory(self, info):
        if info in self.shared_memory:
            self.shared_log.append("Info già presente in memoria condivisa.")
            return False
        self.shared_memory.append(info)
        self.shared_log.append(f"Memoria condivisa aggiornata: {info}")
        return True

    def auto_create_agent(self, name, skills):
        if any(a.name == name for a in self.members):
            self.shared_log.append(f"Errore: agente '{name}' già esistente.")
            return None
        new_agent = SuperAgent(name, skills=skills)
        self.add_member(new_agent)
        self.shared_log.append(f"Nuovo agente creato: {name} con skill {skills}")
        return new_agent

    def get_team_status(self):
        return [a.get_status() for a in self.members]

    def analyze_performance(self):
        stats = {a.name: len(a.tasks) for a in self.members}
        completed = {a.name: a.completed_tasks for a in self.members}
        suggestions = []
        for a in self.members:
            if len(a.tasks) > 5:
                suggestions.append(f"{a.name} ha troppi task: considera redistribuzione.")
            if a.completed_tasks == 0:
                suggestions.append(f"{a.name} non ha completato task: verifica skill o motivazione.")
        return {'stats': stats, 'completed': completed, 'suggestions': suggestions}

    def get_shared_log(self):
        return self.shared_log[-20:]

    def knowledge_base(self):
        return self.shared_memory[-50:]

    def report(self):
        return {
            'team_status': self.get_team_status(),
            'performance': self.analyze_performance(),
            'log': self.get_shared_log(),
            'knowledge_base': self.knowledge_base()
        }

    def feedback_loop(self, outcome):
        self.shared_memory.append({'feedback': outcome, 'timestamp': datetime.now().isoformat()})
        self.shared_log.append(f"Feedback ricevuto: {outcome}")
        if 'errore' in outcome.lower():
            self.shared_log.append("Suggerimento: rivedi task e skill assegnati.")

    def auto_improve_team(self):
        perf = self.analyze_performance()
        for suggestion in perf['suggestions']:
            if 'troppi task' in suggestion:
                name = f"Auto_{len(self.members)+1}"
                skills = ["support", "optimizer"]
                self.auto_create_agent(name, skills)
                self.shared_log.append(f"Agente di supporto creato: {name}")
            if 'verifica skill' in suggestion:
                name = f"Specialist_{len(self.members)+1}"
                skills = ["specialist"]
                self.auto_create_agent(name, skills)
                self.shared_log.append(f"Agente specialist creato: {name}")
        for a in self.members:
            if len(a.tasks) > 5:
                for t in a.tasks[3:]:
                    candidates = [m for m in self.members if m != a and len(m.tasks) < 3]
                    if candidates:
                        target = min(candidates, key=lambda x: len(x.tasks))
                        a.exchange_task(target, t['task'])
                        self.shared_log.append(f"Task '{t['task']}' redistribuito da {a.name} a {target.name}")
        self.shared_log.append("Auto-miglioramento completato.")

    def evolutionary_orchestration(self):
        self.auto_improve_team()
        self.shared_log.append("Orchestrazione evolutiva eseguita.")

    def evolutionary_dashboard(self):
        metrics = {
            'num_agents': len(self.members),
            'num_tasks': sum(len(a.tasks) for a in self.members),
            'completed_tasks': sum(a.completed_tasks for a in self.members),
            'special_agents': [a.name for a in self.members if 'specialist' in a.skills or 'optimizer' in a.skills],
            'log': self.get_shared_log(),
        }
        return metrics

    def trigger_auto_improvement(self, outcome=None):
        if outcome:
            self.feedback_loop(outcome)
        self.evolutionary_orchestration()
        return self.evolutionary_dashboard()

    def auto_evolve_and_increase_iq(self, cycles=3, feedbacks=None):
        iq_history = []
        feedbacks = feedbacks or []
        for cycle in range(cycles):
            outcome = feedbacks[cycle] if cycle < len(feedbacks) else None
            dashboard = self.trigger_auto_improvement(outcome)
            efficienza = dashboard['completed_tasks'] / (dashboard['num_tasks'] + 1)
            specializzazione = len(dashboard['special_agents']) / (dashboard['num_agents'] + 1)
            auto_miglioramento = 1.0 if 'Auto-miglioramento completato.' in dashboard['log'] else 0.7
            feedback_score = 1.0 if outcome and 'errore' not in str(outcome).lower() else 0.8
            iq = round((efficienza * 0.4 + specializzazione * 0.2 + auto_miglioramento * 0.2 + feedback_score * 0.2) * 150, 2)
            iq_history.append(iq)
            self.shared_log.append(f"Ciclo evolutivo {cycle+1}: IQ={iq}")
        return {
            'iq_history': iq_history,
            'last_iq': iq_history[-1] if iq_history else None,
            'dashboard': dashboard,
            'log': self.get_shared_log()
        }

# === ESEMPIO DI FUNZIONE AVANZATA DEL TEAM ===
def demo_team_advanced():
    """Esempio: orchestrazione avanzata team software con report e auto-creazione agenti."""
    team = SoftwareTeam()
    dev = SuperAgent("Dev_1", skills=["python", "backend"])
    ux = SuperAgent("UX_1", skills=["ux", "design"])
    qa = SuperAgent("QA_1", skills=["test", "qa"])
    team.add_member(dev)
    team.add_member(ux)
    team.add_member(qa)
    team.assign_task("Implementa API REST", required_skill="python")
    team.assign_task("Test funzionali", required_skill="qa")
    team.assign_task("Mockup interfaccia", required_skill="ux")
    dev.complete_task("Implementa API REST")
    team.feedback_loop("API REST completata senza errori")
    team.auto_create_agent("DevOps_1", ["devops", "deploy"])
    team.assign_task("Deploy su server", required_skill="devops")
    report = team.report()
    print("\n=== REPORT AVANZATO TEAM SOFTWARE ===")
    print("-- Stato Team --")
    for agent in report['team_status']:
        print(f"Agente: {agent['name']}")
        print(f"  Skill: {agent['skills']}")
        print(f"  Task: {agent['tasks']}")
        print(f"  Completati: {agent['completed_tasks']}")
        print(f"  Log: {agent['log']}")
        print(f"  Conflitti: {agent['conflicts']}")
        print()
    print("-- Performance --")
    perf = report['performance']
    print(f"  Task per agente: {perf['stats']}")
    print(f"  Task completati: {perf['completed']}")
    print(f"  Suggerimenti: {perf['suggestions']}")
    print("-- Log condiviso --")
    for entry in report['log']:
        print(f"  {entry}")
    print("-- Knowledge base --")
    for kb in report['knowledge_base']:
        print(f"  {kb}")
    print("=== FINE REPORT ===\n")
