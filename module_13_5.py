from config import TOKEN
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# Объект бота
bot = Bot(token=TOKEN)
# Диспетчер
dp = Dispatcher(bot, storage=MemoryStorage())
# Создание кнопок
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb = ReplyKeyboardMarkup(resize_keyboard=True).row(button1, button2)


# Хэндлер на команду /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


class UserState(StatesGroup):
    age = State()       # возраст
    growth = State()    # рост
    weight = State()    # вес


# Хэндлер на Calories
@dp.message_handler(text=['Рассчитать'])
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


# Хэндлер на возраст
@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(first=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


# Хэндлер на рост
@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(second=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


# Хэндлер на вес
@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(third=message.text)
    data = await state.get_data()
    calories = 10 * float(data['third']) + 6.25 * float(data['second']) - 5 * float(data['first']) + 5
    await message.answer(f'Ваша норма калорий: {calories}')
    await state.finish()


# Хэндлер на все сообщения
@dp.message_handler()
async def all_massages(message: types.Message):
    await message.answer('Введите команду /start, чтобы начать общение.')


# Запуск процесса поллинга новых апдейтов
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
