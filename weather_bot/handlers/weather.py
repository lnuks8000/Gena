# handlers/weather.py

from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from utils.weather_api import get_weather
from utils.file_manager import save_to_csv
from utils.media_sender import send_weather_media

router = Router()

# Список городов России
cities = [
    "Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань",
    "Нижний Новгород", "Самара", "Ростов-на-Дону", "Уфа", "Краснодар"
]

# Создаём клавиатуру из городов
def get_city_keyboard():
    buttons = [InlineKeyboardButton(text=city, callback_data=f"weather_{city}") for city in cities]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        buttons[i:i+2] for i in range(0, len(buttons), 2)
    ])
    return keyboard

# Команда /start — показывает меню
@router.message(F.text.lower() == "/start")
async def start_handler(message: Message):
    await message.answer(
        "Привет! 🌤 Выбери город из списка или введи название вручную:",
        reply_markup=get_city_keyboard()
    )

# Обработка выбора города из меню
@router.callback_query(F.data.startswith("weather_"))
async def handle_city_callback(callback: CallbackQuery):
    city = callback.data.replace("weather_", "")

    await callback.answer()  # Закрываем "часики"

    # Получаем данные погоды
    weather_data = await get_weather(city)

    if weather_data is None:
        await callback.message.answer("❌ Не удалось получить данные о погоде.")
        return

    # Формируем ответ
    response = (
        f"🌆 Город: {city}\n"
        f"🌡 Температура: {weather_data['temp']}°C\n"
        f"💧 Влажность: {weather_data['humidity']}%\n"
        f"☔ Осадки: {weather_data['description']}"
    )

    await callback.message.answer(response)

    # Сохраняем в CSV
    save_to_csv(city, weather_data)

    # Отправляем медиа
    await send_weather_media(callback.message, weather_data)

# Обработка произвольного текста — пользователь ввёл город сам
@router.message(F.text)
async def handle_weather(message: Message):
    city = message.text.strip()

    weather_data = await get_weather(city)

    if weather_data is None:
        await message.answer("❌ Не удалось получить данные о погоде. Проверьте название города.")
        return

    response = (
        f"🌆 Город: {city}\n"
        f"🌡 Температура: {weather_data['temp']}°C\n"
        f"💧 Влажность: {weather_data['humidity']}%\n"
        f"☔ Осадки: {weather_data['description']}"
    )

    await message.answer(response)

    save_to_csv(city, weather_data)

    await send_weather_media(message, weather_data)
