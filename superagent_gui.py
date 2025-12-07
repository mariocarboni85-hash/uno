import tkinter as tk
from tkinter import scrolledtext
from core.brain import interfaccia_superagent

def send_command():
    agent_name = agent_entry.get()
    command = command_entry.get()
    response = interfaccia_superagent(agent_name, command)
    output_text.config(state='normal')
    output_text.insert(tk.END, f"\n> {command}\n{response}\n")
    output_text.config(state='disabled')
    command_entry.delete(0, tk.END)

root = tk.Tk()
root.title("SuperAgent GUI")
root.geometry("600x400")

frame = tk.Frame(root)
frame.pack(pady=10)

agent_label = tk.Label(frame, text="Nome agente:")
agent_label.grid(row=0, column=0, padx=5)
agent_entry = tk.Entry(frame)
agent_entry.insert(0, "Dev_1")
agent_entry.grid(row=0, column=1, padx=5)

command_label = tk.Label(frame, text="Comando:")
command_label.grid(row=1, column=0, padx=5)
command_entry = tk.Entry(frame, width=40)
command_entry.grid(row=1, column=1, padx=5)

send_btn = tk.Button(frame, text="Invia", command=send_command)
send_btn.grid(row=1, column=2, padx=5)

output_text = scrolledtext.ScrolledText(root, state='disabled', width=70, height=18)
output_text.pack(pady=10)

root.mainloop()
