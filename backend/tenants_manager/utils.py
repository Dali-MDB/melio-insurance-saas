import smtplib
import dotenv
import os
dotenv.load_dotenv()


def send_email(receiver_email, subject, body):
    sender_email = os.getenv('SMTP_EMAIL')
    text = f'Subject: {subject}\n\n{body}'
    password =  os.getenv('SMTP_PASSWORD')
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(sender_email,password)
    server.sendmail(sender_email,receiver_email,text)