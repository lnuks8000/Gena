# main.py
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os

from handlers import weather

# Загружаем переменные окружения из .env
load_dotenv()

# Получаем токен бота из .env
BOT_TOKEN = '7736461947:AAFoX5n2akwdFgKPKxvGl-7_rp73tFFQUKA'

# Создаём экземпляры бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Регистрируем роутер с обработчиками погоды
dp.include_router(weather.router)

# Функция запуска бота
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

# Точка входа
if __name__ == "__main__":
    asyncio.run(main())
