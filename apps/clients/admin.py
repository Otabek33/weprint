from django.contrib import admin

# Register your models here.

from apps.clients.models import (Client)


# Register your models here.


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


admin.site.register(Client, ClientAdmin)