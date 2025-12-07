import docker
import schedule
import time
from datetime import datetime

client = docker.from_env()

CONTAINERS = [
    "core", "brain", "team_a", "team_b", "team_c", "gateway", "logger", "scheduler", "security", "storage", "analytics", "events", "mobile_api", "optimizer", "sandbox", "optimizer_advanced", "agent_hub", "agent_evolution", "self_healing", "graphics"
]

def check_and_repair():
    print(f"[{datetime.now()}] 🔍 Auto-diagnosi dei container in corso...")
    report = []
    for name in CONTAINERS:
        try:
            container = client.containers.get(name)
            status = container.attrs['State']['Status']
            if status != "running":
                msg = f"[Self-Healing] ⚠️ Container {name} non attivo. Riavvio in corso..."
                print(msg)
                report.append(msg)
                container.restart()
            else:
                msg = f"[Self-Healing] Container {name} OK"
                print(msg)
                report.append(msg)
        except Exception as e:
            msg = f"[Self-Healing] Errore con {name}: {e}"
            print(msg)
            report.append(msg)
            try:
                client.containers.run(name, detach=True)
                msg = f"[Self-Healing] Container {name} ricreato con successo"
                print(msg)
                report.append(msg)
            except:
                msg = f"[Self-Healing] Impossibile ricreare {name}"
                print(msg)
                report.append(msg)
    # Verifica dipendenze e log
    # (Placeholder: qui si possono aggiungere controlli su requirements, log, aggiornamenti)
    with open("self_healing_report.txt", "a", encoding="utf-8") as f:
        f.write(f"\n[{datetime.now()}] Report auto-diagnosi:\n")
        for line in report:
            f.write(line + "\n")

def main():
    schedule.every(5).minutes.do(check_and_repair)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
