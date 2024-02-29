from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from items.models import Order


@receiver(m2m_changed, sender=Order.items.through)
def update_total_price(sender, instance, action, **kwargs) -> None:
    """
    Сигнал для обновления суммы заказа при его создании
    и добавлении скидки или налога через админ-панель
    """
    if action:
        total_price_usd, total_price_eur = instance.calculate_total_price()
        instance.total_price_usd = total_price_usd
        instance.total_price_eur = total_price_eur
        instance.save()


@receiver(post_save, sender=Order)
def update_order_total_price(sender, instance, **kwargs) -> None:
    """
    Сигнал для обновления суммы заказа
    при добавлении скидки или налога в созданный заказ
    """
    if instance.discount or instance.tax:
        total_price_usd, total_price_eur = instance.calculate_total_price()
        Order.objects.filter(pk=instance.pk).update(total_price_usd=total_price_usd, total_price_eur=total_price_eur)
