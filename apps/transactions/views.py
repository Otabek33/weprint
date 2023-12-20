# from django.contrib.auth.mixins import LoginRequiredMixin
from typing import Any, Dict
from datetime import datetime, timezone

from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import (ListView, UpdateView, DeleteView)
from apps.products.models import Product as ProductModel
from apps.products.forms import ProductCreateForm, ProductUpdateForm
from apps.transactions.models import Transaction
from utils.helpers import is_ajax


class TransactionListView(ListView):
    model = Transaction
    template_name = "transactions/transaction_list.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['transaction_list'] = Transaction.objects.filter(created_by=self.request.user, deleted_status=False)
        return context


product_list = TransactionListView.as_view()
