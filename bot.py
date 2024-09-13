import telebot
from io import BytesIO
import numpy as np
from telebot import types
from googletrans import Translator
import keras
from random import randint, choice, shuffle
from random import randint, choice, shuffle
from tensorflow.keras import models
import numpy as np
from PIL import Image
import pickle
import cv2

TELEGRAM_API_TOKEN = '7532048730:AAGDuCvqvWcsGP2pddWqZSc4NqM96vY4Ncw'
bot = telebot.TeleBot(TELEGRAM_API_TOKEN)
# Стартовый набор кнопок
photo = ''
desc_text = ''


def get_users():
    global users
    f = open('users.txt', 'rt').readlines()
    users_data = {}
    for i in f:
        print(i.split('%'))
        name, desc, ph = i.split('%')
        users_data[int(name)] = [desc, ph]

    return users_data


users = get_users()
print(users)


def save_data():
    global users
    f = open('users.txt', 'wt')
    s = ''
    for i in users.items():
        name, lst = i
        s += f'{name}%{lst[0]}%{lst[1]}\n'
    f.write(s)
    f.close()


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

markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_yes = types.KeyboardButton("Да")
button_no = types.KeyboardButton("Нет")
markup3.add(button_yes, button_no)

markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_yes = types.KeyboardButton("Да")
button_no = types.KeyboardButton("Нет")
markup3.add(button_yes, button_no)

model = models.load_model('AI_CDEK.keras')

with open("vec_and_le.pkl", 'rb') as f:
    label_encoder, vectorizer = pickle.load(f)


with open("vec_and_le.pkl", 'rb') as f:
    label_encoder, vectorizer = pickle.load(f)


# Данные о товаре


# Встреча клиента
@bot.message_handler(commands=['start'])
def start_message(message):
    if message.text == '/start':
        if message.chat.id not in users:
            users[message.chat.id] = ['', '']
        if message.chat.id not in users:
            users[message.chat.id] = ['', '']
        bot.send_message(message.chat.id, f'Привет!🖐 Я бот-помощник анализа товара сайта CDEK', reply_markup=markup1)
        bot.register_next_step_handler(message, second_message)
    else:
        bot.send_message(message.chat.id, 'Запустить бота: /start')


#
def second_message(message):
    if message.text == 'Анализ товара🛒':
        bot.send_message(message.chat.id, 'Требуются описание/фото товара: ', reply_markup=markup2)

    elif message.text == 'Информация❓':
        bot.send_message(message.chat.id, info_text1)
        bot.register_next_step_handler(message, second_message)


# Нажал на кнопку анализ

@bot.message_handler(content_types=['photo'])
def get_image(message):
    global photo
    raw = message.photo[-1].file_id
    name = raw + ".jpg"
    file_info = bot.get_file(raw)
    downloaded_file = bot.download_file(file_info.file_path)
    rand_name = str(randint(1, 100000)) + choice(
        '132423rksjhfkjdkgdkfhgkjslakjlkgfhsldjglkhdslkjghlkfhskljajklg') + '.jpg'
    with open(f'uploads/{rand_name}', 'wb') as new_file:
        new_file.write(downloaded_file)
    img = open(f'uploads/{rand_name}', 'rb')
    bot.reply_to(message, "Фото загружено")
    users[message.chat.id][1] = f'uploads/{rand_name}'
    save_data()


@bot.message_handler(content_types=['text'])
def msg(message):
    global photo, desc_text
    if message.text == 'Загрузить описание':

        bot.send_message(message.chat.id, 'Введите описание товара:')

        bot.send_message(message.chat.id, 'Введите описание товара:')
    elif message.text == 'Загрузить фото':
        bot.send_message(message.chat.id, "Пришлите фото: ")  # затычка
        bot.register_next_step_handler(message, get_image)
        bot.send_message(message.chat.id, "Пришлите фото: ")  # затычка
        bot.register_next_step_handler(message, get_image)


    elif message.text == 'Доп.Информация':
        bot.send_message(message.chat.id, info_text2)


    elif message.text == 'Да':
        if not users[message.chat.id][1]:
            bot.send_message(message.chat.id, 'Фото не загружено')
        if not users[message.chat.id][0]:
            bot.send_message(message.chat.id, 'Описание товара не загружено')
        else:
            try:
                image = cv2.resize(np.array(Image.open(users[message.chat.id][1])), (128, 128))
                TEXT_DATA = [vectorizer.transform([users[message.chat.id][0]]).toarray()]

                predict = model.predict(x=[np.array([image]), TEXT_DATA])
                metka = predict.argmax(axis=-1)[0]
                label_encoder_dd = label_encoder.inverse_transform([metka])[0]

                # predict = np.sort(predict)
                # ans =label_encoder_dd[0]
                # for i in range(1, len(str(label_encoder_dd))):
                #     if label_encoder_dd[i].isupper():
                #         ans += str(' / ') + label_encoder_dd[i]
                #     else:
                #         ans += label_encoder_dd[i]

                top_10_indices = np.argsort(predict[0])[::-1][:10]

                top_10_probabilities = predict[0][top_10_indices]

                top_10_labels = label_encoder.inverse_transform(top_10_indices)
                ans = ''
                for label, probability in zip(top_10_labels, top_10_probabilities):
                    s = label[0]
                    for i in range(1, len(label)):
                        if label[i].isupper():
                            s += str(' / ') + label[i]
                        else:
                            s += label[i]
                    ans += f"{s}: {probability * 100:.2f}%\n"
                bot.send_message(message.chat.id, ans, reply_markup=markup2)
            except Exception as e:
                bot.send_message(message.chat.id, 'Ошибка, попробуйте еще!')


    elif message.text == 'Провести анализ':
        if not users[message.chat.id][1]:
            bot.send_message(message.chat.id, 'Фото не загружено')
        if not users[message.chat.id][0]:
            bot.send_message(message.chat.id, 'Описание товара не загружено')
        elif users[message.chat.id][0] and users[message.chat.id][1]:
            img = open(users[message.chat.id][1], 'rb')
            bot.send_message(message.chat.id,
                             "Описание товара: " + users[message.chat.id][0] + '\nИзображение: ')  # затычка
            bot.send_photo(message.chat.id, img)
            bot.send_message(message.chat.id,
                             "Все верно, можно провести анализ?\nЕсли нет, то пришлите нужное описание или фото",
                             reply_markup=markup3)
        # моделька
    elif message.text == 'Нет':
        bot.send_message(message.chat.id, 'Требуются описание/фото товара: ', reply_markup=markup2)
    else:
        try:
            if message.text not in ['Загрузить описание', 'Провести анализ', 'Доп.Информация', 'Анализ товара🛒',
                                    'Информация❓']:
                users[message.chat.id][0] = message.text
                save_data()
                bot.reply_to(message, 'Описание товара загружено!:')
        except Exception as e:
            bot.send_message(message.chat.id, "Ошиюка, попробуйте перезапустить бота командой /start")


bot.infinity_polling()

