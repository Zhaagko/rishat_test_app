from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.name}, {self.price}"