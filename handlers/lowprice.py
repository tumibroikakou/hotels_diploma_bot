import classes
from handlers.user_chat import start_chat
from simply_logging import logger

from telebot import types
from typing import Callable


@logger
def low_price(message: types.Message) -> Callable:
    user = classes.get_user_by_message(message)
    user.answers['sort_by'] = 'PRICE'
    return start_chat(message)
