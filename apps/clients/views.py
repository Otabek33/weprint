# from django.contrib.auth.mixins import LoginRequiredMixin
from typing import Any, Dict
from datetime import datetime, timezone
from django.forms.models import BaseModelForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.generic import (CreateView, UpdateView, DeleteView)
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
    template_name = "clients/client_update.html"

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

    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            pk = request.POST.get("id")
            client = Client.objects.get(uuid=pk)
            client.deleted_status = True
            client.updated_at = datetime.now(tz=timezone.utc)
            client.updated_by = self.request.user
            client.save()
            # ProjectSerializer(client, many=False).data

            return JsonResponse(
                {"success": True, "data": None}
            )
        return JsonResponse({"success": False, "data": None})


client_delete = ClientDeleteView.as_view()
