from datetime import datetime

from django.contrib import auth, messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView

from apps.accounts.forms import CompanyUpdateForm, MoneySaverCreateForm
from apps.accounts.models import CustomUser, MoneySaver, CashType, Company
from apps.transactions.models import Transaction


# Create your views here.
def login_request(request):
    if request.method == "POST":
        user = auth.authenticate(
            username=request.POST.get("username"), password=request.POST.get("password")
        )
        if user is not None:
            # auth.login(request, user)
            return redirect("accounts:home")
        else:
            messages.error(request, "Неправильное имя пользователя или пароль")
            return redirect("accounts:login")

    if request.user.is_authenticated:
        return redirect("accounts:home")

    return render(request, "accounts/login.html")


def logout(request):
    auth.logout(request)
    return redirect("accounts:login")


class Dashboard(TemplateView):
    template_name = "base.html"


home = Dashboard.as_view()


class CashListView(ListView):
    model = Transaction
    template_name = "accounts/cash.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(CustomUser, pk=self.kwargs["pk"])
        cash = MoneySaver.objects.get(cashType=CashType.CASH, company=user.company)
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


class CompanyDetailView(DetailView):
    model = Company
    template_name = "accounts/company/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(CustomUser, pk=self.kwargs["pk"])
        context["company"] = user.company
        return context


company_detail = CompanyDetailView.as_view()


class CompanyUpdateView(UpdateView):
    model = Company
    form_class = CompanyUpdateForm
    template_name = "accounts/company/update.html"

    def post(self, request, *args, **kwargs):
        form = CompanyUpdateForm(request.POST, instance=request.user.company)
        if form.is_valid():
            form.save()
            return redirect("accounts:company", pk=request.user.id)
        else:
            print(form.errors)
            return redirect("accounts:company", pk=request.user.id)


company_update = CompanyUpdateView.as_view()


class MoneySaverListView(ListView):
    model = MoneySaver
    template_name = "accounts/banks/money_saver_list.html"


money_saver_list = MoneySaverListView.as_view()


class MoneySaverAddList(CreateView):
    model = MoneySaver
    form_class = MoneySaverCreateForm
    template_name = "accounts/banks/money_saver_add.html"

    def form_valid(self, form):
        user = self.request.user

        bank = form.save(commit=False)
        bank.company = user.company
        bank.save()
        return redirect("accounts:money_saver_list", pk=self.request.user.id)


money_saver_add = MoneySaverAddList.as_view()
