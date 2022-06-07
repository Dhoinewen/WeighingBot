import logging

from data import create_user, create_weighing
from aiogram import Bot, Dispatcher, executor, types
from helpers import from_oject_to_str


API_TOKEN = '5343065010:AAGqqsXGH0G2NugZxKAwJydwEy5b9o2F6qw'


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Додати зважування", "2"]
    keyboard.add(*buttons)
    registered = create_user(message.from_user.id, message.from_user.username)
    if registered is False:
        await message.answer("Already registered", reply_markup=keyboard)
    else:
        await message.answer("Successfully Registered", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Додати зважування")
async def without_puree(message: types.Message):
    try:
        text = message.reply_to_message.text # if replied
    except AttributeError:
        text = 'not replied'
    print(text)
    await message.answer('Вкажіть вагу')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
