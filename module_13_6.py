from config import TOKEN
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Объект бота
bot = Bot(token=TOKEN)
# Диспетчер
dp = Dispatcher(bot, storage=MemoryStorage())
# Создание кнопок
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb = ReplyKeyboardMarkup(resize_keyboard=True).row(button1, button2)

button3 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button4 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb2 = InlineKeyboardMarkup(resize_keyboard=True).add(button3, button4)


class UserState(StatesGroup):
    age = State()       # возраст
    growth = State()    # рост
    weight = State()    # вес


# Хэндлер на команду /start
@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


# Хэндлер на команду Рассчитать
@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb2)


# Хэндлер на команду formulas
@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()


# Хэндлер на Calories
@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
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
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


# Запуск процесса поллинга новых апдейтов
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
