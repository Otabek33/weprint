from django.urls import path

from apps.clients.views import (client_add, client_debit_credit, client_delete,
                                client_list, client_transaction, client_update)

app_name = "clients"

urlpatterns = [
    path("", client_list, name="client_list"),
    path("add/", client_add, name="add"),
    path("update/<uuid:pk>", client_update, name="update"),
    path("delete/<uuid:pk>", client_delete, name="delete"),
    path("debit-credit", client_debit_credit, name="debit_credit"),
    path("<uuid:pk>/debit-credit/", client_transaction, name="debit_credit"),
]
