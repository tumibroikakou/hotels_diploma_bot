import telebot
from decouple import config

bot = telebot.TeleBot(config('bot_token'))
