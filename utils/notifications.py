import smtplib
from email.mime.text import MIMEText
from plyer import notification
import requests

# Notifica desktop
def notify_desktop(title, message):
    notification.notify(title=title, message=message, timeout=5)

# Notifica email
def notify_email(subject, message, to_email):
    from_email = "tua_email@gmail.com"
    password = "password_email"  # meglio usare app password
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(from_email, password)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(f"Errore invio email: {e}")

# Notifica webhook (es. Telegram bot)
def notify_webhook(url, message):
    try:
        requests.post(url, json={"text": message})
    except Exception as e:
        print(f"Errore invio webhook: {e}")
