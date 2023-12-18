from django.views.generic import (ListView, CreateView, TemplateView)
from apps.orders.forms import OrderCreateForm
from apps.orders.models import Order


class OrderListView(ListView):
    model = Order
    template_name = "orders/order_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.order_by(
            "-created_at").exclude(order_status=1)
        context["order_list"] = orders
        return context


order_list = OrderListView.as_view()


class OrderDetail(TemplateView):
    model = Order
    template_name = "orders/order_detail.html"


order_detail = OrderDetail.as_view()


class OrderCreationView(CreateView):
    model = Order
    form_class = OrderCreateForm
    template_name = "orders/order_add.html"


order_creation = OrderCreationView.as_view()
