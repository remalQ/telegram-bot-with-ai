# handlers.py

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from telegram.ext import ContextTypes
import logging
from bot.storage import save_user_data
from bot.yagpt_include import ask_yagpt
import requests
import os

logger = logging.getLogger(__name__)
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


# Запрос на локацию
async def request_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[KeyboardButton(text="📍 Отправить локацию", request_location=True)]]
    reply_markup = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Чтобы узнать погоду, пожалуйста, отправьте свою геопозицию:",
        reply_markup=reply_markup
    )


# Обработка присланной геопозиции
async def location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    location = update.message.location
    if not location:
        await update.message.reply_text("Локация не получена. Повторите попытку.")
        return

    lat, lon = location.latitude, location.longitude
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&lang=ru&appid={OPENWEATHER_API_KEY}"
        resp = requests.get(url).json()

        city = resp.get("name", "Неизвестно")
        temp = resp["main"]["temp"]
        description = resp["weather"][0]["description"].capitalize()

        msg = f"🌍 *Город:* {city}\n🌡 *Температура:* {temp}°C\n☁ *Погода:* {description}"
        await update.message.reply_text(msg, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Ошибка при получении погоды: {e}")
        await update.message.reply_text("Не удалось получить данные о погоде.")


# Приветствие
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_data = {
        "name": user.first_name,
        "username": user.username,
        "id": user.id,
    }
    save_user_data(user.id, user_data)

    keyboard = [
        [
            InlineKeyboardButton("ℹ Команды", callback_data="show_help"),
            InlineKeyboardButton("🌦 Погода", callback_data="get_weather"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        f"👋 Привет, *{user.first_name}*!\n\n"
        "Я — *умный Telegram-бот*, готовый помочь.\n\n"
        "🔽 Выберите действие:"
    )

    image_url = "templates/start_image.jpg"

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=image_url,
        caption=welcome_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


# Помощь
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Доступные команды:\n/start\n/help")


# Обработка кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "show_help":
        await query.edit_message_caption(
            caption="📌 *Команды:*\n/start — приветствие\n/help — справка",
            parse_mode="Markdown"
        )
    elif query.data == "get_weather":
        await query.message.reply_text("⏳ Подготовка к получению погоды...")
        await request_location(update, context)


# Чат с YandexGPT
async def yagpt_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    if not user_message:
        await update.message.reply_text("Пожалуйста, отправьте текст для запроса.")
        return

    answer = await ask_yagpt(user_message)  # Используем YandexGPT
    await update.message.reply_text(answer)


# Обработка ошибок
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Произошла ошибка: %s", context.error)
    if isinstance(update, Update) and update.message:
        await update.message.reply_text("⚠️ Произошла ошибка. Попробуйте позже.")
