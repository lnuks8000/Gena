# utils/file_manager.py

import csv
import os
from datetime import datetime

# Путь до CSV файла
CSV_FILE = "data/weather_data.csv"

# Сохраняем данные о запросе в CSV
def save_to_csv(city: str, weather: dict):
    # Создаём папку, если не существует
    os.makedirs("data", exist_ok=True)

    # Открываем CSV в режиме добавления
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            city,
            weather["temp"],
            weather["humidity"],
            weather["description"]
        ])
