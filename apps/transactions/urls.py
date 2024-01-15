from django.urls import path
from django.views.generic import TemplateView

from apps.transactions.views import (transaction_add,
                                     transaction_client_choose,
                                     transaction_detail, transaction_list,
                                     transaction_order_price)

app_name = "transactions"

urlpatterns = [
    path("", transaction_list, name="transaction_list"),
    path("add/", transaction_add, name="transaction_add"),
    path("client-choose/", transaction_client_choose, name="transaction_client_choose"),
    path("price/", transaction_order_price, name="transaction_order_price"),
    # path("delete/", transaction_delete, name="transaction_delete"),
    path("<int:pk>/detail/", transaction_detail, name="transaction_detail"),
]
