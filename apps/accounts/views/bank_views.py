from datetime import datetime, timezone

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from apps.accounts.forms import MoneySaverCreateForm
from apps.accounts.models import CustomUser, CashType, MoneySaver
from apps.transactions.models import Transaction


class CashListView(ListView):
    model = Transaction
    template_name = "accounts/cash.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(CustomUser, pk=self.kwargs["pk"])
        cash = MoneySaver.objects.get(deleted_status=False, cashType=CashType.CASH, company=user.company)
        context["cash"] = cash
        context["transactions_list"] = Transaction.objects.filter(deleted_status=False, cash_type=cash,
                                                                  company=user.company)
        return context


cash = CashListView.as_view()


class BankListView(ListView):
    model = Transaction
    template_name = "accounts/bank.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(CustomUser, pk=self.kwargs["pk"])
        bank = MoneySaver.objects.get(cashType=CashType.BANK, company=user.company)
        context["bank"] = bank
        context["transactions_list"] = Transaction.objects.filter(deleted_status=False, cash_type=bank,
                                                                  company=user.company)
        return context


bank = BankListView.as_view()


class MoneySaverListView(ListView):
    model = MoneySaver
    template_name = "accounts/banks/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(CustomUser, pk=self.kwargs["pk"])
        bank_list = MoneySaver.objects.filter(deleted_status=False, company=user.company)
        context["bank_list"] = bank_list
        return context


money_saver_list = MoneySaverListView.as_view()


class MoneySaverCreateView(CreateView):
    model = MoneySaver
    form_class = MoneySaverCreateForm
    template_name = "accounts/banks/add.html"

    def form_valid(self, form):
        user = self.request.user

        bank = form.save(commit=False)
        bank.company = user.company
        bank.save()
        return redirect("accounts:money_saver_list", pk=self.request.user.id)


money_saver_add = MoneySaverCreateView.as_view()


class MoneySaverDelete(DeleteView):
    model = MoneySaver
    template_name = "accounts/banks/delete.html"

    def post(self, request, *args, **kwargs):
        bank = get_object_or_404(MoneySaver, pk=self.kwargs["pk"])
        bank.deleted_status = True
        bank.updated_at = datetime.now(tz=timezone.utc)
        bank.updated_by = self.request.user
        bank.save()
        return redirect("accounts:money_saver_list", pk=self.request.user.id)


money_saver_delete = MoneySaverDelete.as_view()


class MoneySaverUpdateView(UpdateView):
    model = MoneySaver
    form_class = MoneySaverCreateForm
    template_name = "accounts/banks/update.html"

    def get_success_url(self):
        return reverse_lazy('accounts:money_saver_list', kwargs={'pk': self.request.user.id})


money_saver_update = MoneySaverUpdateView.as_view()
