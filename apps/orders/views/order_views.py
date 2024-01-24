from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, ListView, TemplateView, CreateView

from apps.accounts.models import ClientAddress
from apps.orders.forms import OrderCreateForm
from apps.orders.models import Order, OrderStatus
from apps.tg.utils import generate_order_number
from django.http import HttpResponse


class OrderListView(ListView):
    model = Order
    template_name = "orders/order_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.order_by("-created_at").exclude(order_status=1)
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
        context["comp_lat"] = order.company.location.latitude
        context["comp_long"] = order.company.location.longitude
        context["client"] = client
        return context

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=self.kwargs["pk"])
        order.order_status = OrderStatus.ACTIVE
        order.save()
        messages.success(request, "Data successfully saved!")
        return redirect("orders:order_list")


order_detail = OrderDetail.as_view()


class OrderCancelView(DetailView):
    model = Order
    template_name = "orders/order_cancel.html"

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=self.kwargs["pk"])
        order.order_status = OrderStatus.CANCELLED
        order.save()
        messages.success(self.request, "Buyurtma bekor qilindi")
        return redirect("orders:order_list")


order_cancel = OrderCancelView.as_view()


class OrderStatusUpdate(TemplateView):
    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=self.kwargs["pk"])
        order.order_status = int(request.POST["status"])
        order.save()
        return redirect("orders:order_list")


order_status = OrderStatusUpdate.as_view()


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderCreateForm
    template_name = "orders/order_add.html"

    def form_valid(self, form):
        order = form.save(commit=False)
        location = ClientAddress.objects.create(
            name=self.request.POST.get("address"),
            latitude=self.request.POST.get("latitude"),
            longitude=self.request.POST.get("longitude"),
        )
        order.location = location
        order.order_number = generate_order_number()
        order.order_status = OrderStatus.ORDERED
        order.save()
        return redirect("accounts:company_list", pk=self.request.user.id)

    def form_invalid(self, form):
        print(form.errors)
        return HttpResponse(form.errors)


order_add = OrderCreateView.as_view()
