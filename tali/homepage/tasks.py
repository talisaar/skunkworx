from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import smtplib
from time import sleep
from celery import shared_task
from django.conf import settings
import os
from email.mime.text import MIMEText
import smtplib
from email.mime.multipart import MIMEMultipart


@shared_task
def add(x, y):
    return x + y

@shared_task
def add_wait(wait, x, y):
    print(f'waiting {wait} seconds')
    sleep(wait)
    print(f'DONE waiting {wait} seconds')
    return x + y

@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


# @shared_task
# def rename_widget(widget_id, name):
#     w = Widget.objects.get(id=widget_id)
#     w.name = name
#     w.save()


@shared_task
def send_activation_task(sender_email, receiver_email, first_name, activation_link):
    logger = logging.getLogger('logger')
    logger.info(f'sending activation email to {receiver_email}')
    logger.info(f'USER {settings.USER}')
    logger.info(f'SMTP_USER_NAME {os.environ.get("SMTP_USER_NAME")}')
    logger.info(f'SMTP_PASSWORD {os.environ.get("SMTP_PASSWORD")}')


    message = MIMEMultipart("alternative")
    message["Subject"] = "Activate your SkunkW0rX account"
    message["From"] = sender_email
    message["To"] = receiver_email
    body = """
    Hello, {0}.
    Pls click this link to activate your skunkworx account:
    
    {1}

    Love, Tali
    """.format(first_name, activation_link)

    message.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP_SSL(settings.SMTP_ENDPOINT, port=settings.TLS_WRAPPER_PORT)
    server.set_debuglevel(1)
    server.connect(settings.SMTP_ENDPOINT, port=settings.TLS_WRAPPER_PORT)
    server.login(os.environ.get('SMTP_USER_NAME'), os.environ.get('SMTP_PASSWORD'))
    txt = message.as_string()
    server.sendmail(sender_email, receiver_email, txt)
    
    # # Send email ends here
