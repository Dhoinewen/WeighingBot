import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from helpers import from_object_to_str, check_weight, read_token, weighing_was_today
from data import create_user, create_weighing, get_all_weighing


API_TOKEN = read_token('bot_token.txt')


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


class FSMText(StatesGroup):
    weight = State()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Add weighing", "Show my stats", "Stop"]
    keyboard.add(*buttons)
    registered = create_user(message.from_user.id, message.from_user.username)
    if registered is False:
        await message.answer("Already registered", reply_markup=keyboard)
    else:
        await message.answer("Successfully Registered", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Add weighing", state='*')
async def add_weighing(message: types.Message):
    if weighing_was_today() is False:
        await message.answer('Only 1 weighing per day')
        return
    await message.answer('Enter weight')
    await FSMText.weight.set()


@dp.message_handler(lambda message: message.text == "Stop", state='*')
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Cancel")


@dp.message_handler(state=FSMText.weight)
async def save_weighing(message: types.Message, state: FSMContext):
    weight_after_check = check_weight(message.text)
    if weight_after_check is False:
        await message.reply('Invalid format, re-enter data')
        return
    await state.update_data(enter_weight=weight_after_check)
    create_weighing(message.from_user.id, weight_after_check)
    await state.finish()
    await message.answer('Saved')


@dp.message_handler(lambda message: message.text == "Show my stats")
async def show_my_stats(message: types.Message):
    data = get_all_weighing(message.from_user.id)
    await message.answer(from_object_to_str(data))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
