from decimal import Decimal
from typing import Tuple

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
    price_usd = models.DecimalField(max_digits=10, decimal_places=2)
    price_eur = models.DecimalField(max_digits=10, decimal_places=2)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'


class Discount(models.Model):
    """
    Модель скидки
    name - название
    amount - размер скидки в %
    """
    name = models.CharField(max_length=100)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Tax(models.Model):
    """
    Модель налога
    name - название
    rate - налоговая ставка
    """
    name = models.CharField(max_length=100)
    rate = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Tax'
        verbose_name_plural = 'Taxes'

    def __str__(self):
        return self.name


class Order(models.Model):
    """
        Модель заказа.

        items - товары в заказе
        user - пользователь, создавший заказ
        total_price - сумма заказа
        created_at - дата создания
        discount - скидка
        tax - налог
        """
    items = models.ManyToManyField(
        Item, related_name="orders"
    )
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    total_price_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_price_eur = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, blank=True)

    def calculate_total_price(self) -> Tuple[float, float]:
        """
        Функция для расчета общей суммы заказа
        """
        total_price_usd = sum(item.price_usd for item in self.items.all())
        total_price_eur = sum(item.price_eur for item in self.items.all())

        if self.discount:
            total_price_usd -= total_price_usd * Decimal(self.discount.amount / 100)
            total_price_eur -= total_price_eur * Decimal(self.discount.amount / 100)

        if self.tax:
            total_price_usd += total_price_usd * Decimal(self.tax.rate / 100)
            total_price_eur += total_price_eur * Decimal(self.tax.rate / 100)

        return total_price_usd, total_price_eur

    def __str__(self):
        return f"Order № {self.pk}"
