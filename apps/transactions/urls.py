from django.urls import path
from django.views.generic import TemplateView

from apps.transactions.views import transaction_list, transaction_add

app_name = "transactions"

urlpatterns = [
    path("", transaction_list, name="transaction_list"),
    path("add/", transaction_add, name="transaction_add"),

]
