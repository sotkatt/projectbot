from telebot import types


def start_text_inline():
    markup = types.InlineKeyboardMarkup(row_width=1)    

    ik_1 = types.InlineKeyboardButton(
        text="Достопримечательности", 
        callback_data="ik_1"
    )

    ik_2 = types.InlineKeyboardButton(
        text="Музеи и Галереи", 
        callback_data="ik_2"
    )

    ik_3 = types.InlineKeyboardButton(
        text="Рестораны и Кафе", 
        callback_data="ik_3"
    )

    ik_4 = types.InlineKeyboardButton(
        text="Развлечения и активный отдых", 
        callback_data="ik_4"
    )
    ik_5 = types.InlineKeyboardButton(
        text="Меню", 
        callback_data="menu"
    )

    markup.add(ik_1, ik_2, ik_3, ik_4, ik_5)
    return markup


def search_places():
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    ik_1 = types.InlineKeyboardButton(
        text="Поиск мест...",
        switch_inline_query_current_chat="",
    )
    markup.add(ik_1)
    return markup