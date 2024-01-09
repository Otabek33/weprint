from django.contrib import auth, messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView

from apps.accounts.models import CustomUser


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


class UserDetailView(DetailView):
    model = CustomUser
    template_name = "accounts/user/detail.html"


user_detail = UserDetailView.as_view()
