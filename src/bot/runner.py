import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.types import ErrorEvent

from app.config import settings
from src.bot.handlers import router as main_router

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def error_handler(event: ErrorEvent):
    """Обработчик ошибок бота."""
    logger.error(f"Ошибка при обработке обновления {event.update}: {event.exception}")

async def main():
    """Инициализирует и запускает бота."""
    if not settings.TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN не установлен. Бот не может быть запущен.")
        sys.exit(1)

    if not settings.GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY не установлен. Бот не может быть запущен.")
        sys.exit(1)

    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()

    # Регистрируем обработчик ошибок
    dp.errors.register(error_handler)

    # Включаем основной роутер
    dp.include_router(main_router)

    logger.info("Запуск бота...")
    try:
        # Начинаем поллинг
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Критическая ошибка бота: {e}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен вручную.")
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
        sys.exit(1)
