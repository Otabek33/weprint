# from django.contrib.auth.mixins import LoginRequiredMixin
from typing import Any, Dict
from django.views.generic import (ListView, CreateView, )

from apps.transactions.forms import TransactionCreateForm
from apps.transactions.models import Transaction


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


transaction_add = TransactionAddView.as_view()
