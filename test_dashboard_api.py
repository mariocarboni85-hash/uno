import requests

def test_run_task():
    url = "http://127.0.0.1:5000/api/run"
    payload = {"agent": "system", "task": {"action": "check"}}
    r = requests.post(url, json=payload)
    print("Status:", r.status_code)
    print("Response:", r.json())

if __name__ == "__main__":
    test_run_task()
