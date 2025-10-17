#!/usr/bin/env python3
"""
Простая точка входа для запуска Admissions Agent
"""

import asyncio
import logging
import sys
from pathlib import Path

# Добавляем src в путь для импортов
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.app.config import Settings
from src.app.db import init_database
from src.bot.runner import main as main_bot
from src.rag.ingest import ingest_data

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Главная функция запуска"""
    logger.info("🚀 Запуск Admissions Agent...")
    
    # Проверяем переменные окружения
    try:
        settings = Settings()
    except Exception as e:
        logger.error(f"❌ Ошибка при загрузке настроек: {e}")
        logger.error("📋 Убедитесь что .env файл настроен корректно")
        sys.exit(1)
    
    if not settings.TELEGRAM_BOT_TOKEN:
        logger.error("❌ TELEGRAM_BOT_TOKEN не установлен в .env файле")
        sys.exit(1)
    
    # Проверяем, что есть либо API ключ, либо путь к JSON credentials
    has_api_key = bool(settings.GEMINI_API_KEY)
    has_credentials = bool(settings.GOOGLE_CREDENTIALS_PATH) and Path(settings.GOOGLE_CREDENTIALS_PATH).exists()
    
    if not has_api_key and not has_credentials:
        logger.error("❌ Не найдены ни GEMINI_API_KEY, ни действительные JSON credentials (GOOGLE_CREDENTIALS_PATH)")
        logger.error("📋 Убедитесь, что в .env файле установлен хотя бы один вариант аутентификации:")
        logger.error("   - GEMINI_API_KEY=ваш_ключ_или")
        logger.error("   - GOOGLE_CREDENTIALS_PATH=путь_к_файлу_json_credentials")
        sys.exit(1)
        
    logger.info("✅ Токены бота и аутентификация Google AI настроены")
    
    try:
        # 1. Инициализация базы данных
        logger.info("🗄️ Инициализация базы данных...")
        await init_database()
        logger.info("✅ База данных инициализирована")
        
        # 2. Создаем папку для данных если её нет
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        # 3. Проверяем наличие документов и индексируем их
        documents = list(data_dir.glob("*.txt")) + \
                   list(data_dir.glob("*.pdf")) + \
                   list(data_dir.glob("*.docx"))
        
        if documents:
            logger.info(f"🔍 Найдено {len(documents)} документов для индексации...")
            try:
                await ingest_data()
                logger.info(f"✅ Проиндексировано {len(documents)} документов")
            except Exception as e:
                logger.error(f"❌ Ошибка при индексации: {e}")
                logger.warning("⚠️ Бот будет работать без RAG функций")
        else:
            logger.warning("⚠️ Документы для индексации не найдены в папке 'data/'")
            logger.info("📁 Поместите файлы .txt, .pdf, .docx в папку 'data/' для работы RAG")
        
        # 4. Запуск бота
        logger.info("🤖 Запуск Telegram бота...")
        await main_bot()
        
    except KeyboardInterrupt:
        logger.info("👋 Завершение работы...")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 До свидания!")