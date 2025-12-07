import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
from core.brain import interfaccia_superagent, demo_evoluzione_super_agent, SuperAgent, chat_superagent_avanzata
from tools.library_updater import LibraryUpdater
import threading

def run_in_thread(func):
    def wrapper(*args, **kwargs):
        threading.Thread(target=func, args=args, kwargs=kwargs, daemon=True).start()
    return wrapper

class SuperAgentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SuperAgent - Interfaccia Completa")
        self.root.geometry("800x600")
        self.setup_widgets()

    def setup_widgets(self):
        tab_control = ttk.Notebook(self.root)
        self.tab_direct = ttk.Frame(tab_control)
        self.tab_evolution = ttk.Frame(tab_control)
        self.tab_specialist = ttk.Frame(tab_control)
        self.tab_chat = ttk.Frame(tab_control)
        self.tab_updater = ttk.Frame(tab_control)
        tab_control.add(self.tab_direct, text='Interfaccia Diretta')
        tab_control.add(self.tab_evolution, text='Evoluzione')
        tab_control.add(self.tab_specialist, text='Soluzioni Specialistiche')
        tab_control.add(self.tab_chat, text='Chat Multimodale')
        tab_control.add(self.tab_updater, text='Library Updater')
        tab_control.pack(expand=1, fill='both')
        self.setup_direct_tab()
        self.setup_evolution_tab()
        self.setup_specialist_tab()
        self.setup_chat_tab()
        self.setup_updater_tab()

    def setup_direct_tab(self):
        frame = tk.Frame(self.tab_direct)
        frame.pack(pady=10)
        tk.Label(frame, text="Nome agente:").grid(row=0, column=0, padx=5)
        self.agent_entry = tk.Entry(frame)
        self.agent_entry.insert(0, "Dev_1")
        self.agent_entry.grid(row=0, column=1, padx=5)
        tk.Label(frame, text="Comando:").grid(row=1, column=0, padx=5)
        self.command_entry = tk.Entry(frame, width=40)
        self.command_entry.grid(row=1, column=1, padx=5)
        send_btn = tk.Button(frame, text="Invia", command=self.send_command)
        send_btn.grid(row=1, column=2, padx=5)
        self.output_text = scrolledtext.ScrolledText(self.tab_direct, state='disabled', width=90, height=20)
        self.output_text.pack(pady=10)

    @run_in_thread
    def send_command(self):
        agent_name = self.agent_entry.get()
        command = self.command_entry.get()
        response = interfaccia_superagent(agent_name, command)
        self.output_text.config(state='normal')
        self.output_text.insert(tk.END, f"\n> {command}\n{response}\n")
        self.output_text.config(state='disabled')
        self.command_entry.delete(0, tk.END)

    def setup_evolution_tab(self):
        frame = tk.Frame(self.tab_evolution)
        frame.pack(pady=10)
        tk.Label(frame, text="Evoluzione SuperAgent:").pack()
        evo_btn = tk.Button(frame, text="Esegui Evoluzione", command=self.run_evolution)
        evo_btn.pack(pady=5)
        self.evo_output = scrolledtext.ScrolledText(self.tab_evolution, state='disabled', width=90, height=20)
        self.evo_output.pack(pady=10)

    @run_in_thread
    def run_evolution(self):
        import io, sys
        old_stdout = sys.stdout
        sys.stdout = mystdout = io.StringIO()
        demo_evoluzione_super_agent()
        sys.stdout = old_stdout
        result = mystdout.getvalue()
        self.evo_output.config(state='normal')
        self.evo_output.insert(tk.END, result + "\n")
        self.evo_output.config(state='disabled')

    def setup_specialist_tab(self):
        frame = tk.Frame(self.tab_specialist)
        frame.pack(pady=10)
        tk.Label(frame, text="Soluzioni Specialistiche:").pack()
        spec_btn = tk.Button(frame, text="Esegui Test Specialistico", command=self.run_specialist)
        spec_btn.pack(pady=5)
        self.spec_output = scrolledtext.ScrolledText(self.tab_specialist, state='disabled', width=90, height=20)
        self.spec_output.pack(pady=10)

    @run_in_thread
    def run_specialist(self):
        agent = SuperAgent("SuperExpert")
        problemi = [
            ("Trova il bug in un algoritmo", "informatica"),
            ("Calcola la resistenza equivalente di tre resistenze", "elettrica"),
            ("Simula il moto parabolico di un oggetto", "fisica"),
            ("Calcola l'integrale di x^2 da 0 a 2", "meccanica"),
        ]
        self.spec_output.config(state='normal')
        for testo, ambito in problemi:
            soluzione = agent.propose_solution(testo, ambito)
            self.spec_output.insert(tk.END, f"[{ambito}] {soluzione}\n")
        self.spec_output.config(state='disabled')

    def setup_chat_tab(self):
        frame = tk.Frame(self.tab_chat)
        frame.pack(pady=10)
        tk.Label(frame, text="Chat Multimodale:").grid(row=0, column=0, padx=5)
        self.chat_agent_entry = tk.Entry(frame)
        self.chat_agent_entry.insert(0, "Dev_1")
        self.chat_agent_entry.grid(row=0, column=1, padx=5)
        tk.Label(frame, text="Testo:").grid(row=1, column=0, padx=5)
        self.chat_text_entry = tk.Entry(frame, width=40)
        self.chat_text_entry.grid(row=1, column=1, padx=5)
        tk.Label(frame, text="Voce:").grid(row=2, column=0, padx=5)
        self.chat_voice_entry = tk.Entry(frame, width=40)
        self.chat_voice_entry.grid(row=2, column=1, padx=5)
        tk.Label(frame, text="Immagine:").grid(row=3, column=0, padx=5)
        self.chat_img_entry = tk.Entry(frame, width=40)
        self.chat_img_entry.grid(row=3, column=1, padx=5)
        chat_btn = tk.Button(frame, text="Invia", command=self.send_chat)
        chat_btn.grid(row=4, column=1, pady=5)
        self.chat_output = scrolledtext.ScrolledText(self.tab_chat, state='disabled', width=90, height=16)
        self.chat_output.pack(pady=10)

    @run_in_thread
    def send_chat(self):
        agent_name = self.chat_agent_entry.get()
        testo = self.chat_text_entry.get()
        voce = self.chat_voice_entry.get()
        immagine = self.chat_img_entry.get()
        response = chat_superagent_avanzata(agent_name, testo=testo, voce=voce, immagine=immagine)
        self.chat_output.config(state='normal')
        self.chat_output.insert(tk.END, f"\n> Testo: {testo}, Voce: {voce}, Immagine: {immagine}\n{response}\n")
        self.chat_output.config(state='disabled')
        self.chat_text_entry.delete(0, tk.END)
        self.chat_voice_entry.delete(0, tk.END)
        self.chat_img_entry.delete(0, tk.END)

    def setup_updater_tab(self):
        frame = tk.Frame(self.tab_updater)
        frame.pack(pady=10)
        tk.Label(frame, text="Library Updater:").pack()
        update_btn = tk.Button(frame, text="Verifica pacchetti obsoleti", command=self.run_updater)
        update_btn.pack(pady=5)
        self.updater_output = scrolledtext.ScrolledText(self.tab_updater, state='disabled', width=90, height=16)
        self.updater_output.pack(pady=10)

    @run_in_thread
    def run_updater(self):
        updater = LibraryUpdater()
        venv_name = ".venv" if (updater.venvs_dir / ".venv").exists() else "super_agent_advanced"
        outdated = updater.list_outdated_packages(venv_name)
        self.updater_output.config(state='normal')
        self.updater_output.insert(tk.END, f"Pacchetti obsoleti trovati: {len(outdated)}\n{outdated}\n")
        self.updater_output.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = SuperAgentGUI(root)
    root.mainloop()
