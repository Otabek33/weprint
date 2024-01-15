from django.urls import path

from .views import webhook

app_name = "bot"

urlpatterns = [
    path("bot/webhook01v/", webhook, name="webhook"),
]
