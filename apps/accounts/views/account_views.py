from django.contrib import auth
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView, UpdateView
from apps.accounts.forms import CustomUserUpdateForm
from apps.accounts.models import CustomUser


class UserLogIn(LoginView):
    template_name = "accounts/login.html"

    def get_success_url(self):
        return reverse_lazy("accounts:home")


log_in = UserLogIn.as_view()


def logout(request):
    auth.logout(request)
    return redirect("accounts:login")


class Dashboard(TemplateView):
    model = CustomUser
    template_name = "base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = get_object_or_404(CustomUser, id=self.request.user.id)
        return context


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
        return reverse_lazy("accounts:user_detail", kwargs={"pk": self.request.user.id})


user_update = UserUpdateView.as_view()
