from bot_loader import bot

from telebot import types


def help_message(message: types.Message):
    bot.send_message(message.chat.id, """
/lowprice - Отели с сортировкой по цене от низкой к высокой
/highprice - Отели с сортировкой по цене от высокой к низкой
/bestdeal - Отели с заданным растоянием от центра
/settings - Настройки бота
/history - История запросов
/help - Показать список команд""")
