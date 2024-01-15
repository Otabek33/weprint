from django.urls import path

from apps.orders.views.order_views import (order_cancel, order_detail,
                                           order_list, order_status)

app_name = "orders"

urlpatterns = [
    path("", order_list, name="order_list"),
    path("<uuid:pk>/", order_detail, name="order_detail"),
    path("<uuid:pk>/cancel-order/", order_cancel, name="order_cancel"),
    path("<uuid:pk>/order-update-status/", order_status, name="status_update"),
]
