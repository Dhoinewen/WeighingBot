import logging


from model import User, session
from aiogram import Bot, Dispatcher, executor, types
from helpers import from_oject_to_str


API_TOKEN = '5343065010:AAGqqsXGH0G2NugZxKAwJydwEy5b9o2F6qw'


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["С пюрешкой", "Без пюрешки"]
    keyboard.add(*buttons)
    await message.answer("Hi!\nI'm EchoBot!\nPowered by aiogram." , reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Без пюрешки")
async def without_puree(message: types.Message):
    print(types.base.TelegramObject.)
    user = session.query(User).filter(User.id == 1).first()
    text = from_oject_to_str(user)
    await message.answer(text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
