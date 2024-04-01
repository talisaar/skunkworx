from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import loader

# def index(request):
#     return HttpResponse("Hello, world. You're at the homepage index.")


def index(request):
    welcome = "My welcome text"
    context = {"welcome": welcome}

    return render(request, "homepage/index.html", context)
