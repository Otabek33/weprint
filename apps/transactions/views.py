# from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from typing import Any, Dict

from django.db.models.signals import post_save
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import (ListView, CreateView, )

from apps.transactions.forms import TransactionCreateForm
from apps.transactions.models import Transaction, CashType
from apps.transactions.signals import updating_company_balance
from apps.transactions.utils import payment_order_generation, company_balance_generation, disconnect_signal, \
    reconnect_signal, get_company


class TransactionListView(ListView):
    model = Transaction
    template_name = "transactions/transaction_list.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['transaction_list'] = Transaction.objects.filter(deleted_status=False)
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
        transaction.save()
        disconnect_signal(post_save, updating_company_balance, Transaction)
        company_balance_generation(transaction, self.request.user)
        reconnect_signal(post_save, updating_company_balance, Transaction)
        return redirect("transactions:transaction_list")

    def form_invalid(self, form):
        return HttpResponse(form.errors)


transaction_add = TransactionAddView.as_view()
