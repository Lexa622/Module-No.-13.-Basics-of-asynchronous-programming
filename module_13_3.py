import asyncio
from config import TOKEN
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command


# Объект бота
bot = Bot(token=TOKEN)
# Диспетчер
dp = Dispatcher()


# Хэндлер на команду /start
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')


# Хэндлер на все сообщения
@dp.message()
async def all_massages(message: types.Message):
    await message.answer('Введите команду /start, чтобы начать общение.')


# Запуск процесса поллинга новых апдейтов
if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
