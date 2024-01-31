import classes
from bot_loader import bot
from handlers.user_chat import start_chat
from simply_logging import logger

from telebot import types, handler_backends


@logger
def best_deal(message: types.Message) -> handler_backends.MemoryHandlerBackend:
    user = classes.get_user_by_message(message)
    user.answers['sort_by'] = 'DISTANCE_FROM_LANDMARK'
    bot.send_message(message.chat.id, f'{user.name}, введите диапазон цен\n(формат 1000-6000):')
    return bot.register_next_step_handler_by_chat_id(user.chat_id, price_fork, user)


@logger
def price_fork(message: types.Message, user: classes.User) -> handler_backends.MemoryHandlerBackend:
    tmp_answer = message.text.split('-')[:2]
    if len(tmp_answer) < 2 or not all([i.isdigit() for i in tmp_answer]):
        bot.reply_to(message, 'Некорректный ответ! Введите диапазон цен\n(формат 1000-6000):')
        return bot.register_next_step_handler_by_chat_id(user.chat_id, price_fork, user)
    user.answers['price_min'], user.answers['price_max'] = tmp_answer
    bot.send_message(message.chat.id, f'{user.name}, введите максимальное расстояние от центра города'
                                      f'\n(в километрах):')
    return bot.register_next_step_handler_by_chat_id(user.chat_id, distance_from, user)


@logger
def distance_from(message: types.Message, user: classes.User) -> handler_backends.MemoryHandlerBackend:
    if not message.text.isdigit():
        bot.reply_to(message, 'Некорректный ответ! Введите максимальное расстояние от центра города'
                              '\n(в километрах):')
        return bot.register_next_step_handler_by_chat_id(user.chat_id, distance_from, user)
    user.answers['max_distance'] = message.text
    return start_chat(message)
