# super_agent.py

import random
import datetime
import logging
import smtplib
from email.mime.text import MIMEText
from flask import Flask, render_template_string, request
import threading
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
import requests
import time
# --- Modulo AI reale (esempio semplificato) ---
from sklearn.linear_model import LinearRegression

# Configurazione logging dettagliato
logging.basicConfig(filename='super_agent_log.txt', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

# --- Email Report ---
def send_email_report(subject, body, to_email):
    from_email = 'superagent@example.com'
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    try:
        with smtplib.SMTP('localhost') as server:
            server.sendmail(from_email, [to_email], msg.as_string())
        print(f"Email inviata a {to_email}")
    except Exception as e:
        print(f"Errore invio email: {e}")

# --- Dashboard Web ---
app = Flask(__name__)
DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>SuperAgent Dashboard</title></head>
<body>
    <h1>SuperAgent Dashboard</h1>
    <h2>Report Periodico</h2>
    <pre>{{ log }}</pre>
    <h2>Grafico Performance</h2>
    <img src="data:image/png;base64,{{ chart }}" />
</body>
</html>
'''

@app.route('/')
def dashboard():
    try:
        with open('super_agent_log.txt', 'r') as f:
            log = f.read()
    except Exception:
        log = 'Nessun log disponibile.'
    # Estrai dati per grafico (esempio: numero strategie per giorno)
    days = []
    strategies = []
    for line in log.splitlines():
        if 'auto-miglioramento del' in line:
            day = line.split('auto-miglioramento del ')[-1].strip()
            days.append(day)
        if 'strategia ottimizzata' in line:
            strategies.append(len(strategies)+1)
    if not days:
        days = ['Oggi']
        strategies = [len(strategies)]
    # Crea grafico
    fig, ax = plt.subplots()
    ax.plot(days, strategies, marker='o')
    ax.set_xlabel('Giorno')
    ax.set_ylabel('Strategie Ottimizzate')
    ax.set_title('Evoluzione Strategie')
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)
    chart_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return render_template_string(DASHBOARD_TEMPLATE, log=log, chart=chart_base64)

def start_dashboard():
    app.run(port=5000)

def calculate_qi_test():
    # Simulazione test QI: 10 domande, punteggio casuale
    domande = [f"Domanda {i+1}" for i in range(10)]
    risposte = np.random.randint(0, 2, size=10)  # 0=errata, 1=corretta
    punteggio = risposte.sum() * 10
    rapporto = f"\n[TEST QI SUPER AGENT]\n"
    for i, r in enumerate(risposte):
        rapporto += f"{domande[i]}: {'corretta' if r else 'errata'}\n"
    rapporto += f"Punteggio totale: {punteggio}/100\n"
    if punteggio >= 80:
        rapporto += "Valutazione: Eccellente\n"
    elif punteggio >= 60:
        rapporto += "Valutazione: Buono\n"
    else:
        rapporto += "Valutazione: Migliorabile\n"
    return rapporto

class SuperAgent:
    def __init__(self, nome):
        self.nome = nome
        self.status = 'Pronto'
        self.last_task = None
        self.last_result = None
        self.knowledge_base = []
        self.agents = []
        self.strategies = []
        self.anomalies = []
    def run_task(self, task):
        self.last_task = task
        self.status = 'Lavorando'
        result = None
        if task == 'analizza ambiente':
            result = self.analyze_environment()
        elif task == 'gestisci agenti':
            result = self.orchestrate_agents()
        elif task == 'report performance':
            result = self.generate_performance_report()
        elif task == 'ottimizza strategia':
            result = self.optimize_strategy()
        elif task == 'auto-apprendimento':
            result = self.self_learn()
        elif task == 'monitoraggio':
            result = self.monitor_and_autocorrect()
        else:
            result = f'{self.nome}: task sconosciuto'
        self.last_result = result
        self.status = 'Pronto'
        return result

    def analyze_environment(self):
        # Meta-ragionamento: analizza agenti, task, strategie
        analysis = f'{self.nome}: analisi ambiente, agenti={len(self.agents)}, strategie={len(self.strategies)}'
        self.knowledge_base.append(analysis)
        return analysis

    def orchestrate_agents(self):
        # Orchestrazione: coordina agenti, delega task
        if not self.agents:
            return f'{self.nome}: nessun agente da orchestrare'
        orchestration = f'{self.nome}: orchestrazione agenti completata'
        self.strategies.append('orchestrazione')
        return orchestration

    def generate_performance_report(self):
        # Report: analizza knowledge base e strategie
        report = f'{self.nome}: report performance - {len(self.knowledge_base)} analisi, {len(self.strategies)} strategie'
        return report

    def optimize_strategy(self):
        # Ottimizzazione: crea e testa nuove strategie
        new_strategy = f'Strategia_{len(self.strategies)+1}'
        self.strategies.append(new_strategy)
        return f'{self.nome}: strategia ottimizzata ({new_strategy})'

    def self_learn(self):
        # Auto-apprendimento: apprende da errori e successi
        learning = f'{self.nome}: apprendimento automatico eseguito'
        self.knowledge_base.append(learning)
        return learning

    def monitor_and_autocorrect(self):
        # Monitoraggio e auto-correzione
        anomaly = f'Anomalia_{len(self.anomalies)+1}'
        self.anomalies.append(anomaly)
        correction = f'{self.nome}: monitoraggio e correzione ({anomaly})'
        return correction

    def interface_external_system(self, system_name):
        # Interfaccia con sistemi esterni
        return f'{self.nome}: interfacciato con {system_name}'

    def daily_self_improvement(self):
        # Simula auto-allenamento quotidiano
        today = datetime.date.today().isoformat()
        improvement = f"{self.nome}: auto-miglioramento del {today}"
        self.knowledge_base.append(improvement)
        self.optimize_strategy()
        self.self_learn()
        self.monitor_and_autocorrect()
        return improvement

    def ecosystem_self_analysis(self):
        # Analizza tutto l'ecosistema e propone miglioramenti
        analysis = self.analyze_environment()
        perf = self.generate_performance_report()
        suggestion = f"{self.nome}: suggerimento miglioramento ecosistema"
        self.knowledge_base.append(suggestion)
        return f"{analysis}\n{perf}\n{suggestion}"

    def run_automatic_tests(self, num_tests=5):
        # Esegue test automatici su tutte le funzioni
        print(f"\n[Test automatici SuperAgent]")
        results = []
        tasks = ['analizza ambiente', 'gestisci agenti', 'report performance', 'ottimizza strategia', 'auto-apprendimento', 'monitoraggio']
        for i in range(num_tests):
            task = random.choice(tasks)
            result = self.run_task(task)
            print(f"Test {i+1}: {task} -> {result}")
            results.append(result)
        print("[Fine test automatici]\n")
        return results

    def log_periodic_report(self):
        report = self.generate_performance_report()
        improvement = self.daily_self_improvement()
        analysis = self.ecosystem_self_analysis()
        log_entry = f"\n[REPORT PERIODICO]\n{report}\n{improvement}\n{analysis}\n"
        logging.info(log_entry)
        print(log_entry)
        # Invio email (modifica l'indirizzo per test reale)
        send_email_report('SuperAgent Report', log_entry, 'tuo@email.it')
        return log_entry

    # Funzione avanzata: suggerimento intelligente
    def smart_suggestion(self):
        # Analizza knowledge base e propone miglioramento
        if len(self.strategies) > 5:
            return f"{self.nome}: suggerisco di testare una nuova strategia basata su AI."
        else:
            return f"{self.nome}: continua con ottimizzazione incrementale."

    def run_qi_test(self):
        report = calculate_qi_test()
        self.knowledge_base.append(report)
        print(report)
        return report

    def ai_predict_performance(self):
        # Simula analisi predittiva con AI
        X = np.array([[i] for i in range(len(self.strategies))])
        y = np.array([i*10+50 for i in range(len(self.strategies))])  # Punteggio simulato
        if len(X) > 1:
            model = LinearRegression().fit(X, y)
            next_strategy = len(self.strategies)+1
            pred = model.predict(np.array([[next_strategy]]))[0]
            return f"{self.nome}: previsione performance prossima strategia = {pred:.1f}"
        else:
            return f"{self.nome}: dati insufficienti per previsione AI"

    def multi_agent_test(self, num_agents=3):
        print("\n[Test multi-agente]")
        agents = [SuperAgent(f"SuperAgent_{i+1}") for i in range(num_agents)]
        for agent in agents:
            agent.run_automatic_tests(num_tests=5)
            agent.daily_self_improvement()
            agent.ecosystem_self_analysis()
            agent.log_periodic_report()
            agent.run_qi_test()
            print(agent.smart_suggestion())
            print(agent.ai_predict_performance())
        print("[Fine test multi-agente]\n")

    def communicate_with_agent(self, agent_url, message):
        try:
            response = requests.post(agent_url, json={"message": message})
            return f"{self.nome}: risposta da {agent_url} -> {response.text}"
        except Exception as e:
            return f"{self.nome}: errore comunicazione con {agent_url}: {e}"

    def broadcast_message(self, agent_urls, message):
        results = []
        for url in agent_urls:
            result = self.communicate_with_agent(url, message)
            results.append(result)
        return results

    def collaborative_task(self, agent_urls, task):
        # Invia task a tutti gli agenti e raccoglie le risposte
        print(f"\n[Collaborative Task: {task}]")
        responses = self.broadcast_message(agent_urls, f"Esegui: {task}")
        for resp in responses:
            print(resp)
        print("[Fine collaborazione]\n")
        return responses

class AgentNetwork:
    def __init__(self, agent_count, base_url):
        self.agent_urls = [f"{base_url}/message?agent={i+1}" for i in range(agent_count)]
    def simulate_network(self, super_agent, task):
        print(f"\n[Simulazione rete di {len(self.agent_urls)} agenti]")
        responses = super_agent.collaborative_task(self.agent_urls, task)
        print("Risposte dalla rete:")
        for resp in responses:
            print(resp)
        print("[Fine simulazione rete]\n")

# Endpoint Flask per ricevere messaggi da altri agenti
@app.route('/message', methods=['POST'])
def receive_message():
    agent_id = request.args.get('agent', '1')
    data = request.get_json()
    msg = data.get('message', '')
    reply = f"SuperAgent_{agent_id} ha ricevuto: {msg}"
    return reply, 200

if __name__ == "__main__":
    super_agent = SuperAgent('SuperAgent')
    print(super_agent.run_task('analizza ambiente'))
    print(super_agent.run_task('gestisci agenti'))
    print(super_agent.run_task('report performance'))
    print(super_agent.run_task('ottimizza strategia'))
    print(super_agent.run_task('auto-apprendimento'))
    print(super_agent.run_task('monitoraggio'))
    print(super_agent.interface_external_system('CloudAPI'))
    print(super_agent.daily_self_improvement())
    print(super_agent.ecosystem_self_analysis())
    super_agent.run_automatic_tests(num_tests=5)
    super_agent.log_periodic_report()
    print(super_agent.smart_suggestion())
    super_agent.run_qi_test()
    # Avvia dashboard web in thread separato
    threading.Thread(target=start_dashboard, daemon=True).start()
    print('Dashboard web disponibile su http://localhost:5000')
    # Attendi che la dashboard sia pronta
    time.sleep(2)
    # Test comunicazione singola
    print(super_agent.communicate_with_agent('http://localhost:5000/message', 'Ciao da SuperAgent!'))
    # Test collaborazione multi-agente (simulando più endpoint)
    agent_urls = ['http://localhost:5000/message', 'http://localhost:5000/message']
    super_agent.collaborative_task(agent_urls, 'analizza ambiente')
    # Simulazione rete di agenti (esempio: 5 agenti)
    network = AgentNetwork(agent_count=5, base_url='http://localhost:5000')
    network.simulate_network(super_agent, 'ottimizza strategia')
