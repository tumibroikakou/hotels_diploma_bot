from bot_loader import bot
import classes
import keyboards
from simply_logging import logger

from telebot import types, handler_backends


@logger
def setup_settings(message: types.Message) -> handler_backends.MemoryHandlerBackend:
    user = classes.get_user_by_message(message)
    bot.send_message(user.chat_id, f'Текущие настройки:\nДата заезда: {user.settings.check_in}'
                                   f'\nДата выезда: {user.settings.check_out}'
                                   f'\nКоличество гостей: {user.settings.adults}')
    bot.send_message(user.chat_id, 'Поменять настройки? (Да/Нет)', reply_markup=keyboards.yes_no)
    return bot.register_next_step_handler_by_chat_id(user.chat_id, ask_all, user)


@logger
def ask_all(message: types.Message, user: classes.User) -> handler_backends.MemoryHandlerBackend:
    tmp_answer = message.text.lower()
    if tmp_answer not in ['lf', 'ytn', 'yes', 'no', 'да', 'нет']:
        bot.reply_to(message, 'Некорректный ответ, возврат\nПоменять настройки? (Да/Нет)')
        return bot.register_next_step_handler_by_chat_id(user.chat_id, ask_all, user)
    if tmp_answer in ['lf', 'yes', 'да']:
        bot.send_message(message.chat.id, 'Введите дату заезда, выезда, и кол-во гостей через пробел'
                                          '\n(формат "гггг-мм-дд гггг-мм-дд 1"):')
        return bot.register_next_step_handler_by_chat_id(user.chat_id, set_all, user)


@logger
def set_all(message: types.Message, user: classes.User) -> None:
    user.settings.check_in, user.settings.check_out, user.settings.adults = message.text.lower().split()
    bot.send_message(user.chat_id, f'Сохранено!\nТекущие настройки:\nДата заезда: {user.settings.check_in}'
                                   f'\nДата выезда: {user.settings.check_out}'
                                   f'\nКоличество гостей: {user.settings.adults}')

# TODO Собрал наскоро, переделать с календарём, ну когда-нибудь...
