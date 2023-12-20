from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (ListView, DetailView, DeleteView)
from apps.orders.models import Order, OrderStatus
from django.contrib import messages


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


class OrderDetail(DetailView):
    model = Order
    template_name = "orders/order_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = get_object_or_404(Order, pk=self.kwargs["pk"])
        client = order.created_by
        context["order"] = order
        context["client"] = client
        return context

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=self.kwargs["pk"])
        order.order_status = OrderStatus.ACTIVE
        order.save()
        messages.success(request, 'Data successfully saved!')
        return redirect("orders:order_list")


order_detail = OrderDetail.as_view()


class OrderCancelView(DetailView):
    model = Order
    template_name = "orders/order_cancel.html"

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=self.kwargs["pk"])
        order.order_status = OrderStatus.CANCELLED
        order.save()
        messages.success(self.request, 'Buyurtma bekor qilindi')
        return redirect("orders:order_list")


order_cancel = OrderCancelView.as_view()
