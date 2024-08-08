import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
DB_PATH = os.getenv("DB_PATH")
BASE_URL = os.getenv("BASE_URL")
DATE_FORMAT = "%d.%m.%Y"


DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("history", "Открыть историю поиска"),
    ("help", "Вывести справку"),
    ("movie_search", "Поиск фильма/сериала по названию"),
    ("movie_by_rating", "Поиск фильма/сериала по рейтингу"),
    ("low_budget_movie", "Поиск фильма/сериала с маленьким бюджетом"),
    ("high_budget_movie", "Поиск фильма/сериала с большим бюджетом")

)
