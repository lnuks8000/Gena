# utils/weather_api.py

import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

# Получаем погоду по API
async def get_weather(city: str):
    url = (
        f"http://api.openweathermap.org/data/2.5/weather?q={city}"
        f"&appid={API_KEY}&units=metric&lang=ru"
    )

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return None

            data = await response.json()

            # Извлекаем нужные параметры
            weather = {
                "temp": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"],
                "main": data["weather"][0]["main"]
            }

            return weather
