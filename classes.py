from datetime import date, timedelta, datetime
import sqlite_db_utlls


class User:
    _users_lst = list()

    def __init__(self, message):
        self._name = message.from_user.first_name
        self._user_id = message.from_user.id
        self._chat_id = message.chat.id
        self._settings = Settings()
        self._history = sqlite_db_utlls.get_from_db(message.from_user.id)
        self._answers = dict()
        if self not in self._users_lst:
            self._users_lst.append(self)

    @property
    def history(self):
        return self._history

    @property
    def name(self):
        return self._name

    @property
    def settings(self):
        return self._settings

    @property
    def answers(self):
        return self._answers

    @answers.setter
    def answers(self, dct: dict):
        self._answers = dct

    @property
    def chat_id(self):
        return self._chat_id

    def add_history(self, hotels_lst):
        self._history.update({str(datetime.now()): [self.answers, hotels_lst]})
        sqlite_db_utlls.insert_to_db(self._user_id, self.history)

    @classmethod
    def users(cls):
        return cls._users_lst


class Settings:

    def __init__(self):
        self._adults = '1'
        self._check_in, self._check_out = today_and_tomorrow()

    @property
    def adults(self):
        return self._adults

    @adults.setter
    def adults(self, number: str):
        self._adults = number

    @property
    def check_in(self):
        return self._check_in

    @check_in.setter
    def check_in(self, date_in: str):
        self._check_in = date_in

    @property
    def check_out(self):
        return self._check_out

    @check_out.setter
    def check_out(self, date_out: str):
        self._check_out = date_out


def today_and_tomorrow() -> tuple:
    today = date.today()
    return str(today), str(today + timedelta(days=1))


def get_user_by_message(message):
    for i_user in User.users():
        if i_user.chat_id == message.chat.id:
            return i_user
    return User(message)

# TODO Сохранять пользователей в дб,
