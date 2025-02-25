import stripe
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse
from django.http.response import HttpResponse
from .models import Item


def hello_rishat(*args, **kwargs):
    return HttpResponse("<h1>Hello, Rishat!</h1>")


def get_item_detail(request, item_id: int):
    item = get_object_or_404(Item, id=item_id)
    return render(request, "item_detail.html", {
        "item": item,
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
    })


def get_checkout_session(request, item_id: int):
    item = get_object_or_404(Item, id=item_id)
    item_detail_uri = reverse("payments_item_detail", args=(item_id,))
    redirect_url = f"{request.scheme}://{request.get_host()}{item_detail_uri}"
    session_kwargs = dict(
        payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": settings.STRIPE_DEFAULT_CURRENCY,
                        "product_data": {
                            "name": item.name,
                        },
                        "unit_amount": int(item.price * 100),
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=redirect_url,
            cancel_url=redirect_url,
    )
    try:
        checkout_session = stripe.checkout.Session.create(
            **session_kwargs
        )
        return JsonResponse({"session_id": checkout_session.id})
    except Exception as e:
        return JsonResponse({"error": str(e), "session_kwargs": session_kwargs}, status=500)
