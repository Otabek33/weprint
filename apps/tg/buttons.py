from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from apps.clients.models import Client
from telebot import types

from apps.tg.models import PrintColor, PrintSize


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttonA = types.KeyboardButton(text='Buyurtma berish 🛒')
    buttonB = types.KeyboardButton(text='Buyurtmalar 📦')
    buttonC = types.KeyboardButton(text='Sozlamalar ⚙️')
    buttonD = types.KeyboardButton(text='Biz haqimizda ℹ️')
    markup.row(buttonA, buttonB)
    markup.row(buttonC, buttonD)
    return markup


def order_color():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton(f"{PrintColor.WHITE.value} 📃", callback_data="white"),
               InlineKeyboardButton(f"{PrintColor.COLOURFUL.value} 🌈", callback_data="color"))
    return markup


def order_size():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton(f"{PrintSize.A5.value}", callback_data="a5"))
    markup.add(InlineKeyboardButton(f"{PrintSize.A4.value}", callback_data="a4"))
    markup.add(InlineKeyboardButton(f"{PrintSize.A3.value}", callback_data="a3"))
    markup.add(InlineKeyboardButton(f"🔙 Ortga", callback_data="backSize"))
    return markup


def themes():
    objects = Client.objects.all()
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    for i in objects:
        markup.add(InlineKeyboardButton(f"{i.content}", callback_data=f"theme_pk_{i.id}"))
    return markup
