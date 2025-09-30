#!/usr/bin/env python3
"""
Единая точка входа для запуска Admissions Agent
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Добавляем src в путь для импортов
sys.path.insert(0, str(Path(__file__).parent / "src"))

from app.config import Settings
from app.db import init_database
from rag.ingest import ingest_documents
from bot.main import main as start_bot

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def setup_database():
    """Инициализация базы данных"""
    logger.info("🗄️ Инициализация базы данных...")
    try:
        await init_database()
        logger.info("✅ База данных инициализирована")
    except Exception as e:
        logger.error(f"❌ Ошибка при инициализации БД: {e}")
        raise


async def setup_rag():
    """Настройка и индексация RAG"""
    logger.info("🔍 Индексация документов для RAG...")
    
    # Создаем папку для данных если её нет
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Проверяем наличие документов
    documents = list(data_dir.glob("*.txt")) + \
               list(data_dir.glob("*.pdf")) + \
               list(data_dir.glob("*.docx"))
    
    if not documents:
        logger.warning("⚠️ Документы для индексации не найдены в папке 'data/'")
        logger.info("📁 Создайте папку 'data/' и поместите туда файлы .txt, .pdf, .docx")
        return
    
    try:
        await ingest_documents(str(data_dir))
        logger.info(f"✅ Проиндексировано {len(documents)} документов")
    except Exception as e:
        logger.error(f"❌ Ошибка при индексации: {e}")
        # Не прерываем работу, бот может работать без RAG


async def main():
    """Главная функция запуска"""
    logger.info("🚀 Запуск Admissions Agent...")
    
    # Проверяем переменные окружения
    settings = Settings()
    if not settings.BOT_TOKEN:
        logger.error("❌ BOT_TOKEN не установлен в .env файле")
        sys.exit(1)
    
    if not settings.GOOGLE_API_KEY:
        logger.error("❌ GOOGLE_API_KEY не установлен в .env файле")
        sys.exit(1)
    
    try:
        # Инициализация базы данных
        await setup_database()
        
        # Настройка RAG
        await setup_rag()
        
        # Запуск бота
        logger.info("🤖 Запуск Telegram бота...")
        await start_bot()
        
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