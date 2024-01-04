from django.urls import path
from .views import (login_request, logout, home, cash, bank)

app_name = "accounts"

urlpatterns = [
    path("logout/", logout, name="logout"),
    path("", login_request, name="login"),
    path("home/", home, name="home"),
    path("<int:pk>/cash/", cash, name="cash"),
    path("<int:pk>/bank/", bank, name="bank"),
]
