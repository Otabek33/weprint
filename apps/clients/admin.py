from django.contrib import admin

from apps.clients.models import Client

# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    model = Client
    list_display = [
        "uuid",
        "userId",
        "username",
        "first_name",
        "last_name",
        "phone",
    ]
