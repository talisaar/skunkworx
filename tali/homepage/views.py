from django.shortcuts import render
import logging
import os.path
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.conf import settings
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

from email.mime.text import MIMEText
import smtplib, ssl
from email.mime.multipart import MIMEMultipart

# Create your views here.

from django.template import RequestContext
from django.http import HttpResponse
from django.template import loader

# def index(request):
#     return HttpResponse("Hello, world. You're at the homepage index.")


def index(request):
    logger = logging.getLogger('poop')
    logger.warning(f'request is: {request}')

    welcome = "My welcome text"
    request_context = RequestContext(request)
    request_context.push({"welcome": welcome})

    return render(request, "homepage/index.html", request_context.__dict__)

from rest_framework import viewsets
from homepage.models import myUser
from homepage.serializers import UserSerializer
from uuid import uuid4


class UserViewSet(viewsets.ModelViewSet):
    queryset = myUser.objects.all()
    serializer_class = UserSerializer

    # overrider the default create method in order to use the builtin 'create_user' function that
    # comes with builtin User. This one hashes the password by itself.
    def create(self, request):
        logger = logging.getLogger('hello')
        logger.warning(request.data)
        first_name = request.data["firstname"]
        last_name = request.data["lastname"]
        email = request.data["email"]
        password = request.data["password"]
        username = uuid4().hex[:30] # Makes a random username
        new_user = myUser.objects.create_user(
            username=username, 
            email=email, 
            password=password,
            first_name=first_name,
            last_name=last_name)
        self.send_activation_email(new_user)
        return HttpResponse("User Created!")
    
    def send_activation_email(self, new_user):
        sender_email = 'tali@skunkworx.co'
        receiver_email = new_user.email

        logger = logging.getLogger('activation_email')
        logger.warning(f'sending email to {receiver_email}')

        message = MIMEMultipart("alternative")
        message["Subject"] = "Activate your SkunkW0rX account"
        message["From"] = sender_email
        message["To"] = receiver_email
        name = new_user.first_name
        body = """
        Hello, {0}.
        Pls click this link to activate your skunkworx account:
        
        # # # Here will be link # # #

        Love, Tali
        """.format(name)

        message.attach(MIMEText(body, 'plain'))


        # Create a secure SSL context
        context = ssl.create_default_context()
        # send the email with SES smtp

        # server = smtplib.SMTP(SMTP_ENDPOINT, port=STARTTLS_PORT)
        server = smtplib.SMTP_SSL(settings.SMTP_ENDPOINT, port=settings.TLS_WRAPPER_PORT)

        server.set_debuglevel(1)

        # server.connect(SMTP_ENDPOINT, port=STARTTLS_PORT)
        server.connect(settings.SMTP_ENDPOINT, port=settings.TLS_WRAPPER_PORT)

        # server.starttls() ### ONLY NEED THESE STEPS IF NOT USING THE SMTP_SSL OPTION
        # server.helo()
        # server.ehlo()

        server.login(settings.SMTP_USER_NAME, settings.SMTP_PASSWORD)
        # TODO: Send email here
        txt = message.as_string()
        server.sendmail(sender_email, receiver_email, txt)


            # Send email ends here


