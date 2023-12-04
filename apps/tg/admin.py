from django.contrib import admin

from apps.tg.models import Chat, Message, TelegramUser, Theme

# Register your models here.
admin.site.register([Theme, Chat, TelegramUser, Message])
