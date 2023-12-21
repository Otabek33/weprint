# from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from typing import Any, Dict

from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import (ListView, CreateView, )

from apps.transactions.forms import TransactionCreateForm
from apps.transactions.models import Transaction, CashType


class TransactionListView(ListView):
    model = Transaction
    template_name = "transactions/transaction_list.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['transaction_list'] = Transaction.objects.filter(created_by=self.request.user, deleted_status=False)
        return context


transaction_list = TransactionListView.as_view()


class TransactionAddView(CreateView):
    model = Transaction
    form_class = TransactionCreateForm
    template_name = "transactions/transaction_add.html"

    def form_valid(self, form):
        product = form.save(commit=False)
        product.created_by = self.request.user
        product.created_at = datetime.now()
        product.save()
        return redirect("transactions:transaction_list")

    def form_invalid(self, form):
        return HttpResponse(form.errors)


transaction_add = TransactionAddView.as_view()
