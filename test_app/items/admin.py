from django.contrib import admin

from .models import Item, Order, Discount, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price_usd', 'price_eur']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['pk', 'total_price_usd', 'user', 'created_at']
    ordering = ['created_at']


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount']


@admin.register(Tax)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['name', 'rate']
