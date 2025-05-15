# utils/media_sender.py

import os
from aiogram.types import FSInputFile, Message

# Отправляем соответствующую медиа (изображение или звук) в зависимости от погоды
async def send_weather_media(message: Message, weather_data: dict):
    condition = weather_data["main"].lower()

    # Путь к ассетам
    media_path = "data/assets/"

    # Варианты файлов
    sunny_img = FSInputFile(os.path.join(media_path, "sunny.jpg"))
    rain_img = FSInputFile(os.path.join(media_path, "rain.jpg"))
    music = FSInputFile(os.path.join(media_path, "sound.mp3"))

    if "rain" in condition:
        await message.answer_photo(rain_img, caption="🌧 Похоже, идёт дождь!")
    elif "clear" in condition or "sun" in condition:
        await message.answer_photo(sunny_img, caption="☀️ Солнечно!")
    else:
        # Для всех остальных условий отправляем звук
        await message.answer_audio(music, caption="🎵 Атмосфера погоды.")
