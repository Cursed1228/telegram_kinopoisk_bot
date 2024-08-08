from telebot.handler_backends import State, StatesGroup


class MovieRatingInfoState(StatesGroup):
    name = State()
    genre = State()
    rating = State()
    limit = State()
