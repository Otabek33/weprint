import os

import django
from django.core.checks import messages
from django.core.management.base import BaseCommand

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "petb.settings")
django.setup()
from apps.tg.chat import bot


class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        bot.remove_webhook()
        bot.polling(none_stop=True,skip_pending=True)
