import json
from datetime import datetime

import telebot
from django.contrib.auth import get_user_model
from telebot import types

import logging
from apps.tg.buttons import main_menu, order_color, order_size, order_binding, order_info, location_request, \
    payment_type

from apps.tg.models import TelegramUser, PrintColor, PrintSize, PaymentType, DeliveryType
from apps.tg.utils import get_or_create_user, get_or_create_order, generation_price, save_order_file, get_order, \
    update_delivery
from apps.orders.models import PrintBindingTypes

User = get_user_model()

TOKEN = "6788108652:AAE89YGQ06R2aqds3RP5mhymRJqBE9Djblg"

bot = telebot.TeleBot(TOKEN, parse_mode="html")
logger = logging.getLogger(__name__)

amount_of_page = False
sending_document = False
order_number = ""
MAX_FILE_SIZE_MB = 50
GROUP_CHAT_ID = 4089429437


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global order_number
    global sending_document
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
    elif call.data == "order_save":
        bot.answer_callback_query(call.id, "Buyurtma muvofaqiyatli saqlandi", show_alert=True)
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
        location = location_request()
        bot.send_message(call.message.chat.id, "Yetkazib berish usuli", reply_markup=location)

    elif call.data == 'Self_Delivery':
        update_delivery(order, DeliveryType.Self_Delivery)
        bot.delete_message(call.message.chat.id, call.message.id)
        payment = payment_type()
        bot.send_message(call.message.chat.id, "To'lov turini tanlang", reply_markup=payment)

    elif call.data == 'Courier_Delivery':
        update_delivery(order, DeliveryType.Courier_Delivery)
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, "Courier_Delivery")
    elif call.data == 'Naqt':
        bot.delete_message(call.message.chat.id, call.message.id)
        global sending_document

        sending_document = True
        order.file_status = True
        order.cash_type = PaymentType.CASH
        order.save()
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_photo(call.message.chat.id, photo=open('media/download.png', 'rb'),
                       caption="Hujjatni yuboring")

    elif call.data == "backFromSize":
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, "Qaysi rangda chop etmoqchisiz 🖨️ 📄?", reply_markup=order_color())
    elif call.data == "backFromBinding":
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, "Qaysi o'lchamda chop etmoqchisiz", reply_markup=order_size())
    elif call.data == "backFromLocationChoose":
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
def start(message):
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

            bot.send_message(message.chat.id, "Xujjat qabul qilindi")
            mess = f'<b>Sizning buyurtmangiz </b>\n\n\n\n<b>Buyurtma raqami 🔍 :</b> {order.order_number}\n\n<b>Varaqlar soni  📄 : </b> {order.page_number}' \
                   f'\n\n<b>Chop etish formati 🖨 :</b> {order.printBindingType.name}\n\n<b>Rangi 📕 :</b> {order.get_printColor_display()}' \
                   f'\n\n<b>Kitob o\'lchami 📏 : </b> {order.get_printSize_display()} \n\n<b>Narxi 🏷 :   </b> {order.price:.2f} so\'m  \n\n' \
                   f'<b>Status : </b> {order.get_order_status_display()} \n\n \n\n' \
                   f'Yaratildi 🕕 : {order.created_at:%d-%m-%Y %H:%M:%S}\n'
            admin_message = f'<b>Yangi buyurtma </b>\n\n\n\n<b>Buyurtma raqami 🔍 :</b> {order.order_number}\n\n<b>Buyurtma beruvchi 🔍 :</b> {order.created_by}\n\n' \
                            f'<b>Telefon 🔍 :</b> {order.created_by.phone}\n\n<b>Varaqlar soni  📄 : </b> {order.page_number}' \
                            f'\n\n<b>Chop etish formati 🖨 :</b> {order.printBindingType.name}\n\n<b>Rangi 📕 :</b> {order.get_printColor_display()}' \
                            f'\n\n<b>Kitob o\'lchami 📏 : </b> {order.get_printSize_display()} \n\n<b>Narxi 🏷 :   </b> {order.price:.2f} so\'m  \n\n' \
                            f'<b>Status : </b> {order.get_order_status_display()} \n\n \n\n' \
                            f'Yaratildi 🕕 : {order.created_at:%d-%m-%Y %H:%M:%S}\n'
            bot.send_document(message.chat.id, document=open(file_path, 'rb'), caption=mess)
            bot.send_document(chat_id=-4089429437, document=open(file_path, 'rb'), caption=admin_message)
            os.remove(file_path)


        else:
            bot.send_message(message.chat.id, "Yuborilayotgan hujjat pdf yoki word ko'rinishida bo'lishi kerak")
            # Save the file content to a local file


def polToWebhook(request):
    update = telebot.types.Update.de_json(json.loads(request.body.decode('utf-8')))
    bot.process_new_updates([update])
    return True
