from django.urls import path
from .views import hello_rishat

urlpatterns = [
    path("hello_rishat/", hello_rishat, name="payments_hello_rishat")
]