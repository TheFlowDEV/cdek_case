import telebot
from io import BytesIO
import numpy as np
from telebot import types
import translater as tr
import emoji # для оформления


info_text = 'Бот был разработан командой Kodiki на Хакатоне-ТПУ 11.09.2024'
TELEGRAM_API_TOKEN = '7532048730:AAGDuCvqvWcsGP2pddWqZSc4NqM96vY4Ncw'
bot = telebot.TeleBot(TELEGRAM_API_TOKEN)

# Вступление, две кнопки: инфо + анализ
@bot.message_handler(commands=['start'])
def start_bot(message):
    if message.text=='/start':
        markup = types.InlineKeyboardMarkup()
        # Кнопка анализа товара
        button_promt_analyse = types.InlineKeyboardButton('Проанализировать товар', callback_data = 'analyse_of_data')
        # Кнопка информации о создателях
        button_info = types.InlineKeyboardButton('Информация о боте', callback_data = 'info')
        markup.add(button_promt_analyse)
        markup.add(button_info)
    else:
        bot.send_message(message.chat.id,f'Запустите бота командой /start')

# Получение данных о товаре(запроса)
@bot.message_handler(commands=['text'])
def get_data(message):
    bot.send_message(message.chat.id, text = 'Пришлите описание, фотографию товара: ')
    promt_desc = tr.client_promt(message.text) # Описание товара с переводом на en
    promt_view = message.photo                 # Фотография товара
    return [promt_desc, promt_view]

# Вывод сообщений
@bot.callback_query_handler(func= lambda call: True)
def callback_worker(call):
    if call.data == 'analyse_of_data':
        bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.id)
        bot.send_message(call.message.chat.id, f'сработал')
    elif call.data == 'info':
        bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.id)
        bot.send_message(call.message.chat.id, info_text)        

# if __name__ == "__main__":
#     main()