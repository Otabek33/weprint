import json
import random

import telebot
from django.contrib.auth import get_user_model
from telebot import types
from telegram import KeyboardButton, ReplyKeyboardMarkup
import logging
from apps.tg.buttons import main_menu, themes, order_color, order_size
from apps.tg.choices import RoleTypeChoices
from apps.tg.models import Chat, Message, TelegramUser
from apps.tg.utils import get_or_create_user

User = get_user_model()

TOKEN = "6788108652:AAE89YGQ06R2aqds3RP5mhymRJqBE9Djblg"

bot = telebot.TeleBot(TOKEN, parse_mode="html")
logger = logging.getLogger(__name__)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    tg_user = TelegramUser.objects.get(tg_pk=call.message.chat.id)
    if call.data == "white" or call.data == "color":
        # bot.answer_callback_query(call.id, "Keyingi bosqichga o'tyapsiz!", show_alert=True)
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, "Qaysi o'lchamda chop etmoqchisiz", reply_markup=order_size())


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
    if attr_value is False:
        bot.send_message(message.chat.id, "Xizmatdan foydalanish uchun telefon raqamingizni yuboring")
    else:
        text = message.text
        if text == "Buyurtma berish 🛒":
            bot.send_message(message.chat.id, "Qaysi rangda chop etmoqchisiz 🖨️ 📄?", reply_markup=order_color())
        elif text == "Buyurtmalar 📦":
            bot.send_message(message.chat.id, text)
        elif text == "Sozlamalar ⚙️":
            bot.send_message(message.chat.id, text)
        elif text == "Biz haqimizda ℹ️":
            bot.send_message(message.chat.id, text)
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


def polToWebhook(request):
    update = telebot.types.Update.de_json(json.loads(request.body.decode('utf-8')))
    bot.process_new_updates([update])
    return True
