from datetime import datetime
from telebot.types import Message
from database.models import User, History, create_models
from loader import bot
from states.state import MovieRatingState
from api.movie_by_rating_api import rating_search_movie
from api.genre_check import check_genre, create_genres_txt
from telegram_bot_pagination import InlineKeyboardPaginator
from handlers.custom_handlers.format_movie_info import _process_movie_results


@bot.message_handler(state="*", commands=["movie_by_rating"])
def search_by_rating(message: Message) -> None:
    global user_id
    user_id = message.from_user.id
    if User.get_or_none(User.user_id == user_id) is None:
        bot.reply_to(message, "Вы не зарегистрированы. Напишите /start")
        return

    bot.send_message(user_id, "Введите рейтинг фильма/сериала (1,2 или 5-9)")
    bot.set_state(message.from_user.id, MovieRatingState.rating)
    with bot.retrieve_data(message.from_user.id) as data:
        data["movie_by_rating"] = {"user_id": user_id}


@bot.message_handler(state=MovieRatingState.rating)
def get_rating(message: Message) -> None:
    genres = create_genres_txt()
    bot.send_message(message.from_user.id, f'Выберите жанр фильма/сериала \nСписок доступных жанров:\n{genres} ')
    bot.set_state(message.from_user.id, MovieRatingState.genre)

    with bot.retrieve_data(message.from_user.id) as data:
        data["movie_by_rating"]['rating'] = message.text


@bot.message_handler(state=MovieRatingState.genre)
def get_rating(message: Message) -> None:

    if message.text.lower() != 'нет' and check_genre(message.text):
        with bot.retrieve_data(message.from_user.id) as data:
            data["movie_by_rating"]['genre'] = message.text.lower()
        bot.send_message(message.from_user.id, "Количество выводимых результатов")
        bot.set_state(message.from_user.id, MovieRatingState.limit)

    else:
        bot.send_message(message.from_user.id, "Такого жанра нет в базе или совершенна ошибка в вводе!"
                                               "\nПопробуйте ещё раз")


@bot.message_handler(state=MovieRatingState.limit)
def get_limit_1(message: Message) -> None:
    global movie_by_rating_info
    if message.text.isdigit():
        with bot.retrieve_data(message.from_user.id) as data:
            data["movie_by_rating"]['limit'] = message.text

            result = rating_search_movie(rating=data['movie_by_rating']['rating'],
                                         limit=data["movie_by_rating"]['limit'],
                                         genre=data["movie_by_rating"]['genre'])

            movie_by_rating_info = _process_movie_results(result, int(data["movie_by_rating"]['limit']))
            data["movie_by_rating"]['result'] = movie_by_rating_info
            print(movie_by_rating_info)
        if movie_by_rating_info:
            send_movie_page(message)
        else:
            bot.send_message(message.from_user.id, "По данному запросу результатов нету")

    else:
        bot.send_message(message.from_user.id, "Количество результатов вводиться цифрами. Попробуйте ещё раз")


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == 'rating_movie')
def movie_page_callback(call):
    page = int(call.data.split('#')[1])
    bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )
    send_movie_page(call.message, page)


def send_movie_page(message, page=1):
    paginator = InlineKeyboardPaginator(
        len(movie_by_rating_info),
        current_page=page,
        data_pattern='rating_movie#{page}'
    )

    bot.send_message(
        message.chat.id,
        movie_by_rating_info[page - 1],
        reply_markup=paginator.markup,
        parse_mode='Markdown'
    )

    date = datetime.now().strftime("%d.%m.%Y %H:%M")
    new_search = History(user_id=user_id,
                         result=movie_by_rating_info[page - 1],
                         date=date)
    new_search.save()