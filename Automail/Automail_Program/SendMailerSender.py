from mailersend import MailerSendClient, EmailBuilder
import app

Sender_email = None
Sender_name = None
Receiver_email = None
Subject = None
Content = None

def receive_values(sender_email,  sender_name, receiver_email, subject, content, key):
    global Sender_email, Sender_name, Receiver_email, Subject, Content, API, ms

    Sender_email = sender_email
    Sender_name = sender_name
    Receiver_email = receiver_email
    Subject = subject
    Content = content
    API = key
    ms = MailerSendClient(api_key=API)

    main()



def main():
    mail_body = (
        EmailBuilder()
        .from_email(Sender_email, Sender_name)
        .to_many([{"email": Receiver_email, "name": Receiver_email}])
        .subject(Subject)
        .text(Content)
        .build()
    )

    try:
        response = ms.emails.send(mail_body)
        print(response)
    except Exception as e:
        print(e)
        app.email_error(e)

    
if __name__ == "__main__":
    main()
