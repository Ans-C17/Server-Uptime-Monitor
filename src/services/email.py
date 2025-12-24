import smtplib
from email.mime.text import MIMEText
import os
from src.core.config import RECEIVER, SMTP_SERVER, SMTP_PORT

def send_email(message, subject):
    sender = os.getenv("EMAIL")
    app_password = os.getenv("PASS")

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = RECEIVER

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(sender, app_password)
            server.send_message(msg)
    except Exception as e:
        print(f"{e}")