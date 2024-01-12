
from django.core.management.base import BaseCommand

from apps.tg.chat import bot


class Command(BaseCommand):
    help = 'Telegram-bot'

    def handle(self, *args, **options):
        bot.remove_webhook()
        bot.polling(none_stop=True, skip_pending=True)
