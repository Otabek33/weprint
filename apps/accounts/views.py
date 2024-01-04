from django.contrib import auth, messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView

from apps.accounts.models import CustomUser, MoneySaver, CashType
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
