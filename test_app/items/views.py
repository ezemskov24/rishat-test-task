from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView

from .models import Item, Order


class ItemView(DetailView):
    model = Item
    template_name = "item-details.html"


class ItemsListView(ListView):
    template_name = "items-list.html"
    context_object_name = "items"
    queryset = Item.objects.filter(archived=False)


class OrderListView(ListView):
    template_name = "order-list.html"
    queryset = (
        Order.objects.select_related("user").prefetch_related("items")
        .exclude(items__archived=True)
    )
