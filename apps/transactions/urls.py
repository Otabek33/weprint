from django.urls import path
from django.views.generic import TemplateView

from apps.transactions.views import transaction_list, transaction_add, transaction_client_choose

app_name = "transactions"

urlpatterns = [
    path("", transaction_list, name="transaction_list"),
    path("add/", transaction_add, name="transaction_add"),
    path("client-choose/", transaction_client_choose, name="transaction_client_choose"),

]
