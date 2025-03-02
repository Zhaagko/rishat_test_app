from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"ID: {self.id}, Name: {self.name}, Price: {self.price}"


class OrderItem(models.Model):
    item = models.ForeignKey("payments.Item", on_delete=models.PROTECT)
    order = models.ForeignKey("payments.Order", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"ID: {self.id}, Order id: {self.order_id}, Item id: {self.item_id}, Quantity: {self.quantity}"


class Order(models.Model):
    items = models.ManyToManyField("payments.Item", through="payments.OrderItem")
    created_at = models.DateTimeField()
    finished_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"ID: {self.id}, Finished: {self.finished_at is not None}"
