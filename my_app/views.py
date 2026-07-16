from django.http import HttpResponse

def hello_name(request, name):
    return HttpResponse(f"<h1>Hello, {name}</h1>")

def hello_world(request):
    return HttpResponse(f"<h1>Hello world!</h1>")
