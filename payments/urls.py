from django.urls import path
from . import views

urlpatterns = [
    path("hello_rishat/", views.hello_rishat, name="payments_hello_rishat"),
    path("item/<int:item_id>/", views.get_item_detail, name="payments_item_detail"),
    path("buy/<int:item_id>/", views.get_checkout_session, name="payments_item_buy"),
]