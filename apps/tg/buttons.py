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
    # for printColor in PrintColor:
    counter = 0
    color_list = []
    for printColor in PrintColor:
        counter += 1
        color_list.append(InlineKeyboardButton(f"{str(printColor.label)}", callback_data=str(printColor.name)))
        if counter == 2:
            markup.add(color_list[0], color_list[1])
            counter = 0
            color_list = []
    return markup


def order_size():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    for printSize in PrintSize:
        markup.add(InlineKeyboardButton(f"{str(printSize.label)}", callback_data=str(printSize.label)))
    markup.add(InlineKeyboardButton(f"🔙 Ortga", callback_data="backFromSize"))
    return markup


def order_binding():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    bindings = PrintBindingTypes.objects.all()

    for binding in bindings:
        markup.add(InlineKeyboardButton(binding.name, callback_data=binding.name))
    markup.add(InlineKeyboardButton(f"📷 Rasmlar", callback_data="photoOfBinding"))
    markup.add(InlineKeyboardButton(f"🔙 Ortga", callback_data="backFromBinding"))
    return markup


# InlineKeyboardButton(f"Buyurtma berish ✔", callback_data="order_product"))

def order_info():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton(f"Bekor qilish ❌", callback_data="cancel_order"),
               InlineKeyboardButton(f"Davom etirish", callback_data="location_request"))
    markup.add(InlineKeyboardButton(f"Saqlab qo'yish ➕", callback_data="order_save"))
    markup.add(InlineKeyboardButton(f"🔙 Ortga", callback_data="backFromOrderInfo"))
    return markup


def location_request():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton(f"O'zim olib ketaman", callback_data="self_take"),
               InlineKeyboardButton(f"Kuryerlik hizmati", callback_data="courier_service"))
    markup.add(InlineKeyboardButton(f"🔙 Ortga", callback_data="backFromLocationChoose"))


def themes():
    objects = Client.objects.all()
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    for i in objects:
        markup.add(InlineKeyboardButton(f"{i.content}", callback_data=f"theme_pk_{i.id}"))
    return markup
