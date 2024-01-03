import asyncio
import json
from datetime import datetime

import telebot
from django.contrib.auth import get_user_model
from telebot import types

import logging
from apps.tg.buttons import main_menu, order_color, order_size, order_binding, order_info, location_request, \
    payment_type, location_share
from apps.tg.consta import BOT_TOKEN, MAX_FILE_SIZE_MB, GROUP_CHAT_ID

from apps.tg.models import PrintColor, PrintSize, PaymentType, DeliveryType
from apps.tg.utils import get_or_create_client, get_or_create_order, update_order_price, update_order_file_path, \
    get_order, \
    update_delivery, get_user_orders, update_order_color, update_order_size, update_order_binding, \
    update_order_file_status, \
    update_order_page_number, update_order_location_sentence, update_order_location_telegram_share
from apps.orders.models import PrintBindingTypes, ClientAddress
from apps.tg.message import MESSAGES

User = get_user_model()

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="html")
logger = logging.getLogger(__name__)

amount_of_page = False
sending_document = False
sending_location = False
user_phone_sharing = False
order_number = ""


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global order_number
    global sending_document
    global sending_location
    global amount_of_page
    order = get_order(order_number)
    bindings = PrintBindingTypes.objects.all()
    if call.data == "WHITE" or call.data == "COLOURFUL":
        update_order_color(call, order)
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, "Qaysi o'lchamda chop etmoqchisiz", reply_markup=order_size())
    elif call.data == "A5" or call.data == "A4" or call.data == "A3":
        update_order_size(call, order)
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, "Pereplyot shaklidini tanlang", reply_markup=order_binding())
    elif call.data == "photoOfBinding":
        for binding in bindings:
            bot.send_photo(call.message.chat.id, photo=binding.photo, caption=binding.name)
        bot.send_message(call.message.chat.id, "Pereplyot shaklidini tanlang", reply_markup=order_binding())

    elif PrintBindingTypes.objects.filter(name=call.data).exists():
        amount_of_page = True
        update_order_binding(call, order)
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, "Sahifalar sonini kiriting")
    elif call.data == "cancel_order":
        order.delete()
        bot.delete_message(call.message.chat.id, call.message.id)
        markup = main_menu()
        bot.send_message(call.message.chat.id, "Xizmatlardan birini tanlang", reply_markup=markup)
    elif call.data == "order_product":

        sending_document = True
        update_order_file_status(order)
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_photo(call.message.chat.id, photo=open('media/download.png', 'rb'),
                       caption="Hujjatni yuboring")
    elif call.data == 'location_request':
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, "Yetkazib berish usuli", reply_markup=location_request())

    elif call.data == 'Self_Delivery':
        sending_document = True
        update_order_file_status(order)
        update_delivery(order, DeliveryType.Self_Delivery)
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_photo(call.message.chat.id, photo=open('media/download.png', 'rb'),
                       caption="Hujjatni yuboring")

    elif call.data == 'Courier_Delivery':
        update_delivery(order, DeliveryType.Courier_Delivery)
        sending_location = True
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, "Manzilingizni yuboring", reply_markup=location_share())
    elif call.data == "backFromSize":
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, "Qaysi rangda chop etmoqchisiz 🖨️ 📄?", reply_markup=order_color())
    elif call.data == "backFromBinding":
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, "Qaysi o'lchamda chop etmoqchisiz", reply_markup=order_size())
    elif call.data == "backFromLocationChoose":
        bot.delete_message(call.message.chat.id, call.message.id)
        amount_of_page = False
        update_order_price(order)
        mess = f'<b>Sizning buyurtmangiz </b>\n\n\n\n<b>Buyurtma raqami 🔍 :</b> {order.order_number}\n\n<b>Varaqlar soni  📄 : </b> {order.page_number}' \
               f'\n\n<b>Chop etish formati 🖨 :</b> {order.printBindingType.name}\n\n<b>Rangi 📕 :</b> {order.get_printColor_display()}' \
               f'\n\n<b>Kitob o\'lchami 📏 : </b> {order.get_printSize_display()} \n\n<b>Narxi 🏷 :   </b> {order.price:.2f} so\'m  \n\n' \
               f'<b>Status : </b> {order.get_order_status_display()} \n\n \n\n' \
               f'Yaratildi 🕕 : {order.created_at:%d-%m-%Y %H:%M:%S}\n'

        bot.send_message(call.message.chat.id, mess, reply_markup=order_info())
    else:
        markup = main_menu()
        bot.send_message(call.message.chat.id, "Xizmatlardan birini tanlang", reply_markup=markup)


@bot.message_handler(commands=["start", "stop"])
def start(message):
    global user_phone_sharing
    user_phone_sharing = True
    mess = f'Assalomu aleykum , <b>{message.from_user.first_name}</b>!\nMen - <b>PrintBot</b>man,\nTizimdan foydalanish uchun telefon raqamingizni yuboring'
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Telefon 📱", request_contact=True))
    bot.send_message(
        message.chat.id, mess, reply_markup=keyboard)


CONTENT_TYPES = ["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact",
                 "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo",
                 "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id",
                 "migrate_from_chat_id", "pinned_message"]


@bot.message_handler()
def get_sms(message):
    keyboard = types.ReplyKeyboardRemove()
    global amount_of_page
    global order_number
    global sending_document
    global user_phone_sharing
    if message.chat.id == GROUP_CHAT_ID:
        bot.send_message(message.chat.id, "GROUP_CHAT_ID", reply_markup=keyboard)
    else:
        if user_phone_sharing:
            bot.send_message(message.chat.id, "Xizmatdan foydalanish uchun telefon raqamingizni yuboring")
        else:
            text = message.text
            if text == "Buyurtma berish 🛒":
                order_number = get_or_create_order(message)
                bot.send_message(message.chat.id, "Qaysi rangda chop etmoqchisiz 🖨️ 📄?", reply_markup=order_color())
            elif text == "Buyurtmalar 📦":
                order_list = get_user_orders(message.chat.id)
                for order in order_list:
                    mess = f'<b>Sizning buyurtmangiz </b>\n\n\n\n' \
                           f'<b>Buyurtma raqami 🔍 :</b> {order.order_number}\n\n' \
                           f'<b>Varaqlar soni  📄 : </b> {order.page_number}\n\n' \
                           f'<b>Chop etish formati 🖨 :</b> {order.printBindingType.name}\n\n' \
                           f'<b>Rangi 📕 :</b> {order.get_printColor_display()}\n\n' \
                           f'<b>Kitob o\'lchami 📏 : </b> {order.get_printSize_display()}\n\n' \
                           f'<b>Narxi 🏷 :   </b> {order.price:.2f} so\'m  \n\n' \
                           f'<b>Yetqazib berish turi 🚚 :   </b> {order.get_delivery_type_display()}  \n\n' \
                           f'<b>Status : </b> {order.get_order_status_display()} \n\n\n\n' \
                           f'Yaratildi 🕕 : {order.created_at:%d-%m-%Y %H:%M:%S}\n'
                    bot.send_message(message.chat.id, mess)
            elif text == "Sozlamalar ⚙️":
                bot.send_message(message.chat.id, text)
            elif text == "Biz haqimizda ℹ️":
                about_company_text = """
                   <b>🤖 Botga xush kelibsiz!</b>

                   <b>🌐 Biz haqimizda:</b>
                   Print Hub-bu sizning g'oyalaringizni hayotga tatbiq etishga bag'ishlangan yetakchi matbaa kompaniyasi hisoblanadi.
                   Biz kitoblar va nashrlarga alohida e'tibor qaratgan holda keng turdagi mahsulotlar uchun yuqori sifatli bosma xizmatlarni taqdim etishga ixtisoslashganmiz. 
                   
                   <b>📖 Bizning tajriba:</b>
                  Biz  bir qancha turdagi kitob chop etish xizmatlarini taqdim qilamiz .
                  Bizning zamonaviy bosma uskunalarimiz har bir chop etilayotgan kitobda  aniqlik va sifatni ta'minlaydi.
                   <b>🌟 Bizning qadriyatlar:</b>
                   - <i>Sifat:</i> Biz yuqori sifatda mahsulotlar ishlab chiqaramiz.
                   - <i>Mijozlar Ehtiyojini Qondirish:</i> Sizning mamnunligingiz bizning ustuvor vazifamizdir. Biz har bir buyurtma bilan alohida yondashamiz.
                   - <i>Innovation:</i> Bizda yangi texnologiyalar va bosib chiqarish texnikalari mavjud.

                   <b>📞 Bog'lanish:</b>
                   Biz bilan bog'lanmoqchimisiz? 
                   Biz bilan <a href="#">kebatotabek33@gmail.com</a> manzili orqali bog‘laning yoki qo‘shimcha ma’lumot olish uchun veb-saytimizga tashrif buyuring: <a href="https://www.printhub.com"> www.printhub.com</a>.

                   Bugun buyurtma bering!\nBizga ishonch bildirganingiz uchun rahmat! 🚀
                   """
                bot.send_message(message.chat.id, about_company_text)
            elif amount_of_page:
                if text.isnumeric():
                    order = get_order(order_number)
                    amount_of_page = False
                    update_order_page_number(order, text)
                    update_order_price(order)
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
                sending_document = True
                update_order_location_sentence(order_number, text)
                bot.delete_message(message.chat.id, message.id)
                bot.send_photo(message.chat.id, photo=open('media/download.png', 'rb'),
                               caption="Hujjatni yuboring")
            else:
                markup = main_menu()
                bot.send_message(message.chat.id, "Xizmatlardan birini tanlang", reply_markup=markup)


@bot.message_handler(content_types=["contact"])
def get_contact(message):
    global user_phone_sharing
    user_phone_sharing = False
    get_or_create_client(message)
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
            bot.send_message(message.chat.id, "Xodimimiz tez orada siz bilan bog'lanadi", disable_notification=False
                             )

            order = update_order_file_path(message, file_path, order_number)

            mess = f'<b>Sizning buyurtmangiz muvoffaqiyatli yaratildi.\n\nTez orada xodimimiz siz bilan bog\'lanadi!!!</b>\n\n\n' \
                   f'<b>Buyurtma 🔍 :</b> {order.order_number}\n\n' \
                   f'<b>Varaqlar soni  📄 : </b> {order.page_number}\n\n' \
                   f'<b>Chop etish formati 🖨 :</b> {order.printBindingType.name}\n\n' \
                   f'<b>Rangi 📕 :</b> {order.get_printColor_display()}\n\n' \
                   f'<b>Kitob o\'lchami 📏 : </b> {order.get_printSize_display()} \n\n' \
                   f'<b>Narxi 🏷 :   </b> {order.price:.2f} so\'m  \n\n' \
                   f'<b>Status : </b> {order.get_order_status_display()} \n\n \n\n' \
                   f'Yaratildi 🕕 : {order.created_at:%d-%m-%Y %H:%M:%S}\n'
            admin_message = f'<b>Yangi buyurtma </b>' \
                            f'\n\n\n\n<b>Buyurtma  🔍 :</b> {order.order_number}' \
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
    global sending_document
    sending_document = True
    update_order_location_telegram_share(message, order_number)
    bot.delete_message(message.chat.id, message.id)
    bot.send_photo(message.chat.id, photo=open('media/download.png', 'rb'),
                   caption="Hujjatni yuboring")


def polToWebhook(request):
    update = telebot.types.Update.de_json(json.loads(request.body.decode('utf-8')))
    bot.process_new_updates([update])
    return True
