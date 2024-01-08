from django.urls import path
from .views import (login_request, logout, home, cash, bank, company_detail,company_update,money_saver_list,money_saver_add)

app_name = "accounts"

urlpatterns = [
    path("logout/", logout, name="logout"),
    path("", login_request, name="login"),
    path("home/", home, name="home"),
    path("<int:pk>/cash/", cash, name="cash"),
    path("<int:pk>/bank/", bank, name="bank"),
    path("<int:pk>/company/", company_detail, name="company"),
    path("<int:pk>/company-update/", company_update, name="company_update"),
    path("<int:pk>/money-saver-list/", money_saver_list, name="money_saver_list"),
    path("<int:pk>/money-saver-add/", money_saver_add, name="money_saver_add"),

]
