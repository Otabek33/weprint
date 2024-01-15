# from django.contrib.auth.mixins import LoginRequiredMixin
import decimal
from datetime import datetime
from typing import Any, Dict

from django.db.models import Case, DecimalField, F, Q, Sum, When
from django.db.models.signals import post_save
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, ListView

from apps.accounts.models import CashType, MoneySaver
from apps.clients.models import Client
from apps.orders.models import Order, OrderStatus
from apps.transactions.forms import TransactionCreateForm
from apps.transactions.models import Transaction
from apps.transactions.serializers import OrderSerializer
from apps.transactions.signals import (transaction_deleted_signal,
                                       updating_company_balance)
from apps.transactions.utils import (disconnect_signal, get_company,
                                     payment_order_generation,
                                     reconnect_signal)
from utils.helpers import is_ajax


class TransactionListView(ListView):
    model = Transaction
    template_name = "transactions/transaction_list.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["transaction_list"] = Transaction.objects.filter(deleted_status=False)
        context["company"] = get_company(self.request.user)

        context["money"] = MoneySaver.objects.aggregate(
            cash=Sum(
                Case(
                    When(cashType=CashType.CASH, then=F("balance")),
                    default=0,
                    output_field=DecimalField(),
                )
            ),
            bank=Sum(
                Case(
                    When(cashType=CashType.BANK, then=F("balance")),
                    default=0,
                    output_field=DecimalField(),
                )
            ),
        )
        return context


transaction_list = TransactionListView.as_view()


class TransactionAddView(CreateView):
    model = Transaction
    form_class = TransactionCreateForm
    template_name = "transactions/transaction_add.html"

    def form_valid(self, form):
        transaction = form.save(commit=False)
        transaction.created_by = self.request.user
        transaction.created_at = datetime.now()
        transaction.company = get_company(self.request.user)
        transaction.payment_order = payment_order_generation()
        price = decimal.Decimal(self.request.POST.get("price"))
        transaction.balance = price
        order = self.request.POST.get("order")
        if order:
            transaction.order = Order.objects.get(uuid=order)
        transaction.save()

        return redirect("transactions:transaction_list")

    def form_invalid(self, form):
        return HttpResponse(form.errors)


transaction_add = TransactionAddView.as_view()


class TranslateClientChoose(DetailView):
    model = Client

    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            pk = request.POST.get("selectedOption")
            client = self.model.objects.get(uuid=pk)
            order_list = Order.objects.filter(
                Q(created_by=client)
                & ~Q(order_status=OrderStatus.CANCELLED)
                & ~Q(order_status=OrderStatus.CREATION)
            )
            serializer = OrderSerializer(order_list, many=True)
            serialized_data = serializer.data
            return JsonResponse({"success": True, "data": serialized_data}, safe=False)
        return JsonResponse({"success": False, "data": None})


transaction_client_choose = TranslateClientChoose.as_view()


class TranslatePrice(DetailView):
    model = Order

    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            pk = request.POST.get("selectedValue")
            order = self.model.objects.get(uuid=pk)
            return JsonResponse({"success": True, "data": order.price}, safe=False)
        return JsonResponse({"success": False, "data": None})


transaction_order_price = TranslatePrice.as_view()


class TransactionDetailView(DetailView):
    model = Transaction
    template_name = "transactions/transaction_detail.html"

    def post(self, request, *args, **kwargs):
        disconnect_signal(post_save, updating_company_balance, sender=Transaction)
        transaction = get_object_or_404(Transaction, pk=self.kwargs["pk"])
        transaction.deleted_status = True
        transaction.save()
        reconnect_signal(post_save, updating_company_balance, sender=Transaction)
        transaction_deleted_signal.send(sender=Transaction, instance=transaction)
        return redirect("transactions:transaction_list")


transaction_detail = TransactionDetailView.as_view()
