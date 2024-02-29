from django.urls import path

from .views import (
    ItemView,
    SuccessView,
    CancelView,
    ItemsListView,
    OrderListView,
    OrderCreateView,
    OrderDetailView,
)

from .services import GetItemSessionIdView, GetOrderSessionIdView


app_name = 'items'

urlpatterns = [
    path("", ItemsListView.as_view(), name="items_list"),
    path("item/<int:pk>/", ItemView.as_view(), name='item_details'),
    path("buy/<int:id>/", GetItemSessionIdView.as_view(), name="get_item_session_id"),
    path("success/", SuccessView.as_view(), name='item_details'),
    path("cancel/", CancelView.as_view(), name="orders_list"),
    path("orders/", OrderListView.as_view(), name="orders_list"),
    path("orders/<int:pk>", OrderDetailView.as_view(), name="order_details"),
    path('orders/create/', OrderCreateView.as_view(), name='order_create'),
    path("orders/buy/<int:id>/", GetOrderSessionIdView.as_view(), name="get_order_session_id"),
]
