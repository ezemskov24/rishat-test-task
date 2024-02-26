from django.contrib.auth.models import User
from django.db import models


class Item(models.Model):
    """
    Модель товара.

    name - наименование
    description - описание
    price - цена
    """
    name = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'


class Order(models.Model):
    items = models.ManyToManyField(
        Item, related_name="orders"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)


class Discount(models.Model):
    """
    Модель скидки
    """
    items = models.ManyToManyField(
        Item,
        related_name='item_discount'
    )

