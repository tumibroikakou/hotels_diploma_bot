import classes
import keyboards
from bot_loader import bot
from handlers import user_chat
from simply_logging import logger

from telebot import types, handler_backends
from typing import Callable


@logger
def show_entries(message: types.Message) -> handler_backends.MemoryHandlerBackend:
    user = classes.get_user_by_message(message)
    if not user.history:
        return bot.send_message(user.chat_id, f'{user.name}, ещё нет истории!')
    bot.send_message(
        user.chat_id, '\n'.join([str(i) + '. ' + key for i, key in enumerate(user.history.keys(), 1)]),
        reply_markup=keyboards.history_kbd(len(user.history.keys()))
    )
    return bot.register_next_step_handler_by_chat_id(user.chat_id, call_history, user)


@logger
def call_history(message: types.Message, user: classes.User) -> Callable:
    for i, val in enumerate(user.history.values(), 1):
        if i == int(message.text):
            user.answers = val[0]
            return user_chat.send_to_user(message, user, val[1])
