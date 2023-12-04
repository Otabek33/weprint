from django.contrib.auth import get_user_model

from apps.clients.models import Client
from apps.orders.models import Order, OrderStatus
from apps.tg.choices import RoleTypeChoices
from apps.tg.models import TelegramUser

User = get_user_model()


def get_or_create_user(message):
    tguser, created = TelegramUser.objects.get_or_create(tg_pk=message.chat.id,
                                                         current_role_in_chat=RoleTypeChoices.USER)
    if created:
        first_name = message.from_user.first_name or ''
        username = message.from_user.username or ''
        last_name = message.from_user.last_name or ''
        client = Client.objects.create(username=username, userId=message.chat.id,
                                       first_name=first_name, last_name=last_name)
        tguser.user = client
        tguser.save()
    return tguser.user, tguser


def get_or_create_order(message):
    order, created = Order.objects.get_or_create(order_number=message.chat.id, page_number=0)
    if created:
        client = Client.objects.get(userId=message.chat.id)
        order.created_by = client
        order.order_number = message.chat.id
        order.save()
    return order.created_by, order
