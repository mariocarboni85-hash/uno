import os
import subprocess
import traceback
from super_agent_workspace.templates.agent_template import AgentBase

class OperationalAgent(AgentBase):
    def handle_message(self, message: str) -> str:
        try:
            msg = message.strip().lower()
            msg = ' '.join(msg.split())

            # --- COMANDI TASK DI COSTRUZIONE ---
            if msg.startswith("crea task") or msg.startswith("aggiungi task"):
                # Esempio: "crea task build app" -> tipo: build, descrizione: app
                parts = msg.split()
                if len(parts) >= 3:
                    task_type = parts[2]
                    descr = ' '.join(parts[3:]) if len(parts) > 3 else ''
                    task = {'type': task_type, 'description': descr, 'status': 'pending'}
                    t = self.app.memory.add_task(task)
                    self.app.job_queue.push(task)
                    return f"Task '{task_type}' aggiunto con id {t['id']}."
                return "Uso: crea task <tipo> <descrizione>"

            if msg.startswith("mostra task") or msg.startswith("elenca task"):
                tasks = self.app.memory.list_tasks()
                if not tasks:
                    return "Nessun task presente."
                return '\n'.join([f"ID:{t['id']} | Tipo:{t['type']} | Stato:{t['status']} | Desc:{t.get('description','')}" for t in tasks])

            if msg.startswith("aggiorna task"):
                # Esempio: "aggiorna task 2 done"
                parts = msg.split()
                if len(parts) >= 4:
                    try:
                        task_id = int(parts[2])
                        status = parts[3]
                        t = self.app.memory.update_task(task_id, status=status)
                        return f"Task {task_id} aggiornato a '{status}'."
                    except Exception as e:
                        return f"Errore aggiornamento: {e}"
                return "Uso: aggiorna task <id> <stato>"

            if msg.startswith("pipeline"):
                # Esempio: "pipeline build app"
                pipeline = msg.replace("pipeline ", "").strip()
                # Aggiungi task multipli di esempio
                steps = pipeline.split()
                ids = []
                for step in steps:
                    task = {'type': step, 'description': pipeline, 'status': 'pending'}
                    t = self.app.memory.add_task(task)
                    self.app.job_queue.push(task)
                    ids.append(str(t['id']))
                return f"Pipeline '{pipeline}' creata con task id: {', '.join(ids)}."
            # Puoi aggiungere altri comandi qui
            return "Comando non riconosciuto."
        except Exception as e:
            return f"Errore nell'agent: {e}"

    def get_reasoning(self, message: str) -> str:
        msg = message.strip().lower()
        if msg.startswith("!python"):
            return "Ricevuto comando Python: verrà eseguito codice dinamico in ambiente isolato."
        if msg.startswith("!run "):
            return "Ricevuto richiesta di esecuzione script Python: verrà avviato il file indicato."
        if msg.startswith("!cmd "):
            return "Ricevuto comando shell: verrà eseguito direttamente nel terminale."
        if msg.startswith("!pip "):
            return "Ricevuto richiesta installazione pacchetto Python: verrà usato pip."
        if msg == "!info":
            return "Richiesta informazioni di sistema: verranno raccolti dati su OS, CPU, RAM, Python."
        if msg == "!list files":
            return "Richiesta elenco file: verrà mostrata la lista dei file nella cartella corrente."
        if msg.startswith("!delete "):
            return "Richiesta eliminazione file: verrà rimosso il file indicato."
        if msg.startswith("!rename "):
            return "Richiesta rinomina file: il file verrà rinominato come richiesto."
        if msg.startswith("!search "):
            return "Richiesta ricerca testo: verrà cercato il testo in tutti i file del progetto."
        if msg.startswith("!git "):
            return "Richiesta comando Git: verrà eseguito il comando git specificato."
        if msg == "!tasklist":
            return "Richiesta task attivi: verrà mostrata la lista dei task (placeholder)."
        if msg == "!agent list":
            return "Richiesta elenco agenti: verrà mostrata la lista degli agenti (placeholder)."
        if msg.startswith("!agent info "):
            return "Richiesta info agente: verranno mostrate le informazioni sull'agente (placeholder)."
        if msg.startswith("!set theme "):
            return "Richiesta cambio tema: verrà impostato il tema richiesto."
        if msg == "!clear chat":
            return "Richiesta pulizia chat: la chat verrà svuotata."
        if msg in ["help", "aiuto", "?", "comandi"]:
            return "Richiesta help: verranno mostrati tutti i comandi disponibili."
        if msg in ["ciao", "salve", "hello", "hi"]:
            return "Saluto rilevato: risposta di benvenuto."
        if any(x in msg for x in ["crea agente", "genera agente", "costruisci agente", "crea un agente", "genera un agente", "costruisci agente base"]):
            return "Richiesta generazione agente: verrà avviata la logica di creazione."
        if msg.startswith("crea file"):
            return "Richiesta creazione file: verrà avviata la logica di creazione."
        if msg.startswith("apri file"):
            return "Richiesta apertura file: verrà avviata la logica di apertura."
        if msg.startswith("crea task") or msg.startswith("aggiungi task"):
            return "Richiesta creazione task di costruzione."
        if msg.startswith("mostra task") or msg.startswith("elenca task"):
            return "Richiesta visualizzazione elenco task."
        if msg.startswith("aggiorna task"):
            return "Richiesta aggiornamento stato task."
        if msg.startswith("pipeline"):
            return "Richiesta creazione pipeline di task."
        return "Messaggio non riconosciuto: verrà gestito in futuro."

    # --- IMPLEMENTAZIONI DEI NUOVI COMANDI ---
    def install_pip_package(self, package: str) -> str:
        try:
            result = subprocess.run(["pip", "install", package], capture_output=True, text=True)
            return f"[pip install]:\n{result.stdout}\n{result.stderr}"
        except Exception as e:
            return f"[pip install error]: {e}"

    def safe_import(self, module_name: str):
        try:
            return __import__(module_name)
        except ModuleNotFoundError:
            self.install_pip_package(module_name)
            try:
                return __import__(module_name)
            except Exception as e:
                return f"[Import error]: {e}"

    def get_system_info(self) -> str:
        import platform
        try:
            import psutil
            ram = f"RAM: {round(psutil.virtual_memory().total/1e9,2)} GB"
        except Exception:
            ram = "RAM: info non disponibile"
        info = [
            f"OS: {platform.system()} {platform.release()}",
            f"Python: {platform.python_version()}",
            f"CPU: {platform.processor()}",
            ram,
        ]
        return "\n".join(info)

    def list_files(self) -> str:
        files = os.listdir()
        return "File nella cartella:\n" + "\n".join(files)

    def delete_file(self, file: str) -> str:
        try:
            os.remove(file)
            return f"File '{file}' eliminato."
        except Exception as e:
            return f"Errore eliminazione: {e}"

    def rename_file(self, old, new) -> str:
        try:
            os.rename(old, new)
            return f"File '{old}' rinominato in '{new}'."
        except Exception as e:
            return f"Errore rinomina: {e}"

    def search_text(self, text: str) -> str:
        result = []
        for root, dirs, files in os.walk('.'):
            for f in files:
                try:
                    path = os.path.join(root, f)
                    with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                        for i, line in enumerate(file):
                            if text in line:
                                result.append(f"{path} [{i+1}]: {line.strip()}")
                except Exception:
                    continue
        return "\n".join(result) if result else "Nessun risultato."

    def run_git_command(self, git_cmd: str) -> str:
        try:
            result = subprocess.run(["git"] + git_cmd.split(), capture_output=True, text=True)
            return f"[Git Output]:\n{result.stdout}\n{result.stderr}"
        except Exception as e:
            return f"[Git Error]: {e}"

    def get_task_list(self) -> str:
        # Placeholder: logica per mostrare i task attivi
        return "[TaskList] Funzione non ancora implementata."

    def list_agents(self) -> str:
        # Placeholder: logica per elencare agenti
        return "[Agent List] Funzione non ancora implementata."

    def agent_info(self, agent_name: str) -> str:
        # Placeholder: logica per info agente
        return f"[Agent Info] Info per '{agent_name}' non ancora implementata."

    def set_theme(self, theme: str) -> str:
        if self.app:
            self.app.set_theme(theme)
            return f"Tema impostato su '{theme}'."
        return "Impossibile cambiare tema: app non collegata."
    """
    Agente operativo per Super Agent Workspace.
    Analizza messaggi in linguaggio naturale, riconosce comandi
    e li esegue realmente sul sistema.
    """

    def __init__(self, app_ref=None):
        super().__init__("OperationalAgent")
        self.app = app_ref

    # --- DISPATCHER PRINCIPALE ---
    def handle_message(self, message: str) -> str:
        try:
            # Normalizzazione avanzata
            msg = message.strip().lower()
            msg = ' '.join(msg.split())  # rimuove spazi multipli

            # Alias e varianti
            if msg in ["info", "!info", "mostra info", "mostra informazioni", "mostra sistema"]:
                return self.get_system_info()

            if msg in ["list files", "!list files", "elenca file", "mostra file", "mostra files"]:
                return self.list_files()

            if msg.startswith("!pip ") or msg.startswith("pip "):
                package = msg.replace("!pip ", "").replace("pip ", "").strip()
                return self.install_pip_package(package)

            if msg.startswith("!delete ") or msg.startswith("delete "):
                file = msg.replace("!delete ", "").replace("delete ", "").strip()
                return self.delete_file(file)

            if msg.startswith("!rename ") or msg.startswith("rename "):
                parts = msg.replace("!rename ", "").replace("rename ", "").split()
                if len(parts) == 2:
                    return self.rename_file(parts[0], parts[1])
                else:
                    return "Uso: !rename <file> <nuovo_nome>"

            if msg.startswith("!search ") or msg.startswith("search "):
                text = msg.replace("!search ", "").replace("search ", "").strip()
                return self.search_text(text)

            if msg.startswith("!git ") or msg.startswith("git "):
                git_cmd = msg.replace("!git ", "").replace("git ", "").strip()
                return self.run_git_command(git_cmd)

            if msg in ["tasklist", "!tasklist", "mostra task", "elenca task"]:
                return self.get_task_list()

            if msg in ["agent list", "!agent list", "elenca agenti", "mostra agenti"]:
                return self.list_agents()

            if msg.startswith("!agent info ") or msg.startswith("agent info "):
                agent_name = msg.replace("!agent info ", "").replace("agent info ", "").strip()
                return self.agent_info(agent_name)

            if msg.startswith("!set theme ") or msg.startswith("set theme "):
                theme = msg.replace("!set theme ", "").replace("set theme ", "").strip()
                return self.set_theme(theme)

            if msg in ["clear chat", "!clear chat", "pulisci chat"]:
                if self.app:
                    self.app.clear_chat()
                return "Chat pulita."

            # Nuovi comandi avanzati
            if message.startswith("!pip "):
                package = message.replace("!pip ", "").strip()
                return self.install_pip_package(package)

            if message == "!info":
                return self.get_system_info()

            if message == "!list files":
                return self.list_files()

            if message.startswith("!delete "):
                file = message.replace("!delete ", "").strip()
                return self.delete_file(file)

            if message.startswith("!rename "):
                parts = message.split()
                if len(parts) == 3:
                    return self.rename_file(parts[1], parts[2])
                else:
                    return "Uso: !rename <file> <nuovo_nome>"

            if message.startswith("!search "):
                text = message.replace("!search ", "").strip()
                return self.search_text(text)

            if message.startswith("!git "):
                git_cmd = message.replace("!git ", "").strip()
                return self.run_git_command(git_cmd)

            if message == "!tasklist":
                return self.get_task_list()

            if message == "!agent list":
                return self.list_agents()

            if message.startswith("!agent info "):
                agent_name = message.replace("!agent info ", "").strip()
                return self.agent_info(agent_name)

            if message.startswith("!set theme "):
                theme = message.replace("!set theme ", "").strip()
                return self.set_theme(theme)

            if message == "!clear chat":
                if self.app:
                    self.app.clear_chat()
                return "Chat pulita."

            # Help base
            if message in ["help", "aiuto", "?", "comandi"]:
                return (
                    "Comandi disponibili:\n"
                    "!python <codice> - Esegui codice Python\n"
                    "!run <file.py> - Esegui uno script Python\n"
                    "!cmd <comando> - Esegui comando shell\n"
                    "!pip <pacchetto> - Installa pacchetto Python\n"
                    "!info - Info sistema\n"
                    "!list files - Elenca file\n"
                    "!delete <file> - Elimina file\n"
                    "!rename <file> <nuovo_nome> - Rinomina file\n"
                    "!search <testo> - Cerca testo nei file\n"
                    "!git <comando> - Comando Git\n"
                    "!tasklist - Mostra task attivi\n"
                    "!agent list - Elenca agenti\n"
                    "!agent info <nome> - Info agente\n"
                    "!set theme <chiaro|scuro> - Cambia tema\n"
                    "!clear chat - Pulisci chat\n"
                    "crea file <nome> - Crea un file\n"
                    "apri file <nome> - Apri file in editor\n"
                    "crea/genera un agente - Crea un nuovo agente\n"
                    "Altri messaggi verranno gestiti in futuro."
                )

            # Risposta automatica a saluti
            if message in ["ciao", "salve", "hello", "hi"]:
                return "Ciao! Sono SuperAgent, pronto ad aiutarti. Scrivi 'help' per vedere i comandi."

            # Comando Python diretto
            if message.startswith("!python"):
                code = message.replace("!python", "").strip()
                return self.run_python(code)

            # Esecuzione di file Python
            if message.startswith("!run "):
                path = message.replace("!run ", "").strip()
                return self.run_script(path)

            # Creazione agenti
            if any(x in msg for x in ["crea agente", "genera agente", "costruisci agente", "crea un agente", "genera un agente", "costruisci agente base"]):
                return self.generate_agent(msg)

            # Creazione file generico
            if message.startswith("crea file"):
                return self.create_file_from_message(message)

            # Apertura file nel tuo editor
            if message.startswith("apri file"):
                return self.open_file_in_editor(message)

            # Comandi terminale diretti
            if message.startswith("!cmd "):
                shell_cmd = message.replace("!cmd ", "").strip()
                return self.run_shell(shell_cmd)

            return "Comando non riconosciuto. Scrivi 'help' per vedere i comandi disponibili."
        except Exception as e:
            return f"[OperationalAgent][Errore]: {e}\n{traceback.format_exc()}"

    def run_python(self, code: str) -> str:
        try:
            import ast
            local_vars = {}
            # Prova a separare l'ultima espressione
            lines = code.strip().split('\n')
            if lines:
                if len(lines) > 1:
                    body = lines[:-1]
                    last = lines[-1]
                else:
                    body = []
                    last = lines[0]
                body_code = '\n'.join(body) if body else ''
                if body_code:
                    exec(body_code, {}, local_vars)
                try:
                    # Prova a valutare l'ultima riga come espressione
                    result = eval(last, {}, local_vars)
                    return f"[Python Output]: {local_vars}\n[Result]: {result}"
                except Exception:
                    # Se non è un'espressione, esegui come statement
                    exec(last, {}, local_vars)
                    return f"[Python Output]: {local_vars}"
            else:
                return "[Python Output]: {}"
        except Exception as e:
            return f"[Python Error]: {e}\n{traceback.format_exc()}"

    def run_script(self, path: str) -> str:
        try:
            result = subprocess.run(["python", path], capture_output=True, text=True)
            return f"[Script Output]:\n{result.stdout}\n[Script Error]:\n{result.stderr}"
        except Exception as e:
            return f"[Script Error]: {e}\n{traceback.format_exc()}"

    def run_shell(self, cmd: str) -> str:
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return f"[Shell Output]:\n{result.stdout}\n[Shell Error]:\n{result.stderr}"
        except Exception as e:
            return f"[Shell Error]: {e}\n{traceback.format_exc()}"

    def generate_agent(self, message: str) -> str:
        # Placeholder: logica di generazione agenti da messaggio
        return "[OperationalAgent] Generazione agente non ancora implementata."

    def create_file_from_message(self, message: str) -> str:
        # Placeholder: logica di creazione file da messaggio
        return "[OperationalAgent] Creazione file non ancora implementata."

    def open_file_in_editor(self, message: str) -> str:
        # Placeholder: logica di apertura file in editor
        return "[OperationalAgent] Apertura file non ancora implementata."
