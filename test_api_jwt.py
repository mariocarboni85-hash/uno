import requests

# 1. Ottieni un token JWT
login_data = {"username": "testuser", "password": "testpass"}
r = requests.post("http://localhost:5050/api/login", json=login_data)
if r.status_code == 200:
    token = r.json()["access_token"]
    print("[LOGIN OK] Token JWT:", token)
    headers = {"Authorization": f"Bearer {token}"}
    # 2. Richiesta autenticata a /api/scan_apps
    r2 = requests.get("http://localhost:5050/api/scan_apps", headers=headers)
    print("/api/scan_apps:", r2.status_code, r2.json())
else:
    print("[LOGIN ERROR]", r.text)
