from telebot import types

yes_no = types.ReplyKeyboardMarkup(True, True)
btn1 = types.KeyboardButton('Да')
btn2 = types.KeyboardButton('Нет')
yes_no.add(btn1, btn2)


def url_key(url: str) -> types.InlineKeyboardMarkup:
    url_btn = types.InlineKeyboardButton("Страничка отеля на Hotels.com", url)
    kbd = types.InlineKeyboardMarkup()
    kbd.add(url_btn)
    return kbd


def images_album(lst: list, text: str, url: str) -> list[types.InputMediaPhoto]:
    first = True
    album_lst = list()
    message = f'{text}\n<a href="{url}">Страничка отеля на Hotels.com</a>'
    for i in lst:
        if first:
            album_lst.append(types.InputMediaPhoto(i, caption=message, parse_mode='HTML'))
            first = False
        else:
            album_lst.append(types.InputMediaPhoto(i))
    return album_lst


def history_kbd(num: int) -> types.ReplyKeyboardMarkup:
    kbd = types.ReplyKeyboardMarkup(True, True)
    buttons = [types.KeyboardButton(str(i)) for i in range(1, num + 1)]
    for i_btn in buttons:
        kbd.add(i_btn)
    return kbd
