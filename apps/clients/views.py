# from django.contrib.auth.mixins import LoginRequiredMixin
from typing import Any, Dict
from datetime import datetime, timezone
from django.forms.models import BaseModelForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.generic import (CreateView, UpdateView, DeleteView, ListView)
from apps.clients.forms import ClientCreateForm, ClientUpdateForm
from apps.clients.models import Client
from utils.helpers import is_ajax


class ClientListView(CreateView):
    model = Client
    form_class = ClientCreateForm
    template_name = "clients/client_list.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['client_list'] = Client.objects.filter(deleted_status=False)
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        client = form.save(commit=False)
        client.created_by = self.request.user
        client.save()
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_invalid(form)


client_list = ClientListView.as_view()


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientUpdateForm
    template_name = "clients/client_add.html"

    def form_valid(self, form):
        product = form.save(commit=False)
        product.updated_by = self.request.user
        product.updated_at = datetime.now()
        product.save()
        return redirect("clients:client_list")

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


client_update = ClientUpdateView.as_view()


class ClientDeleteView(DeleteView):
    model = Client
    success_url = "/"
    template_name = "clients/client_delete.html"


client_delete = ClientDeleteView.as_view()


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientCreateForm
    template_name = "clients/client_add.html"

    def form_valid(self, form):
        print("ishladi form valid")
        client = form.save(commit=False)
        client.save()
        return redirect("clients:client_list")

    def form_invalid(self, form):
        print(form.errors)
        return HttpResponse(form.errors)


client_add = ClientCreateView.as_view()


class ClientDebitCredit(ListView):
    model = Client
    template_name = "debit_credit/client_debit_credit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client_list"] = Client.objects.filter(deleted_status=False).order_by(
            "created_at")

        return context


client_debit_credit = ClientDebitCredit.as_view()
