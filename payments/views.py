import json
import stripe
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse
from django.http.response import HttpResponse
from payments import orders
from .models import Item, Order
from .stripe import get_price_data_for_item, get_line_items_for_order


def hello_rishat(*args, **kwargs):
    return HttpResponse("<h1>Hello, Rishat!</h1>")


def get_item_detail(request, item_id: int):
    if request.method != "GET":
        return HttpResponse(status=405)
    item = get_object_or_404(Item, id=item_id)
    return render(request, "item_detail.html", {
        "item": item,
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
    })


def get_order_detail(request, order_id: int):
    if request.method != "GET":
        return HttpResponse(status=405)
    order_detail = orders.get_order_detail(order_id)
    return JsonResponse(order_detail)


def create_order(request, *args, **kwargs):
    if request.method != "POST":
        return HttpResponse(status=405)
    order = orders.create_order()
    return JsonResponse({"order_id": order.id}, status=201)


def add_item_to_order(request, order_id: int, *args, **kwargs):
    if request.method != "POST":
        return HttpResponse(status=405)
    if orders.order_is_finished(order_id):
        return JsonResponse({"error": {"code": "order_is_finished", "msg": "Невозможно добавить товар в завершенный заказ"}}, status=400)
    request_body = json.loads(request.body)
    try:
        item_id = int(request_body["item_id"])
        quantity = int(request_body["quantity"])
    except (KeyError, ValueError):
        return HttpResponse(status=400)
    orders.add_item_to_order(order_id, item_id, quantity)
    return HttpResponse(status=204)


def payment_success(request, *args, **kwargs):
    return HttpResponse("""<h3>Заказ успешно оплачен</h3>""")


def payment_cancel(request, *args, **kwargs):
    return HttpResponse("""<h3>Заказ отменен</h3>""")


def get_redirect_url(request, uri: str) -> str:
    return f"{request.scheme}://{request.get_host()}{uri}"


def get_payment_redirect_urls(request) -> tuple[str, str]:
    payment_success_uri = reverse("payments_payment_success")
    payment_cancel_uri = reverse("payments_payment_cancel")
    success_url = get_redirect_url(request, payment_success_uri)
    cancel_url = get_redirect_url(request, payment_cancel_uri)
    return success_url, cancel_url


def buy_item(request, item_id: int):
    if request.method != "POST":
        return HttpResponse(status=405)
    request_json = json.loads(request.body)
    try:
        quantity = int(request_json["quantity"])
    except (KeyError, ValueError):
        return HttpResponse(status=400)
    item = get_object_or_404(Item, id=item_id)
    success_url, cancel_url = get_payment_redirect_urls(request)
    session_kwargs = dict(
        payment_method_types=["card"],
            line_items=[
                get_price_data_for_item(item, quantity)
            ],
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
    )
    try:
        checkout_session = stripe.checkout.Session.create(
            **session_kwargs
        )
        return JsonResponse({"session_id": checkout_session.id})
    except Exception as e:
        return JsonResponse({"error": str(e), "session_kwargs": session_kwargs}, status=500)


def pay_for_order(request, order_id: int, *args, **kwargs):
    order = get_object_or_404(Order, id=order_id)
    success_url, cancel_url = get_payment_redirect_urls(request)
    session_kwargs = dict(
        payment_method_types=["card"],
            line_items=get_line_items_for_order(order),
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
    )
    try:
        checkout_session = stripe.checkout.Session.create(
            **session_kwargs
        )
        return JsonResponse({"session_id": checkout_session.id})
    except Exception as e:
        return JsonResponse({"error": str(e), "session_kwargs": session_kwargs}, status=500)
