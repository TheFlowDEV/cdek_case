import telebot
from io import BytesIO
import numpy as np
from telebot import types
from googletrans import Translator
import keras
from tensorflow.keras import models
import numpy as np
from PIL import Image
import pickle
import cv2

TELEGRAM_API_TOKEN = '7532048730:AAGDuCvqvWcsGP2pddWqZSc4NqM96vY4Ncw'
bot = telebot.TeleBot(TELEGRAM_API_TOKEN)
# Стартовый набор кнопок
info_text1 = f'Бот был разработан командой Kodiki на Хакатоне-ТПУ 11-13.09.2024❤️'
markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_analyse_product = types.InlineKeyboardButton('Анализ товара🛒')
button_info1 = types.InlineKeyboardButton('Информация❓')
markup1.add(button_analyse_product, button_info1)
# Набор кнопок основного рабочего поля
info_text2 = 'Для более детального анализа вашего товара потребуются И фотографии, И описание.'
markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_get_desc = types.KeyboardButton("Загрузить описание")
button_get_photo = types.KeyboardButton("Загрузить фото")
button_analyse = types.KeyboardButton("Провести анализ")
button_info2 = types.KeyboardButton("Доп.Информация")
markup2.add(button_get_desc, button_get_photo, button_analyse, button_info2)

model = models.load_model('AI_CDEK.keras')

# Данные о товаре
product_desc = ''


# Встреча клиента
@bot.message_handler(commands=['start'])
def start_message(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, f'Привет!🖐 Я бот-помощник анализа товара сайта CDEK', reply_markup=markup1)
        bot.register_next_step_handler(message, second_message)
    else:
        bot.send_message(message.chat.id, 'Запустить бота: /start')


#
def second_message(message):
    if message.text == 'Анализ товара🛒':
        bot.send_message(message.chat.id, 'Требуются описание/фото товара: ', reply_markup=markup2)
        bot.register_next_step_handler(message, third_message)

    elif message.text == 'Информация❓':
        bot.send_message(message.chat.id, info_text1)
        bot.register_next_step_handler(message, second_message)


# Нажал на кнопку анализ
def third_message(message):
    if message.text == 'Загрузить описание':
        cid = message.chat.id
        msg = message
        bot.send_message(cid, 'Введите описание товара:')

        @bot.message_handler(commands=['text'])
        def record_desc(message):
            product_desc = message.text
            bot.reply_to(message, 'Описание записано.')

        bot.register_next_step_handler(msg, third_message)
    elif message.text == 'Загрузить фото':
        bot.send_message(message.chat.id, "Пришлите фото: ")
        bot.register_next_step_handler(message, third_message)  # затычка


    elif message.text == 'Провести анализ':  # & (product[] != '' |[]): #хз хз
        bot.send_message(message.chat.id, "Начинаем анализ..........")
        ####################################################
        #                                                  #
        #                 Работка для ИИ                   #
        #                                                  #
        ####################################################
        bot.register_next_step_handler(message, third_message)


    elif message.text == 'Доп.Информация':
        bot.send_message(message.chat.id, info_text2)
        bot.register_next_step_handler(message, third_message)

    else:
        bot.send_message(message.chat.id, 'Неверный запрос!')
        bot.register_next_step_handler(message, third_message)


bot.infinity_polling()