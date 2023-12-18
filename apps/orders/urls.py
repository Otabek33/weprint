from django.urls import path
from apps.orders.views import order_list, order_creation, order_detail

app_name = "orders"

urlpatterns = [
    path("", order_list, name="order_list"),
    path("add/", order_creation, name="creation_order_stage_one"),
    path("detail/", order_detail, name="order_detail"),
]
