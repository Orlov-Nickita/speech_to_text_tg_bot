"""
Модуль с некоторыми данными, хранящимися в переменных
"""

import os

from aiogram.contrib.middlewares.logging import LoggingMiddleware
from dotenv import load_dotenv
from aiogram import Bot
from aiogram.dispatcher import Dispatcher

load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
