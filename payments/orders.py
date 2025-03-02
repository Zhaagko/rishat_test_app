from typing import TypedDict
from django.db.models import F
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Order, OrderItem


class ItemDetail(TypedDict):
    name: str
    quantity: int


class OrderDetail(TypedDict):
    items: list[ItemDetail]
    created_at: str
    finished_at: str | None


def create_order() -> Order:
    return Order.objects.create(created_at=timezone.now())


def order_is_finished(order_id: int) -> bool:
    order = get_object_or_404(Order.objects.only("finished_at"), id=order_id)
    return order.finished_at is not None


def add_item_to_order(order_id: int, item_id: int, quantity: int):
    if OrderItem.objects.filter(order_id=order_id, item_id=item_id).exists():
        OrderItem.objects.filter(order_id=order_id, item_id=item_id).update(quantity=F("quantity") + quantity)
        return
    OrderItem.objects.create(item_id=item_id, order_id=order_id, quantity=quantity)


def get_order_detail(order_id: int) -> OrderDetail:
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order_id=order_id).select_related("item")
    item_details = [ItemDetail(name=oi.item.name, quantity=oi.quantity) for oi in order_items]
    return OrderDetail(
        items=item_details,
        created_at=order.created_at,
        finished_at=order.finished_at
    )