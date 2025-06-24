# bot/main.py

import logging
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
)
from bot.config import BOT_TOKEN
from bot.handlers import (
    start,
    help_command,
    conversation,
    button_handler,
    error_handler,  # добавим обработку ошибок
)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def run_bot() -> None:
    """Точка входа: запуск Telegram-бота."""
    app = Application.builder().token(BOT_TOKEN).build()

    # Регистрируем обработчики команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("conversation", conversation))

    # Обработчик inline-кнопок
    app.add_handler(CallbackQueryHandler(button_handler))

    # Обработчик ошибок (необязательно, но полезно)
    app.add_error_handler(error_handler)

    logger.info("Бот запущен...")
    app.run_polling()
