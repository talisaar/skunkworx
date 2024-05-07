from django.shortcuts import render
import logging
import os.path
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
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
        return HttpResponse("User Created!")
