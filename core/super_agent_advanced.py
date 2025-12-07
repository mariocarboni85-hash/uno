import requests
REMOTE_DEVICES = [{"url": "http://192.168.1.20:5500", "api_key": "MASTER_SLAVE_KEY"}]

def send_task_remote(task):
    for device in REMOTE_DEVICES:
        headers = {"Authorization": f"Bearer {device['api_key']}"}
        try:
            resp = requests.post(f"{device['url']}/task/add", json=task, headers=headers, timeout=10)
            if resp.status_code == 200:
                print(f"Task inviato a {device['url']} con successo.")
            else:
                print(f"Errore invio task a {device['url']}: {resp.status_code} - {resp.text}")
        except Exception as e:
            print(f"Errore invio task a {device['url']}: {e}")

# Stub per schedule_task e get_task_status
# Da implementare secondo la logica del sistema

def schedule_task(task):
    print(f"Task schedulato: {task}")
    # Qui va la logica reale di scheduling

def get_task_status():
    # Qui va la logica reale di status
    return {"tasks": []}
