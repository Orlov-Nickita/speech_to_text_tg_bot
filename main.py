"""
Модуль отвечающий за запуск программы. Пусковой файл
"""

from message_handler import *
from aiogram.utils import executor

if __name__ == '__main__':
    print('ok')
    
    executor.start_polling(dispatcher=dp)
