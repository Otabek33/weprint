from django.urls import path

from .views.account_views import home, log_in, logout, user_detail, user_update
from .views.bank_views import (bank, cash, money_saver_add, money_saver_delete,
                               money_saver_list, money_saver_update)
from .views.company_views import (company_add, company_delete, company_detail,
                                  company_list, company_update)

app_name = "accounts"

urlpatterns = [
    path("logout/", logout, name="logout"),
    path("", log_in, name="login"),
    path("main/", home, name="home"),
    path("<int:pk>/detail/", user_detail, name="user_detail"),
    path("<int:pk>/update/", user_update, name="user_update"),
    path("<int:pk>/cash/", cash, name="cash"),
    path("<int:pk>/bank/", bank, name="bank"),
    path("<int:pk>/company-list/", company_list, name="company_list"),
    path("<int:pk>/company-add/", company_add, name="company_add"),
    path("<uuid:pk>/company-detail/", company_detail, name="company_detail"),
    path("<uuid:pk>/company-update/", company_update, name="company_update"),
    path("<uuid:pk>/company-delete/", company_delete, name="company_delete"),
    path("<int:pk>/money-saver-list/", money_saver_list, name="money_saver_list"),
    path("<int:pk>/money-saver-add/", money_saver_add, name="money_saver_add"),
    path(
        "<uuid:pk>/money-saver-delete/", money_saver_delete, name="money_saver_delete"
    ),
    path(
        "<uuid:pk>/money-saver-update/", money_saver_update, name="money_saver_update"
    ),

]
