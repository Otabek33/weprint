from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, UpdateView

from apps.accounts.forms import CompanyUpdateForm
from apps.accounts.models import Company, CustomUser


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