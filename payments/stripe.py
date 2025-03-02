from django.conf import settings
from .models import Item, Order, OrderItem


def get_item_price(item: Item) -> int:
    return int(item.price * 100)


def get_price_data_for_item(item: Item, quantity: int = 1) -> dict:
    return {
                    "price_data": {
                        "currency": settings.STRIPE_DEFAULT_CURRENCY,
                        "product_data": {
                            "name": item.name,
                        },
                        "unit_amount": get_item_price(item),
                    },
                    "quantity": quantity,
                }


def get_line_items_for_order(order: Order) -> list[dict]:
    order_items = OrderItem.objects.select_related("item").only("item", "quantity").filter(order_id=order.id)
    return [get_price_data_for_item(o.item, o.quantity) for o in order_items]
