from django.urls import path
from . import views

urlpatterns = [
    path("hello_rishat", views.hello_rishat, name="payments_hello_rishat"),
    path("item/<int:item_id>", views.get_item_detail, name="payments_get_item_detail"),
    path("buy/<int:item_id>", views.buy_item, name="payments_buy_item"),
    path("success", views.payment_success, name="payments_payment_success"),
    path("cancel", views.payment_cancel, name="payments_payment_cancel"),
    path("order", views.create_order, name="payments_create_order"),
    path("order/<int:order_id>/add_item", views.add_item_to_order, name="payments_add_item_to_order"),
    path("order/<int:order_id>", views.get_order_detail, name="payments_get_order_detail"),
    path("order/<int:order_id>/pay", views.pay_for_order, name="payments_pay_for_order"),
]
