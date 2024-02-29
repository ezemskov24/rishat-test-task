from typing import Any, Dict

from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView, CreateView

from .forms import OrderForm
from .models import Item, Order, Discount, Tax


class ItemsListView(ListView):
    """
    View страницы со списком товаров
    """
    template_name = 'items-list.html'
    context_object_name = 'items'
    queryset = Item.objects.filter(archived=False)


class ItemView(DetailView):
    """
    View детальной страницы товара
    """
    model = Item
    template_name = 'item-details.html'

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """
        Метод для получения контекстных данных, передаваемых в шаблон.
        """
        context = super().get_context_data(**kwargs)
        item = self.get_object()
        context['stripe_public_key'] = settings.STRIPE_PUBLIC_KEY
        context['item_id'] = item.pk
        return context


class SuccessView(TemplateView):
    """
    View страницы успешной оплаты
    """
    template_name = "success.html"


class CancelView(TemplateView):
    """
    View страницы отмены оплаты
    """
    template_name = "cancel.html"


class OrderListView(ListView):
    """
    View страницы списка заказов
    """
    template_name = 'order-list.html'
    queryset = (
        Order.objects.select_related('user').prefetch_related('items')
        .exclude(items__archived=True)
    )


class OrderCreateView(CreateView):
    """
    View страницы создания заказа
    """
    model = Order
    form_class = OrderForm
    template_name = 'order-form.html'
    success_url = reverse_lazy("items:orders_list")

    def form_valid(self, form):
        discount = Discount.objects.first()
        tax = Tax.objects.first()

        form.instance.discount = discount
        form.instance.tax = tax

        return super().form_valid(form)


class OrderDetailView(DetailView):
    """
    View детальной страницы заказа
    """
    model = Order
    template_name = 'order-details.html'

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """
        Метод для получения контекстных данных, передаваемых в шаблон.
        """
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        context['stripe_public_key'] = settings.STRIPE_PUBLIC_KEY
        context['order_id'] = order.pk
        return context
