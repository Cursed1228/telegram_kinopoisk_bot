from telebot.types import Message
from database.models import User, History, create_models
from loader import bot
from peewee import IntegrityError


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    try:
        User.create(
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        bot.reply_to(message, f"Добро пожаловать в сервис по поиску фильмов или сериалов."
                              f"\nДля продолжения работы введите '\help' и выберите интересующий вас формат поиска")
    except IntegrityError:
        bot.reply_to(message, f"Рад вас снова видеть {first_name}")
