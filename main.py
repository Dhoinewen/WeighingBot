import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from helpers import from_oject_to_str, check_weight
from data import create_user, create_weighing, get_all_weighing


API_TOKEN = '5343065010:AAGqqsXGH0G2NugZxKAwJydwEy5b9o2F6qw'


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class FSMText(StatesGroup):
    weight = State()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Add waighing", "Show my stats"]
    keyboard.add(*buttons)
    registered = create_user(message.from_user.id, message.from_user.username)
    if registered is False:
        await message.answer("Already registered", reply_markup=keyboard)
    else:
        await message.answer("Successfully Registered", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Add waighing", state=None)
async def add_weighing(message: types.Message):
    await message.answer('Вкажіть вагу')
    await FSMText.weight.set()


@dp.message_handler(state=FSMText.weight)
async def save_weighing(message: types.Message, state: FSMContext):
    weight_after_check = check_weight(message.text)
    if weight_after_check is False:
        await message.reply('Неправильна вага, введіть повторно')
        return
    create_weighing(message.from_user.id, weight_after_check)
    await state.finish()
    await message.answer('Saved')


@dp.message_handler(lambda message: message.text == "Show my stats")
async def show_my_stats(message: types.Message):
    data = get_all_weighing(message.from_user.id)
    await message.answer(from_oject_to_str(data))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
