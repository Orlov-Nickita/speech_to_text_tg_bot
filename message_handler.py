import io

import aiogram
import speech_recognition
from aiogram.types import Message
from pydub import AudioSegment
import os

from loader import dp, bot


async def oga2wav(filename: str):
    """
    Конвертация формата файлов
    :param filename:
    :return:
    """
    new_filename = filename.replace('.oga', '.wav')
    audio = AudioSegment.from_file(filename)
    audio.export(new_filename, format='wav')
    return new_filename


async def recognize_speech(oga_filename: os.path):
    """
    Перевод голоса в текст + удаление использованных файлов
    :param oga_filename:
    :return:
    """
    wav_filename = await oga2wav(oga_filename)
    recognizer = speech_recognition.Recognizer()
    
    with speech_recognition.WavFile(wav_filename) as source:
        wav_audio = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(wav_audio, language='ru')
    except speech_recognition.exceptions.UnknownValueError:
        text = "Не удалось распознать текст из-за низкого качества записи или наличия шумов"
    
    if os.path.exists(oga_filename):
        os.remove(oga_filename)
    
    if os.path.exists(wav_filename):
        os.remove(wav_filename)
    
    return text


async def download_file(bot: aiogram.Bot, file_id: str):
    """
    Скачивание файла, который прислал пользователь
    :param bot:
    :param file_id:
    :return:
    """
    file_info: aiogram.types.File = await bot.get_file(file_id)
    downloaded_file: io.BytesIO = await bot.download_file(file_info.file_path)
    filename: str = file_id + file_info.file_path
    filename: str = filename.replace('/', '_')
    
    with open(filename, 'wb') as f:
        f.write(downloaded_file.getvalue())
    return filename


@dp.message_handler(content_types=['voice'])
async def transcript(message: Message):
    """
    Функция, отправляющая текст в ответ на голосовое
    :param message:
    """
    filename = await download_file(bot, message.voice.file_id)
    text = await recognize_speech(filename)
    await bot.send_message(message.chat.id, text)
