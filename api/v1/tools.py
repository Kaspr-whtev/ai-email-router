import smtplib

from email.message import EmailMessage

def send_email(to_email: str, sender_email: str, message_text: str):
    msg = EmailMessage()

    msg["Subject"] = "AI Router Test"
    msg["From"] = "router@example.com"
    msg["To"] = to_email
    msg["Reply-To"] = sender_email
    msg.set_content(message_text)

    with smtplib.SMTP("mailhog", 1025) as smtp:
        smtp.send_message(msg)