from bot_loader import bot
import rapid_api
import keyboards
import classes
from simply_logging import logger

from telebot import types, handler_backends
from typing import Callable, Optional


@logger
def start_chat(message: types.Message) -> handler_backends.MemoryHandlerBackend:
    user = classes.get_user_by_message(message)
    bot.send_message(message.chat.id, f'{user.name} введите город, где будет проводиться поиск:')
    return bot.register_next_step_handler_by_chat_id(message.chat.id, ask_city, user)


@logger
def ask_city(message: types.Message, user: classes.User) -> handler_backends.MemoryHandlerBackend:
    user.answers['city'] = message.text
    bot.send_message(message.chat.id,
                     'Введите количество отелей, которые необходимо вывести в результате (не более 7):'
                     )
    return bot.register_next_step_handler_by_chat_id(message.chat.id, number_of_hotels, user)


@logger
def number_of_hotels(message: types.Message, user: classes.User) -> handler_backends.MemoryHandlerBackend:
    tmp_answer = message.text
    if tmp_answer not in [str(i) for i in range(8)]:  # 11 <= int(message.text) < 0 TODO Упростить выражение, мб.
        bot.reply_to(message, 'Пожалуйста введите число, оно должно быть не больше 7:')
        return bot.register_next_step_handler_by_chat_id(message.chat.id, number_of_hotels, user)
    user.answers['number_of_hotels'] = tmp_answer
    bot.send_message(message.chat.id, 'Загружать картинки? (Да/Нет)', reply_markup=keyboards.yes_no)
    return bot.register_next_step_handler_by_chat_id(message.chat.id, load_pictures, user)


@logger
def load_pictures(message: types.Message, user: classes.User) -> Optional[Callable]:
    tmp_answer = message.text.lower()
    if tmp_answer not in ['lf', 'ytn', 'yes', 'no', 'да', 'нет']:
        bot.reply_to(message, 'Некорректный ответ, возврат\nЗагружать картинки? (Да/Нет)')
        return bot.register_next_step_handler_by_chat_id(message.chat.id, load_pictures, user)
    user.answers['load_pictures'] = True if tmp_answer in ['lf', 'yes', 'да'] else False
    if user.answers.get('load_pictures'):
        bot.send_message(message.chat.id, 'Введите количество картинок (максимум четыре):')
        return bot.register_next_step_handler_by_chat_id(message.chat.id, number_of_pictures, user)
    return gathering_complete(message, user)


@logger
def number_of_pictures(message: types.Message, user:classes.User) -> Optional[Callable]:
    tmp_answer = message.text
    if tmp_answer not in [str(i) for i in range(1, 5)]:  # TODO Упростить выражение, мб.
        bot.reply_to(message, 'Пожалуйста введите число, оно должно быть не больше четырёх:')
        return bot.register_next_step_handler_by_chat_id(message.chat.id, number_of_pictures, user)
    user.answers['number_of_pictures'] = tmp_answer
    return gathering_complete(message, user)


def gathering_complete(message: types.Message, user: classes.User) -> Optional[Callable]:
    try:
        hotels_lst = rapid_api.get_hotels(user)
    except (IndexError, ValueError) as e:
        bot.send_message(message.chat.id, 'Произошла невиданная доселе ошибка! Жуть!\n' + str(e))
        logger(rapid_api.get_hotels(user))
    else:
        user.add_history(hotels_lst)
        return send_to_user(message, user, hotels_lst)


@logger
def send_to_user(message: types.Message, user: classes.User, hotels_lst: list) -> None:
    if not hotels_lst:
        return bot.send_message(message.chat.id, f'{user.name}, по вашему запросу отелей не найдено. '
                                                 f'Отправьте новую команду или воспользуйтесь помощью /help')
    for i_hotel in hotels_lst:
        msg = f"{i_hotel['name']}\n{i_hotel['address']}\nТекущая цена: {i_hotel['price']}"
        if i_hotel.get('total_price'):
            msg += f'\n{i_hotel["total_price"]}'
        if user.answers.get('load_pictures'):
            bot.send_media_group(message.chat.id, keyboards.images_album(i_hotel['images'], msg, i_hotel['url']),
                                 disable_notification=True)
        else:
            bot.send_message(message.chat.id, msg, reply_markup=keyboards.url_key(i_hotel.get('url')),
                             disable_notification=True)
    bot.send_message(message.chat.id, f'{user.name}, это отели по вашему запросу. '
                                      f'Отправьте новую команду или воспользуйтесь помощью /help')
