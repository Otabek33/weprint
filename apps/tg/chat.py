import asyncio
import json
from datetime import datetime

import telebot
from django.contrib.auth import get_user_model
from telebot import types

import logging
from apps.tg.buttons import main_menu, order_color, order_size, order_binding, order_info, location_request, \
    payment_type, location_share
from apps.tg.consta import BOT_TOKEN, PAYMENTS_PROVIDER_TOKEN, TIME_MACHINE_IMAGE_URL, MAX_FILE_SIZE_MB, GROUP_CHAT_ID

from apps.tg.models import PrintColor, PrintSize, PaymentType, DeliveryType
from apps.tg.utils import get_or_create_user, get_or_create_order, generation_price, save_order_file, get_order, \
    update_delivery
from apps.orders.models import PrintBindingTypes, ClientAddress
from apps.tg.message import MESSAGES

User = get_user_model()

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="html")
logger = logging.getLogger(__name__)

amount_of_page = False
sending_document = False
sending_location = False
order_number = ""


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global order_number
    global sending_document
    global sending_location
    order = get_order(order_number)
    bindings = PrintBindingTypes.objects.all()
    if call.data == "WHITE" or call.data == "COLOURFUL":
        # bot.answer_callback_query(call.id, "Keyingi bosqichga o'tyapsiz!", show_alert=True)
        printColor = PrintColor[call.data]
        order_number = order.order_number
        order.printColor = printColor
        order.save()
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, "Qaysi o'lchamda chop etmoqchisiz", reply_markup=order_size())
    elif call.data == "A5" or call.data == "A4" or call.data == "A3":
        printSize = PrintSize[call.data]
        order.printSize = printSize
        order.save()
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, "Pereplyot shaklidini tanlang", reply_markup=order_binding())
    elif call.data == "photoOfBinding":
        for binding in bindings:
            bot.send_photo(call.message.chat.id, photo=binding.photo, caption=binding.name)
        bot.send_message(call.message.chat.id, "Pereplyot shaklidini tanlang", reply_markup=order_binding())

    elif PrintBindingTypes.objects.filter(name=call.data).exists():
        order.printBindingType = PrintBindingTypes.objects.filter(name=call.data).first()
        order.save()
        global amount_of_page
        amount_of_page = True
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, "Sahifalar sonini kiriting")
    elif call.data == "cancel_order":
        order.delete()
        bot.delete_message(call.message.chat.id, call.message.id)
        markup = main_menu()
        bot.send_message(call.message.chat.id, "Xizmatlardan birini tanlang", reply_markup=markup)
    elif call.data == "order_product":

        sending_document = True
        order.file_status = True
        order.save()
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_photo(call.message.chat.id, photo=open('media/download.png', 'rb'),
                       caption="Hujjatni yuboring")
    elif call.data == 'location_request':
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, "Yetkazib berish usuli", reply_markup=location_request())

    elif call.data == 'Self_Delivery':
        update_delivery(order, DeliveryType.Self_Delivery)
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, "To'lov turini tanlang", reply_markup=payment_type())

    elif call.data == 'Courier_Delivery':
        update_delivery(order, DeliveryType.Courier_Delivery)
        sending_location = True
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, "Manzilingizni yuboring", reply_markup=location_share())
    elif call.data == 'CASH':
        sending_document = True
        order.file_status = True
        order.cash_type = PaymentType.CASH
        order.save()
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_photo(call.message.chat.id, photo=open('media/download.png', 'rb'),
                       caption="Hujjatni yuboring")
    elif call.data == 'CARD':
        if PAYMENTS_PROVIDER_TOKEN.split(':')[1] == 'TEST':
            bot.send_message(call.message.chat.id, MESSAGES['pre_buy_demo_alert'])

        order.cash_type = PaymentType.CARD
        order.save()
        # Setup prices
        PRICE = types.LabeledPrice(label='Настоящая Машина Времени', amount=4200000)
        bot.delete_message(call.message.chat.id, call.message.id)

    elif call.data == "backFromSize":
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, "Qaysi rangda chop etmoqchisiz 🖨️ 📄?", reply_markup=order_color())
    elif call.data == "backFromBinding":
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, "Qaysi o'lchamda chop etmoqchisiz", reply_markup=order_size())
    elif call.data == "backFromLocationChoose":
        bot.delete_message(call.message.chat.id, call.message.id)
        order = get_order(order_number)
        amount_of_page = False
        order.created_at = datetime.now()
        order.save()
        generation_price(order)
        mess = f'<b>Sizning buyurtmangiz </b>\n\n\n\n<b>Buyurtma raqami 🔍 :</b> {order.order_number}\n\n<b>Varaqlar soni  📄 : </b> {order.page_number}' \
               f'\n\n<b>Chop etish formati 🖨 :</b> {order.printBindingType.name}\n\n<b>Rangi 📕 :</b> {order.get_printColor_display()}' \
               f'\n\n<b>Kitob o\'lchami 📏 : </b> {order.get_printSize_display()} \n\n<b>Narxi 🏷 :   </b> {order.price:.2f} so\'m  \n\n' \
               f'<b>Status : </b> {order.get_order_status_display()} \n\n \n\n' \
               f'Yaratildi 🕕 : {order.created_at:%d-%m-%Y %H:%M:%S}\n'

        bot.send_message(call.message.chat.id, mess, reply_markup=order_info())
    elif call.data == "backFromPaymentChoose":
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, "Yetkazib berish usuli", reply_markup=location_request())
    else:
        markup = main_menu()
        bot.send_message(call.message.chat.id, "Xizmatlardan birini tanlang", reply_markup=markup)


@bot.message_handler(commands=["start", "stop"])
async def start(message):
    mess = f'Ассалому алейкум , <b>{message.from_user.first_name}</b>!\nМен - <b>GimsShopBot</b>,\nТизимдан фойдаланишдан олдин Телефон рақамингизни юборинг'
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Телефон 📱", request_contact=True))
    bot.send_message(
        message.chat.id, mess, reply_markup=keyboard)


CONTENT_TYPES = ["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact",
                 "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo",
                 "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id",
                 "migrate_from_chat_id", "pinned_message"]


@bot.message_handler()
def get_sms(message):
    user, tguser = get_or_create_user(message)
    attr_value = getattr(user, "phone", False)
    keyboard = types.ReplyKeyboardRemove()

    global amount_of_page
    global order_number

    if attr_value is False:
        bot.send_message(message.chat.id, "Xizmatdan foydalanish uchun telefon raqamingizni yuboring")
    else:
        text = message.text
        if text == "Buyurtma berish 🛒":
            client, order = get_or_create_order(message)
            order_number = order.order_number
            bot.send_message(message.chat.id, "Qaysi rangda chop etmoqchisiz 🖨️ 📄?", reply_markup=order_color())
        elif text == "Buyurtmalar 📦":
            bot.send_message(message.chat.id, text)
        elif text == "Sozlamalar ⚙️":
            bot.send_message(message.chat.id, text)
        elif text == "Biz haqimizda ℹ️":
            bot.send_message(message.chat.id, text)
        elif amount_of_page:
            if text.isnumeric():
                order = get_order(order_number)
                amount_of_page = False
                order.page_number = int(text)
                order.created_at = datetime.now()
                order.save()
                generation_price(order)
                mess = f'<b>Sizning buyurtmangiz </b>\n\n\n\n<b>Buyurtma raqami 🔍 :</b> {order.order_number}\n\n<b>Varaqlar soni  📄 : </b> {order.page_number}' \
                       f'\n\n<b>Chop etish formati 🖨 :</b> {order.printBindingType.name}\n\n<b>Rangi 📕 :</b> {order.get_printColor_display()}' \
                       f'\n\n<b>Kitob o\'lchami 📏 : </b> {order.get_printSize_display()} \n\n<b>Narxi 🏷 :   </b> {order.price:.2f} so\'m  \n\n' \
                       f'<b>Status : </b> {order.get_order_status_display()} \n\n \n\n' \
                       f'Yaratildi 🕕 : {order.created_at:%d-%m-%Y %H:%M:%S}\n'

                bot.send_message(message.chat.id, mess, reply_markup=order_info())

            else:
                bot.send_message(message.chat.id, 'Iltimos sahifalar miqdorini yuboring')
        elif sending_document:
            bot.send_message(message.chat.id, 'Iltimos hujjat yuboring')
        elif sending_location:
            order = get_order(order_number)
            # Extract latitude and longitude from the message
            location, created = ClientAddress.objects.get_or_create(name=text)
            order.location = location
            order.save()
            bot.delete_message(message.chat.id, message.id)
            bot.send_message(message.chat.id, "To'lov turini tanlang", reply_markup=payment_type())


        else:
            markup = main_menu()
            bot.send_message(message.chat.id, "Xizmatlardan birini tanlang", reply_markup=markup)


@bot.message_handler(content_types=["contact"])
def get_contact(message):
    client, tguser = get_or_create_user(message)
    client.phone = message.contact.phone_number
    client.save()
    keyboard = types.ReplyKeyboardRemove()
    markup = main_menu()
    bot.send_message(message.chat.id, "Xizmatlardan birini tanlang", reply_markup=markup)


@bot.message_handler(content_types=['document'])
def get_document(message):
    import os
    from django.conf import settings
    global sending_document

    sending_document = False
    # Ensure the "uploads" directory within "media" exists
    uploads_directory = os.path.join(settings.MEDIA_ROOT, "uploads")
    if not os.path.exists(uploads_directory):
        os.makedirs(uploads_directory)

    # Get the file path from the File object
    file_info = bot.get_file(message.document.file_id)
    file_path_telegram = file_info.file_path

    # Construct the absolute file path within the media/uploads directory
    file_path = os.path.join(uploads_directory, message.document.file_name)

    # Download the file content using the file_path
    downloaded_file = bot.download_file(file_path_telegram)
    max_file_size_bytes = MAX_FILE_SIZE_MB * 1024 * 1024

    if message.document.file_size > max_file_size_bytes:
        bot.send_message(message.chat.id, "Yuborilayotgan hujjat hajmi 50 mb dan kichik bo'lishi kerak")
    else:
        if message.document.file_name.lower().endswith('.pdf') or message.document.file_name.lower().endswith(
                ('.doc', '.docx')):
            with open(file_path, 'wb') as local_file:
                local_file.write(downloaded_file)

            # Now, you can save the file path to your Django model
            order = save_order_file(message, file_path, order_number)

            mess = f'<b>Sizning buyurtmangiz muvoffaqiyatli yaratildi.\nTez orada xodimimiz siz bilan bog\'lanadi!!!</b>\n\n\n' \
                   f'<b>Buyurtma raqami 🔍 :</b> {order.order_number}\n\n' \
                   f'<b>Varaqlar soni  📄 : </b> {order.page_number}\n\n' \
                   f'<b>Chop etish formati 🖨 :</b> {order.printBindingType.name}\n\n' \
                   f'<b>Rangi 📕 :</b> {order.get_printColor_display()}\n\n' \
                   f'<b>Kitob o\'lchami 📏 : </b> {order.get_printSize_display()} \n\n' \
                   f'<b>Narxi 🏷 :   </b> {order.price:.2f} so\'m  \n\n' \
                   f'<b>Status : </b> {order.get_order_status_display()} \n\n \n\n' \
                   f'Yaratildi 🕕 : {order.created_at:%d-%m-%Y %H:%M:%S}\n'
            admin_message = f'<b>Yangi buyurtma </b>' \
                            f'\n\n\n\n<b>Buyurtma raqami 🔍 :</b> {order.order_number}' \
                            f'\n\n<b>Buyurtma beruvchi  👤:</b> {order.created_by}' \
                            f'\n\n<b>Telefon 📞 :</b> {order.created_by.phone}' \
                            f'\n\n<b>To\'lov turi 💳 :</b> {order.get_cash_type_display()}' \
                            f'\n\n<b>Yetqazib berish turi 🚚 :</b> {order.get_delivery_type_display()}' \
                            f'\n\n<b>Adres 🏠 :</b> ' \
                            f'\n<b>manzil nomi =></b>{order.location.name}' \
                            f'\n<b>latitude =></b>{order.location.latitude}' \
                            f'\n<b>longitude =></b>{order.location.longitude} ' \
                            f'\n\n<b>==============</b>' \
                            f'\n\n<b>Varaqlar soni  📄 : </b> {order.page_number}' \
                            f'\n\n<b>Chop etish formati 🖨 :</b> {order.printBindingType.name}' \
                            f'\n\n<b>Rangi 📕 :</b> {order.get_printColor_display()}' \
                            f'\n\n<b>Kitob o\'lchami 📏 : </b> {order.get_printSize_display()}' \
                            f'\n\n<b>Narxi 🏷 :   </b> {order.price:.2f} so\'m' \
                            f'\n\n<b>Status : </b> {order.get_order_status_display()}' \
                            f'\n\n \n\nYaratildi 🕕 : {order.created_at:%d-%m-%Y %H:%M:%S}\n'
            bot.send_message(message.chat.id, mess, reply_markup=main_menu())
            bot.send_document(chat_id=GROUP_CHAT_ID, document=open(file_path, 'rb'), caption=admin_message)
            os.remove(file_path)


        else:
            bot.send_message(message.chat.id, "Yuborilayotgan hujjat pdf yoki word ko'rinishida bo'lishi kerak")
            # Save the file content to a local file


@bot.message_handler(content_types=['location'])
def get_location(message):
    order = get_order(order_number)
    # Extract latitude and longitude from the message
    location, created = ClientAddress.objects.get_or_create(name=message.chat.id, latitude=message.location.latitude,
                                                            longitude=message.location.longitude)
    order.location = location
    order.save()

    # Your logic to handle the location data
    bot.delete_message(message.chat.id, message.id)

    bot.send_message(message.chat.id, "To'lov turini tanlang", reply_markup=payment_type())


def polToWebhook(request):
    update = telebot.types.Update.de_json(json.loads(request.body.decode('utf-8')))
    bot.process_new_updates([update])
    return True
