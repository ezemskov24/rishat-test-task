from django.urls import path

from .views import (
    ItemView,
    ItemsListView,
    OrderListView
)


app_name = 'items'

urlpatterns = [
    path("", ItemsListView.as_view(), name="items_list"),
    path("item/<int:pk>", ItemView.as_view(), name='item_details'),
    path("orders/", OrderListView.as_view(), name="orders_list"),
]
