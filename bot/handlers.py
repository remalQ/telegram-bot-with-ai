# bot/handlers.py

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes
import logging
from bot.storage import save_user_data

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Приветствие с фото и inline-кнопками (всегда новое сообщение)."""

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
            InlineKeyboardButton("🗨 Диалог", callback_data="start_dialog"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        f"👋 Привет, *{user.first_name}*!\n\n"
        "Я — *умный Telegram-бот*, готовый помочь.\n\n"
        "🔽 Выберите действие:"
    )

    image_url = "templates/start_image.jpg"

    # Всегда отправляем новое сообщение
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=image_url,
        caption=welcome_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Доступные команды:\n/start\n/help\n/conversation")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Логгирует ошибки, не прерывая работу бота."""
    logger.error("Произошла ошибка: %s", context.error)
    if isinstance(update, Update) and update.message:
        await update.message.reply_text("⚠️ Произошла ошибка. Попробуйте позже.")


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "show_help":
        await query.edit_message_caption(
            caption="📌 *Команды:*\n/start — приветствие\n/help — справка\n/conversation — диалог",
            parse_mode="Markdown"
        )
    elif query.data == "start_dialog":
        await query.message.reply_text("✍ Запустите /conversation для начала диалога.")


async def conversation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🗨 Это заглушка для диалога. Здесь будет ИИ.")