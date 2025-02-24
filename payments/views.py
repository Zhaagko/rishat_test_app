from django.http.response import HttpResponse


def hello_rishat(request, *args, **kwargs):
    return HttpResponse("<h1>Hello, Rishat!</h1>")
