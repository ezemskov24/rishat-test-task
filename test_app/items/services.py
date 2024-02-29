import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views import View

from items.models import Item, Order


DOMAIN = "http://127.0.0.1:8000"

stripe.api_key = settings.STRIPE_SECRET_KEY


class GetItemSessionIdView(View):
    """
    Получение id сессии для оплаты товара
    """
    def get(self, request, id) -> JsonResponse:
        item = Item.objects.get(pk=id)
        currency = request.GET.get('currency', 'usd')
        if currency == 'usd':
            price = item.price_usd
        elif currency == 'eur':
            price = item.price_eur
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': currency,
                        'unit_amount': int(price * 100),
                        'product_data': {
                            'name': item.name
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=DOMAIN + '/success/',
            cancel_url=DOMAIN + '/cancel/',
        )
        return JsonResponse({'session_id': session.id})


class GetOrderSessionIdView(View):
    """
    Получение id сессии для оплаты заказа
    """
    def get(self, request, id) -> JsonResponse:
        order = Order.objects.get(pk=id)
        currency = request.GET.get('currency', 'usd')
        if currency == 'usd':
            price = order.total_price_usd
        elif currency == 'eur':
            price = order.total_price_eur
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': currency,
                        'unit_amount': int(price * 100),
                        'product_data': {
                            'name': f"Order № {id}"
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=DOMAIN + '/success/',
            cancel_url=DOMAIN + '/cancel/',
        )
        return JsonResponse({'session_id': session.id})
