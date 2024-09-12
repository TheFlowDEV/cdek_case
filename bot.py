import logging
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import filters
from aiogram.utils import executor

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Токен вашего бота
TELEGRAM_API_TOKEN = '7532048730:AAGDuCvqvWcsGP2pddWqZSc4NqM96vY4Ncw'
bot = Bot(token=TELEGRAM_API_TOKEN)
dp = Dispatcher(bot)

info_text = 'Бот был разработан командой Kodiki на Хакатоне-ТПУ 11.09.2024'


# Вступление, две кнопки: инфо + анализ
@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    await message.answer("Привет ✌️")
    markup = types.InlineKeyboardMarkup()
    button_promt_analyse = types.InlineKeyboardButton('Проанализировать товар', callback_data='analyse_of_data')
    button_info = types.InlineKeyboardButton('Информация о боте', callback_data='info')
    markup.add(button_promt_analyse, button_info)
    await message.answer("Выберите опцию:", reply_markup=markup)


# Получение запроса (данных о товаре)
@dp.message_handler(commands=['text'])
async def get_data(message: types.Message):
    await message.answer('Пришлите описание, фотографии товара: ')


# Вывод сообщений
@dp.callback_query_handler(lambda call: True)
async def callback_worker(call: types.CallbackQuery):
    if call.data == 'analyse_of_data':
        await call.answer()  # Удаляем уведомление о нажатии кнопки
        await call.message.delete()  # Удаляем предыдущее сообщение
        await call.message.answer('сработал')  # Здесь можно добавить логику анализа товара
    elif call.data == 'info':
        await call.answer()  # Удаляем уведомление о нажатии кнопки
        await call.message.delete()  # Удаляем предыдущее сообщение
        await call.message.answer(info_text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)