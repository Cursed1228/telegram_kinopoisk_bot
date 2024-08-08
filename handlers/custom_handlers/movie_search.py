from datetime import datetime
from telebot.types import Message
from database.models import User, History
from loader import bot
from states.state import MovieInfoState
from api.movie_search_api import search_by_name
from handlers.custom_handlers.format_movie_info import _process_movie_results
from telegram_bot_pagination import InlineKeyboardPaginator, InlineKeyboardButton


@bot.message_handler(state="*", commands=["movie_search"])
def movie_search(message: Message) -> None:
    global user_id
    user_id = message.from_user.id
    if User.get_or_none(User.user_id == user_id) is None:
        bot.reply_to(message, "Вы не зарегистрированы. Напишите /start")
        return

    bot.send_message(user_id, "Введите название фильма/сериала")
    bot.set_state(message.from_user.id, MovieInfoState.name)
    with bot.retrieve_data(message.from_user.id) as data:
        data["movie_search"] = {"user_id": user_id}


@bot.message_handler(state=MovieInfoState.name)
def get_name(message: Message) -> None:
    bot.send_message(message.from_user.id, "Количество выводимых результатов")
    bot.set_state(message.from_user.id, MovieInfoState.limit)

    with bot.retrieve_data(message.from_user.id) as data:
        data["movie_search"]['name'] = message.text


@bot.message_handler(state=MovieInfoState.limit)
def get_limit(message: Message) -> None:
    global movie_info_list
    if message.text.isdigit():
        with bot.retrieve_data(message.from_user.id) as data:
            data['limit'] = message.text

            result = search_by_name(name=data["movie_search"]['name'], limit=data['limit'])
            movie_info_list= _process_movie_results(result, int(data['limit']))

        if movie_info_list:
            send_movie_page(message)
        else:
            bot.send_message(message.from_user.id, "По данному запросу результатов нету")

        bot.delete_state(message.from_user.id)

    else:
        bot.send_message(message.from_user.id, "Количество результатов вводиться цифрами")


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == 'movie')
def movie_page_callback(call):
    page = int(call.data.split('#')[1])
    bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )
    send_movie_page(call.message, page)


def send_movie_page(message, page=1):

    paginator = InlineKeyboardPaginator(
        len(movie_info_list),
        current_page=page,
        data_pattern='movie#{page}'
    )
    date = datetime.now().strftime("%d.%m.%Y %H:%M")
    new_search = History(user_id=user_id,
                         result=movie_info_list[page - 1],
                         date=date)
    new_search.save()
    bot.send_message(
        message.chat.id,
        movie_info_list[page - 1],
        reply_markup=paginator.markup,
        parse_mode='Markdown'
    )
