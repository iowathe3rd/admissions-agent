#!/usr/bin/env python3
"""
Скрипт для запуска различных компонентов системы.

Использование:
    python run.py ingest    # Запустить индексацию данных
    python run.py api       # Запустить API сервер
    python run.py bot       # Запустить Telegram бота
    python run.py test      # Запустить тесты
    python run.py full      # Полный цикл: индексация + API + бот
"""

import sys
import asyncio
import subprocess
import time
import logging
from pathlib import Path

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_command(command, description):
    """Запускает команду и логирует результат."""
    logger.info(f"Запуск: {description}")
    logger.info(f"Команда: {' '.join(command)}")
    
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        logger.info(f"✅ {description} завершено успешно")
        if result.stdout:
            logger.info(f"Вывод: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Ошибка при выполнении: {description}")
        logger.error(f"Код возврата: {e.returncode}")
        if e.stdout:
            logger.error(f"stdout: {e.stdout}")
        if e.stderr:
            logger.error(f"stderr: {e.stderr}")
        return False

async def run_ingest():
    """Запускает процесс индексации данных."""
    logger.info("🔄 Запуск индексации данных...")
    
    try:
        from src.rag.ingest import ingest_data
        await ingest_data()
        logger.info("✅ Индексация данных завершена")
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка при индексации: {e}")
        return False

def run_api():
    """Запускает API сервер."""
    command = ["python", "-m", "uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
    return run_command(command, "API сервер")

def run_bot():
    """Запускает Telegram бота."""
    command = ["python", "-m", "src.bot.runner"]
    return run_command(command, "Telegram бот")

def run_tests():
    """Запускает тесты."""
    command = ["python", "-m", "pytest", "src/tests/", "-v"]
    return run_command(command, "Тесты")

def check_environment():
    """Проверяет окружение и зависимости."""
    logger.info("🔍 Проверка окружения...")
    
    # Проверяем .env файл
    env_file = Path(".env")
    if not env_file.exists():
        logger.warning("⚠️  Файл .env не найден. Скопируйте .env.example в .env и заполните его.")
        return False
    
    # Проверяем poetry
    try:
        subprocess.run(["poetry", "--version"], check=True, capture_output=True)
        logger.info("✅ Poetry найден")
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error("❌ Poetry не найден. Установите Poetry для управления зависимостями.")
        return False
    
    # Проверяем зависимости
    try:
        subprocess.run(["poetry", "check"], check=True, capture_output=True)
        logger.info("✅ Зависимости корректны")
    except subprocess.CalledProcessError:
        logger.warning("⚠️  Проблемы с зависимостями. Запуск poetry install...")
        if not run_command(["poetry", "install"], "Установка зависимостей"):
            return False
    
    logger.info("✅ Окружение готово")
    return True

async def run_full():
    """Полный цикл запуска: индексация, затем параллельный запуск API и бота."""
    logger.info("🚀 Полный запуск системы...")
    
    # Сначала индексация
    if not await run_ingest():
        logger.error("❌ Не удалось выполнить индексацию")
        return False
    
    logger.info("🔄 Запуск API и бота параллельно...")
    
    # Запуск API в фоне
    api_process = subprocess.Popen(
        ["python", "-m", "uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Даем API время запуститься
    time.sleep(5)
    
    # Запуск бота
    bot_process = subprocess.Popen(
        ["python", "-m", "src.bot.runner"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    logger.info("✅ API и бот запущены")
    logger.info(f"API PID: {api_process.pid}")
    logger.info(f"Bot PID: {bot_process.pid}")
    logger.info("Для остановки нажмите Ctrl+C")
    
    try:
        # Ждем завершения любого из процессов
        while api_process.poll() is None and bot_process.poll() is None:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("🛑 Получен сигнал остановки")
        
        # Останавливаем процессы
        api_process.terminate()
        bot_process.terminate()
        
        # Ждем завершения
        api_process.wait(timeout=10)
        bot_process.wait(timeout=10)
        
        logger.info("✅ Все процессы остановлены")

def main():
    """Основная функция."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    # Проверяем окружение для всех команд кроме help
    if command != "help":
        if not check_environment():
            logger.error("❌ Окружение не готово")
            sys.exit(1)
    
    if command == "ingest":
        asyncio.run(run_ingest())
    elif command == "api":
        run_api()
    elif command == "bot":
        run_bot()
    elif command == "test":
        run_tests()
    elif command == "full":
        asyncio.run(run_full())
    elif command == "help":
        print(__doc__)
    else:
        logger.error(f"❌ Неизвестная команда: {command}")
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()