from django.contrib.auth import get_user_model

from apps.clients.models import Client
from apps.orders.models import Order, OrderStatus
from apps.products.models import Product
from apps.tg.choices import RoleTypeChoices
from apps.tg.models import TelegramUser
import uuid
from datetime import datetime

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
    client = Client.objects.get(userId=message.chat.id)
    order, created = Order.objects.get_or_create(tg_pk=message.chat.id, created_by=client,
                                                 order_status=OrderStatus.CREATION, page_number=0)
    if created:
        order.created_by = client
        order.order_number = generate_order_number()
        order.save()
    return order.created_by, order


def generate_order_number():
    # Static prefix for the order number
    prefix = "OB"

    # Current timestamp to include in the order number
    timestamp = datetime.now().strftime("%d%m%H%M")

    # Generate a random UUID and extract the last portion to add some uniqueness
    unique_id = str(uuid.uuid4())[-2:]

    # Combine the elements to create the order number
    order_number = f"{prefix}-{timestamp}-{unique_id}"

    return order_number


def generation_price(order):
    product = Product.productListByUser.get_product(order.printColor, order.printSize, order.printBindingType)
    order.price = order.page_number * product.price
    order.save()


def save_order_file(message, file_oath, order_number):
    order = Order.objects.get(tg_pk=message.chat.id, order_number=order_number)
    order.file = file_oath
    order.file_status = False
    order.save()
    return order


def get_order(order_number):
    return Order.objects.get(order_number=order_number)
