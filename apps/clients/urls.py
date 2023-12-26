from django.urls import path
from apps.clients.views import (client_list, client_update, client_delete, client_add,client_debit_credit)

app_name = "clients"

urlpatterns = [

    path("", client_list, name="client_list"),
    path("add/", client_add, name="add"),
    path("update/<uuid:pk>", client_update, name="update"),
    path("delete/<uuid:pk>", client_delete, name="delete"),
    path('debit-credit', client_debit_credit, name='debit_credit'),

]
