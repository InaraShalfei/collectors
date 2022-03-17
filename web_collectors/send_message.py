import os
import smtplib
from email.mime.text import MIMEText


def send_message(user, collection):
    msg = MIMEText(
        f'У автора {collection.owner} появилась новая коллекция {collection.name}!')
    msg['Subject'] = 'Новая коллекция!'
    msg['From'] = os.getenv('SMTP_LOGIN')
    msg['To'] = user.email
    server = smtplib.SMTP(os.getenv('SMTP_HOST'), os.getenv('SMTP_PORT'))
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(msg['From'], os.getenv('SMTP_PASSWORD'))
    server.sendmail(msg['From'], [msg['To']], msg.as_string())
    server.quit()
