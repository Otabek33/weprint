from datetime import datetime

from django.contrib.auth import get_user_model

from apps.clients.models import Client
from apps.orders.models import (ClientAddress, Order, OrderStatus,
                                PrintBindingTypes)
from apps.products.models import Product
from apps.tg.models import PrintColor, PrintSize

User = get_user_model()


def get_or_create_client(message):
    client, created = Client.objects.get_or_create(userId=message.chat.id)
    if created:
        client.first_name = message.from_user.first_name or ""
        client.username = message.from_user.username or ""
        client.last_name = message.from_user.last_name or ""
        client.phone = message.contact.phone_number
        client.save()


def get_or_create_order(message):
    client = Client.objects.get(userId=message.chat.id)
    order, created = Order.objects.get_or_create(
        tg_pk=message.chat.id,
        created_by=client,
        order_status=OrderStatus.CREATION,
        page_number=0,
    )
    if created:
        order.created_by = client
        order.order_number = generate_order_number()
        order.save()
    return order.order_number


def update_order_color(call, order):
    printColor = PrintColor[call.data]
    order.printColor = printColor
    order.save()


def update_order_size(call, order):
    printSize = PrintSize[call.data]
    order.printSize = printSize
    order.save()


def update_order_binding(call, order):
    order.printBindingType = PrintBindingTypes.objects.filter(name=call.data).first()
    order.save()


def update_order_file_status(order):
    order.file_status = True
    order.save()


def order_generation():
    last_transaction = len(
        Order.objects.exclude(order_status=OrderStatus.CREATION).all()
    )
    if last_transaction is not None:
        # Transaction exists
        return last_transaction + 1
    else:
        return 1


def generate_order_number():
    # Static prefix for the order number
    prefix = "BUY"

    # Current timestamp to include in the order number
    timestamp = datetime.now().strftime("%d%m%Y%H%M")

    # Combine the elements to create the order number
    order_number = f"{prefix}-{timestamp}-{order_generation()}"

    return order_number


def get_user_orders(user_id):
    client = Client.objects.get(userId=user_id)
    excluded_statuses = [OrderStatus.CREATION]
    return Order.objects.filter(created_by=client).exclude(
        order_status__in=excluded_statuses
    )


def update_order_price(order):
    product = Product.objects.get(
        printColor=order.printColor,
        printSize=order.printSize,
        printBindingType=order.printBindingType,
    )
    order.price = order.page_number * product.price
    order.created_at = datetime.now()
    order.save()


def update_order_page_number(order, text):
    order.page_number = int(text)
    order.save()


def update_order_location_sentence(order_number, text):
    order = get_order(order_number)
    location, created = ClientAddress.objects.get_or_create(name=text)
    order.location = location
    order.file_status = True
    order.save()


def update_order_file_path(message, file_oath, order_number):
    try:
        # Try to get an existing order
        order = Order.objects.get(tg_pk=message.chat.id, order_number=order_number)
    except Order.DoesNotExist:
        # Order doesn't exist, create a new one
        order = Order.objects.create(
            tg_pk=message.chat.id,
            order_number=order_number,
            file=file_oath,
            file_status=False,
            order_status=OrderStatus.ORDERED,
        )
    else:
        # Update the existing order
        order.file = file_oath
        order.file_status = False
        order.order_status = OrderStatus.ORDERED
        order.save()

    return order


def update_order_location_telegram_share(message, order_number):
    order = get_order(order_number)
    try:
        location = ClientAddress.objects.get(
            name=message.chat.id,
            latitude=message.location.latitude,
            longitude=message.location.longitude,
        )
    except Exception:
        location = ClientAddress.objects.create(name=message.chat.id,
                                                latitude=message.location.latitude,
                                                longitude=message.location.longitude, )

    order.location = location
    order.file_status = True
    order.save()


def get_order(order_number):
    try:
        order, created = Order.objects.get_or_create(order_number=order_number)
        return order
    except Exception as e:
        return Order.objects.create()


def update_delivery(order, delivery_type):
    order.delivery_type = delivery_type
    order.save()
