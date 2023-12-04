from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from apps.clients.models import Client
from telebot import types


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttonA = types.KeyboardButton(text='Buyurtma berish 🛒')
    buttonB = types.KeyboardButton(text='Buyurtmalar 📦')
    buttonC = types.KeyboardButton(text='Sozlamalar ⚙️')
    buttonD = types.KeyboardButton(text='Biz haqimizda ℹ️')

    markup.row(buttonA, buttonB)
    markup.row(buttonC, buttonD)

    return markup


def themes():
    objects = Client.objects.all()
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    for i in objects:
        markup.add(InlineKeyboardButton(f"{i.content}", callback_data=f"theme_pk_{i.id}"))
    return markup
