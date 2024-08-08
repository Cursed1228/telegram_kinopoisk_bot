from telebot.types import Message
from telegram_bot_pagination import InlineKeyboardPaginator, InlineKeyboardButton
from database.models import User, History, create_models
from loader import bot


all_result_dict = dict()


@bot.message_handler(state="*", commands=["history"])
def handle_history(message: Message) -> None:
    global all_result_dict
    all_result_dict = dict()
    user_id = message.from_user.id
    user = User.get_or_none(User.user_id == user_id)
    if user is None:
        bot.reply_to(message, "Вы не зарегистрированы. Напишите /start")
        return

    requests = History.select().where(History.user_id == user_id)
    if requests:
        for request in requests:
            all_result_dict[request.result] = {'movie_id': request.movie_id, 'is_watching': request.is_watching}

        send_movie_page(message)
    else:
        bot.send_message(message.from_user.id, "Ваша история запросов пуста")


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == 'history')
def movie_page_callback(call):
    page = int(call.data.split('#')[1])
    print(call.data.split('#'))
    bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )
    send_movie_page(call.message, page)


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == 'watched')
def mark_as_watched_callback(call):
    movie_id = int(call.data.split('#')[1])
    user_id = call.from_user.id
    history = History.get(History.user_id == user_id, History.movie_id == movie_id)
    history.is_watching = True
    history.save()

    for key, value in all_result_dict.items():
        if value['movie_id'] == movie_id:
            value['is_watching'] = True
            break

    bot.answer_callback_query(call.id, "Фильм отмечен как просмотренный")
    bot.delete_message(call.message.chat.id, call.message.message_id)
    send_movie_page(call.message)


def send_movie_page(message, page=1):
    paginator = InlineKeyboardPaginator(
        len(all_result_dict.keys()),
        current_page=page,
        data_pattern='history#{page}'
    )

    current_movie = list(all_result_dict.keys())[page - 1]
    movie_info = all_result_dict[current_movie]
    movie_id = movie_info['movie_id']
    is_watching = movie_info['is_watching']

    if not is_watching:
        paginator.add_before(InlineKeyboardButton('Mark as Watched', callback_data=f'watched#{movie_id}'))

    bot.send_message(
        message.chat.id,
        f"{current_movie}\nСтатус: {'Просмотрено' if is_watching else 'Не просмотрено'}",
        reply_markup=paginator.markup,
        parse_mode='Markdown'
    )
