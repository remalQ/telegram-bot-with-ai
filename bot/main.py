import logging
import asyncio
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from bot.config import BOT_TOKEN
from bot.yagpt_include import periodic_iam_update
from telegram import BotCommand
from bot.handlers import (
    start,
    help_command,
    button_handler,
    error_handler,
    yagpt_handler,
    location_handler,
)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def main():
    """Основная асинхронная функция для запуска бота."""
    app = Application.builder().token(BOT_TOKEN).build()

    # Регистрация обработчиков
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, yagpt_handler))
    app.add_handler(MessageHandler(filters.LOCATION, location_handler))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_error_handler(error_handler)

    # Установка команд меню
    commands = [
        BotCommand("start", "Приветствие и главное меню"),
        BotCommand("help", "Справка по командам"),
        BotCommand("weather", "Узнать погоду по геолокации"),
    ]
    await app.bot.set_my_commands(commands)

    logger.info("Бот запущен...")

    # Создаем и запускаем фоновую задачу
    task = asyncio.create_task(periodic_iam_update())

    # Запускаем бота с обработкой остановки
    async with app:
        await app.start()
        await app.updater.start_polling()
        await task  # Ждем завершения задачи (фактически будет работать вечно)
        await app.updater.stop()
        await app.stop()

def run_bot():
    """Точка входа: запуск Telegram-бота."""
    # Создаем новый event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Ошибка при работе бота: {e}")
    finally:
        loop.close()
