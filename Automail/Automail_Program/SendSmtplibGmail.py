import smtplib
from email.mime.text import MIMEText
import app
import random as r


def receive_values(sender_email, sender_password, receiver_email, subject, content, IsRecovery):
    global Content, Sender_password, Sender_email, VerificationCode

    VerificationCode = r.randint(100000, 999999)

    if IsRecovery:
        Content = MIMEText(f"Your recovery code is: {VerificationCode}")
        Content["Subject"] = "Automail - Verification code"
        Content["From"] = "[YOUR SENDER EMAIL HERE]"
        Content["To"] = receiver_email
        Sender_email = "[YOUR SENDER EMAIL HERE]"
        Sender_password = "[YOUR SENDER PASSWORD HERE]"
    else:
        Content = MIMEText(content)
        Content["From"] = sender_email
        Sender_email = sender_email
        Sender_password = sender_password
        Content["To"] = receiver_email
        Content["Subject"] = subject

    main()

def VerifyCode(code):
    if int(code) == VerificationCode:
        return True
    else:
        return False


def main():
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(Sender_email, Sender_password)
            smtp.send_message(Content)
    except Exception as e:
        app.erro_email(e)

if __name__ == "__main__":
    main()
