from datetime import datetime

import telebot
from telebot import types

from core.inlines import start_text_inline, search_places
from core.buttons import contact_button, menu_button
from core.examples import (
    START_TEXT, IK_1, IK_2, IK_3, IK_4, use_it_for_your_health
)
from core.settings import (
    TOKEN,  URL_SEARCH
)
from core.database import (
    registration_user, get_user, search_title
)


bot = telebot.TeleBot(TOKEN, parse_mode="HTML")


@bot.message_handler(commands=['start'])
def start(message):
    bname = bot.get_me().first_name
    bot.reply_to(message, START_TEXT.format(bot_name=bname),
                 reply_markup=start_text_inline())
    
    if get_user(message.from_user.id) is None:
        bot.send_message(
            message.chat.id,
            "Для регистрации нажмите на 'Контакт'",
            reply_markup=contact_button())
    else:
        bot.send_message(message.chat.id, "Вы уже зарегистрированы!")

        bot.send_message(
            message.chat.id,
            use_it_for_your_health,
            reply_markup=search_places()
        )

    # if str(message.from_user.id) not in database:
    #     bot.send_message(
    #         message.chat.id,
    #         "Для регистрации нажмите на 'Контакт'",
    #         reply_markup=contact_button())
    # else:
    #     bot.send_message(message.chat.id, "Вы уже зарегистрированы!", reply_markup=menu_button())

    #     bot.send_message(
    #         message.chat.id,
    #         use_it_for_your_health,
    #         reply_markup=search_places()
    #     )
    

@bot.message_handler(content_types=['contact'])
def contact(message):
    user = message.from_user
    if get_user(user.id) is None:
        registration_user(
            user.id, user.first_name, user.last_name, user.username,
            message.contact.phone_number
        )
        bot.send_message(message.chat.id, "Вы уже зарегистрированы!", 
            reply_markup=types.ReplyKeyboardRemove())

        bot.send_message(
            message.chat.id,
            use_it_for_your_health,
            reply_markup=search_places()
        )
    else:
        bot.send_message(message.chat.id, "Вы уже зарегистрированы!", 
            reply_markup=types.ReplyKeyboardRemove())


@bot.inline_handler(func=lambda query: query.query != '')
def inline_search(query):
    # database = load_database()
    if str(get_user(query.from_user.id)) is None:
        bot.send_message(
            query.from_user.id,
            "Для регистрации нажмите на 'Контакт'",
            reply_markup=contact_button())
        return
    else:
        text = query.query
        results = search_title(text[:len(text)-2])

      
        articles = []
        for result in results:
         

            article = types.InlineQueryResultArticle(
                id=result[0],
                title=result[1],
                description=result[3],
                thumbnail_url=URL_SEARCH,
                input_message_content=types.InputTextMessageContent(
                    message_text=(
                        f"<b>{result[1]}</b>\n\n"
                        f"Категория: {result[3]}\n"
                        f"Адрес: {result[2]}"
                    ),
                    parse_mode="HTML"
                )
            )
            articles.append(article)
            if len(articles) >= 50:
                break

        if len(articles) > 0:
            bot.answer_inline_query(query.id, articles)
        else:
            bot.answer_inline_query(query.id, [
                types.InlineQueryResultArticle(
                    id="1",
                    title="Ничего не найдено",
                    input_message_content=types.InputTextMessageContent(
                        message_text="Ничего не найдено",
                        parse_mode="HTML"
                    )
                )
            ])


@bot.callback_query_handler(func=lambda call: call.data.startswith('ik_'))
def proccessing_ik(call):
    call_data = call.data.split('_')[-1]
    u_id = call.from_user.id

    if call_data == '1':
        bot.edit_message_text(
            IK_1, u_id, call.message.message_id, reply_markup=start_text_inline())

    elif call_data == '2':
        bot.edit_message_text(
            IK_2, u_id, call.message.message_id, reply_markup=start_text_inline())

    elif call_data == '3':
        bot.edit_message_text(
            IK_3, u_id, call.message.message_id, reply_markup=start_text_inline())

    elif call_data == '4':
        bot.edit_message_text(
            IK_4, u_id, call.message.message_id, reply_markup=start_text_inline())


@bot.callback_query_handler(func=lambda call: call.data == 'menu')
def menu(call):
    bot.edit_message_text(
        START_TEXT.format(bot_name=bot.get_me().first_name),
        call.from_user.id,
        call.message.message_id,
        reply_markup=start_text_inline()
    )


if __name__ == '__main__':
    try:
        print(
            f"Бот https://t.me/{bot.get_me().username} успешно был запущен. [{datetime.now().strftime('%d.%m.%Y, %H:%M')}]")
        bot.polling(none_stop=True)

    except (SystemExit, SystemError, KeyboardInterrupt):
        print("Бот был остановлен принудительно.")
        pass
