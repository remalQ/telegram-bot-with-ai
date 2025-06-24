# bot/storage.py

import json
import os

DATA_FILE = "data/users.json"


def save_user_data(user_id: int, data: dict) -> None:
    """Сохраняет данные пользователя в JSON."""
    if not os.path.exists("data"):
        os.makedirs("data")

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = {}

    users[str(user_id)] = data

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4, ensure_ascii=False)
