from django.contrib import admin

from apps.tg.models import  TelegramUser

# Register your models here.
admin.site.register([TelegramUser])
