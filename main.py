from loader import bot
import handlers  # noqa
from utils.set_bot_commands import set_default_commands
from database.models import create_models
from telebot.custom_filters import StateFilter


if __name__ == "__main__":
    bot.add_custom_filter(StateFilter(bot))
    create_models()
    set_default_commands(bot)
    bot.infinity_polling()

