from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from apps.accounts.forms import CompanyCreateForm, CompanyUpdateForm
from apps.accounts.models import ClientAddress, Company


class CompanyDetailView(DetailView):
    model = Company
    template_name = "accounts/company/detail.html"


company_detail = CompanyDetailView.as_view()


class CompanyUpdateView(UpdateView):
    model = Company
    form_class = CompanyUpdateForm
    template_name = "accounts/company/update.html"

    def form_valid(self, form):
        company = form.save(commit=False)
        location = ClientAddress.objects.create(
            name=self.request.POST.get("address"),
            latitude=self.request.POST.get("latitude"),
            longitude=self.request.POST.get("longitude"),
        )
        company.location = location
        company.location = location
        company.save()
        return redirect("accounts:company_list", pk=self.request.user.id)


company_update = CompanyUpdateView.as_view()


class CompanyListView(ListView):
    model = Company
    template_name = "accounts/company/list.html"


company_list = CompanyListView.as_view()


class CompanyCreateView(CreateView):
    model = Company
    form_class = CompanyCreateForm
    template_name = "accounts/company/add.html"

    def form_valid(self, form):
        company = form.save(commit=False)
        location = ClientAddress.objects.create(
            name=self.request.POST.get("address"),
            latitude=self.request.POST.get("latitude"),
            longitude=self.request.POST.get("longitude"),
        )
        company.location = location
        company.location = location
        company.save()
        return redirect("accounts:company_list", pk=self.request.user.id)


company_add = CompanyCreateView.as_view()


class CompanyDeleteView(DeleteView):
    model = Company
    template_name = "accounts/company/delete.html"

    def get_success_url(self):
        return reverse_lazy(
            "accounts:company_list", kwargs={"pk": self.request.user.id}
        )


company_delete = CompanyDeleteView.as_view()
