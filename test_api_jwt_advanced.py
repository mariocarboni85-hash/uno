import requests

# Login con utente demo
login_data = {"username": "admin", "password": "adminpass"}
r = requests.post("http://localhost:5000/api/login", json=login_data)
if r.status_code == 200:
    token = r.json()["access_token"]
    print("[LOGIN OK] Token JWT:", token)
    headers = {"Authorization": f"Bearer {token}"}
    # Test /api/me
    r2 = requests.get("http://localhost:5000/api/me", headers=headers)
    print("/api/me:", r2.status_code, r2.json())
    # Test /api/scan_apps
    r3 = requests.get("http://localhost:5000/api/scan_apps", headers=headers)
    print("/api/scan_apps:", r3.status_code, r3.json())
else:
    print("[LOGIN ERROR]", r.text)
