from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, UpdateView, ListView

from apps.accounts.forms import CompanyUpdateForm
from apps.accounts.models import Company, CustomUser, ClientAddress


class CompanyDetailView(DetailView):
    model = Company
    template_name = "accounts/company/detail.html"


company_detail = CompanyDetailView.as_view()


class CompanyUpdateView(UpdateView):
    model = Company
    form_class = CompanyUpdateForm
    template_name = "accounts/company/update.html"

    # def post(self, request, *args, **kwargs):
    #     form = CompanyUpdateForm(request.POST, instance=request.user.company)
    #     if form.is_valid():
    #
    #         form.location = location
    #         form.save()
    #
    #         return redirect("accounts:company", pk=request.user.id)
    #     else:
    #         print(form.errors)
    #         return redirect("accounts:company", pk=request.user.id)

    def form_valid(self, form):
        user = self.request.user
        company = form.save(commit=False)
        location = ClientAddress.objects.create(name=self.request.POST.get('address'),
                                                latitude=self.request.POST.get('latitude'),
                                                longitude=self.request.POST.get('longitude'))
        company.location = location
        company.location = location
        company.save()
        return redirect("accounts:company_list", pk=self.request.user.id)


company_update = CompanyUpdateView.as_view()


class CompanyListView(ListView):
    model = Company
    template_name = "accounts/company/list.html"


company_list = CompanyListView.as_view()
