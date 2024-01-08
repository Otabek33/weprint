from datetime import datetime, timezone

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from apps.accounts.forms import MoneySaverCreateForm
from apps.accounts.models import CustomUser, CashType, MoneySaver
from apps.products.forms import PrintBindingTypesCreateForm
from apps.products.models import PrintBindingTypes
from apps.transactions.models import Transaction


class BindingTypesListView(ListView):
    model = PrintBindingTypes
    template_name = "products/binding_types/binding_type_list.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user = get_object_or_404(CustomUser, pk=self.kwargs["pk"])
    #
    #     context["binding_types_list"] = PrintBindingTypes.objects.filter(deleted_status=False, cash_type=bank,
    #                                                               company=user.company)
    #     return context


binding_type_list = BindingTypesListView.as_view()


class BindingTypeCreateView(CreateView):
    model = PrintBindingTypes
    form_class = PrintBindingTypesCreateForm
    template_name = "products/binding_types/binding_type_add.html"

    def form_valid(self, form):
        user = self.request.user
        binding_type = form.save(commit=False)
        binding_type.company = user.company
        binding_type.created_by = user
        binding_type.save()
        return redirect("products:binding_type_list", pk=self.request.user.id)


binding_type_add = BindingTypeCreateView.as_view()
