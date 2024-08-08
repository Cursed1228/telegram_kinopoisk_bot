from telebot.handler_backends import State, StatesGroup


class UserState(StatesGroup):
    new_task_title = State()
    new_task_due_date = State()
    tasks_make_done = State()


class MovieInfoState(StatesGroup):
    name = State()
    genre = State()
    rating = State()
    limit = State()
    paginator = State()


class MovieRatingState(StatesGroup):
    name = State()
    genre = State()
    rating = State()
    limit = State()


class MovieLowBudgetState(StatesGroup):
    name = State()
    genre = State()
    rating = State()
    limit = State()


class MovieHighBudgetState(StatesGroup):
    name = State()
    genre = State()
    rating = State()
    limit = State()
