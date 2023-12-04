from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from apps.clients.models import Client
from telebot import types

from apps.tg.models import PrintColor, PrintSize, PrintBindingTypes


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
    markup.add(InlineKeyboardButton(f"{PrintColor.WHITE.label} 📃", callback_data="WHITE"),
               InlineKeyboardButton(f"{PrintColor.COLOURFUL.label} 🌈", callback_data="COLOURFUL"))
    return markup


def order_size():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton(f"{PrintSize.A5.label}", callback_data="A5"))
    markup.add(InlineKeyboardButton(f"{PrintSize.A4.label}", callback_data="A4"))
    markup.add(InlineKeyboardButton(f"{PrintSize.A3.label}", callback_data="A3"))
    markup.add(InlineKeyboardButton(f"🔙 Ortga", callback_data="backFromSize"))
    return markup


def order_binding():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton(f"{PrintBindingTypes.SPIRAL.label}", callback_data="SPIRAL"),
               InlineKeyboardButton(f"{PrintBindingTypes.SADDLE_STITCH.label}", callback_data="SADDLE_STITCH"))
    markup.add(InlineKeyboardButton(f"{PrintBindingTypes.PERFECT_BINDING.label}", callback_data="PERFECT_BINDING"),
               InlineKeyboardButton(f"{PrintBindingTypes.CASE.label}", callback_data="CASE"))
    markup.add(InlineKeyboardButton(f"{PrintBindingTypes.PLASTIC_COMB.label}", callback_data="PLASTIC_COMB"),
               InlineKeyboardButton(f"{PrintBindingTypes.NO_BINDING.label}", callback_data="NO_BINDING"))
    markup.add(InlineKeyboardButton(f"🔙 Ortga", callback_data="backFromBinding"))
    return markup


def themes():
    objects = Client.objects.all()
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    for i in objects:
        markup.add(InlineKeyboardButton(f"{i.content}", callback_data=f"theme_pk_{i.id}"))
    return markup
