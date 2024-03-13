from telebot import types


def contact_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(
        types.KeyboardButton(text="Контакт", request_contact=True)
    )

    return markup


def menu_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    ma2 = types.KeyboardButton(text="Профиль")
    markup.add(ma2)
    return markup