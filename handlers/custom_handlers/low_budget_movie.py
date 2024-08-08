from datetime import datetime

from telebot.types import Message
from database.models import User, History, create_models
from loader import bot
from states.state import MovieLowBudgetState
from api.low_budget_movie_api import low_budget_movie
from api.genre_check import check_genre, create_genres_txt
from telegram_bot_pagination import InlineKeyboardPaginator
from handlers.custom_handlers.format_movie_info import _process_movie_results



@bot.message_handler(state="*", commands=["low_budget_movie"])
def search_by_rating(message: Message) -> None:
    global user_id
    user_id = message.from_user.id
    if User.get_or_none(User.user_id == user_id) is None:
        bot.reply_to(message, "Вы не зарегистрированы. Напишите /start")
        return

    genres = create_genres_txt()
    bot.send_message(message.from_user.id, f'Выберите жанр фильма/сериала \nСписок доступных жанров:\n{genres} ')
    bot.set_state(message.from_user.id, MovieLowBudgetState.genre)
    with bot.retrieve_data(message.from_user.id) as data:
        data["movie_low_budget"] = {"user_id": user_id}


@bot.message_handler(state=MovieLowBudgetState.genre)
def get_rating(message: Message) -> None:
    if message.text.lower() != 'нет' and check_genre(message.text.lower()):
        with bot.retrieve_data(message.from_user.id) as data:
            data["movie_low_budget"]['genre'] = message.text.lower()
        bot.send_message(message.from_user.id, "Количество выводимых результатов")
        bot.set_state(message.from_user.id, MovieLowBudgetState.limit)

    else:
        bot.send_message(message.from_user.id, "Такого жанра нет в базе или совершенна ошибка в вводе!"
                                               "\nПопробуйте ещё раз")


@bot.message_handler(state=MovieLowBudgetState.limit)
def get_limit_1(message: Message) -> None:
    global low_budget_info_list
    if message.text.isdigit():
        with bot.retrieve_data(message.from_user.id) as data:
            data["movie_low_budget"]['limit'] = message.text

            result = low_budget_movie(limit=data["movie_low_budget"]['limit'],
                                      genre=data["movie_low_budget"]['genre'])

            low_budget_info_list = _process_movie_results(result, int(data["movie_low_budget"]['limit']))
            data["movie_low_budget"]['result'] = low_budget_info_list

        if low_budget_info_list:
            send_movie_page(message)
        else:
            bot.send_message(message.from_user.id, "По данному запросу результатов нету")

    else:
        bot.send_message(message.from_user.id, "Количество результатов вводиться цифрами. Попробуйте ещё раз")


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == 'low_movie')
def movie_page_callback(call):
    page = int(call.data.split('#')[1])
    bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )
    send_movie_page(call.message, page)


def send_movie_page(message, page=1):
    paginator = InlineKeyboardPaginator(
        len(low_budget_info_list),
        current_page=page,
        data_pattern='low_movie#{page}'
    )

    bot.send_message(
        message.chat.id,
        low_budget_info_list[page - 1],
        reply_markup=paginator.markup,
        parse_mode='Markdown'
    )

    date = datetime.now().strftime("%d.%m.%Y %H:%M")
    new_search = History(user_id=user_id,
                         result=low_budget_info_list[page - 1],
                         date=date)
    new_search.save()