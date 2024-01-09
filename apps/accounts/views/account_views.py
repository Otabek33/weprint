from django.contrib import auth, messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DetailView, UpdateView

from apps.accounts.forms import CustomUserUpdateForm
from apps.accounts.models import CustomUser


# Create your views here.
def login_request(request):
    if request.method == "POST":
        user = auth.authenticate(
            username=request.POST.get("username"), password=request.POST.get("password")
        )
        print("ishladi")
        print("ishladi")
        print(user.id)
        print(user.username)
        print(user.password)
        if user is not None:
            # auth.login(request, user)
            return redirect("accounts:home")
        else:
            messages.error(request, "Неправильное имя пользователя или пароль")
            return redirect("accounts:login")

    return render(request, "accounts/login.html")


def logout(request):
    auth.logout(request)
    return redirect("accounts:login")


class Dashboard(View):
    model = CustomUser
    template_name = "base.html"


home = Dashboard.as_view()


class UserDetailView(DetailView):
    model = CustomUser
    template_name = "accounts/user/detail.html"


user_detail = UserDetailView.as_view()


class UserUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = "accounts/user/update.html"

    def get_success_url(self):
        return reverse_lazy('accounts:user_detail', kwargs={'pk': self.request.user.id})


user_update = UserUpdateView.as_view()
