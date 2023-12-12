from django.urls import path

from .views import webhook

app_name = "orders"

urlpatterns = [
    path('bot/webhook01v/', webhook, name='webhook'),
]
