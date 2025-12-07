import schedule, time
from flask import Flask

app = Flask(__name__)

def job():
    print("Job eseguito")

schedule.every(60).seconds.do(job)

@app.route("/scheduler/ping")
def ping():
    return {"scheduler": "alive"}

if __name__ == "__main__":
    import threading
    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(1)
    threading.Thread(target=run_scheduler, daemon=True).start()
    app.run(host="0.0.0.0", port=8007)