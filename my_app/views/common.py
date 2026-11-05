from django.http import HttpResponse
from rest_framework.request import Request


def hello_name(request: Request, name):
    return HttpResponse(f"<h1>Hello, {name}</h1>")


def hello_world(request: Request):
    return HttpResponse(f"<h1>Hello world!</h1>")
