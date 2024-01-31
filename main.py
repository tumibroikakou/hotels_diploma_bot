from bot_loader import bot
from handlers import lowprice, highprice, settings, bestdeal, history, help
import sqlite_db_utlls


def register_handlers() -> None:
    bot.register_message_handler(lowprice.low_price, commands='lowprice')
    bot.register_message_handler(highprice.high_price, commands='highprice')
    bot.register_message_handler(settings.setup_settings, commands='settings')
    bot.register_message_handler(bestdeal.best_deal, commands='bestdeal')
    bot.register_message_handler(history.show_entries, commands='history')
    bot.register_message_handler(help.help_message, commands=['start', 'help'])


if __name__ == '__main__':
    sqlite_db_utlls.db_create()
    register_handlers()
    bot.infinity_polling(skip_pending=True)
