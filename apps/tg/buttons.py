from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from apps.clients.models import Client
from telebot import types

from apps.tg.models import PrintColor, PrintSize
from apps.orders.models import PrintBindingTypes


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
    bindings = PrintBindingTypes.objects.all()
    counter = 0
    bind_list = []
    for binding in bindings:
        counter += 1
        bind_list.append(InlineKeyboardButton(binding.name, callback_data=binding.name))
        if counter == 2:
            markup.add(bind_list[0], bind_list[1])
            counter = 0
            bind_list = []

    markup.add(InlineKeyboardButton(f"📷 Rasmlar", callback_data="photoOfBinding"))
    markup.add(InlineKeyboardButton(f"🔙 Ortga", callback_data="backFromBinding"))
    return markup


def order_info():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton(f"Bekor qilish ❌", callback_data="cancel_order"),
               InlineKeyboardButton(f"Buyurtma berish ✔", callback_data="order_product"))
    markup.add(InlineKeyboardButton(f"Saqlab qo'yish ➕", callback_data="order_save"))
    markup.add(InlineKeyboardButton(f"🔙 Ortga", callback_data="backFromOrderInfo"))
    return markup


def themes():
    objects = Client.objects.all()
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    for i in objects:
        markup.add(InlineKeyboardButton(f"{i.content}", callback_data=f"theme_pk_{i.id}"))
    return markup
