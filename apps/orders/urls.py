from django.urls import path
from django.views.generic import TemplateView

from apps.orders.views import order_list, order_detail, order_cancel

app_name = "orders"

urlpatterns = [
    path("", order_list, name="order_list"),
    path("<uuid:pk>/", order_detail, name="order_detail"),
    path('<uuid:pk>/cancel-order/', order_cancel, name='order_cancel'),

]
