from django.urls import path
from django.views.generic import TemplateView

from apps.orders.views import order_list, order_creation, order_detail

app_name = "orders"

urlpatterns = [
    path("", order_list, name="order_list"),
    path("add/", order_creation, name="creation_order_stage_one"),
    path("<uuid:pk>/", order_detail, name="order_detail"),
    path('a/', TemplateView.as_view(template_name='orders/map.html'), name='map'),

]
