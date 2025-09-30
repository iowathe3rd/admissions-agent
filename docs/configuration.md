# ⚙️ Конфигурация

Полное руководство по настройке Admissions Agent для различных сценариев использования.

## Структура конфигурации

Система использует несколько уровней конфигурации:

1. **Переменные окружения** (`.env` файл)
2. **Настройки приложения** (`src/app/config.py`)
3. **Конфигурация Poetry** (`pyproject.toml`)
4. **Docker конфигурация** (`docker-compose.yml`)

## Основные переменные окружения

### Обязательные параметры

```env
# Telegram Bot Token (обязательно)
TELEGRAM_BOT_TOKEN="1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Google Gemini API Key (обязательно)
GEMINI_API_KEY="AIzaSyB..."
```

### Необязательные параметры

```env
# База данных (по умолчанию SQLite)
DATABASE_URL="sqlite+aiosqlite:///./data/bot.db"

# Уровень логирования (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL="INFO"

# Модели Gemini
GEMINI_DEFAULT_MODEL="gemini-2.0-flash-exp"
GEMINI_PRO_MODEL="gemini-2.0-pro-exp"
GEMINI_EMBEDDING_MODEL="text-embedding-004"

# FastAPI настройки
API_HOST="0.0.0.0"
API_PORT="8000"
API_RELOAD="true"

# ChromaDB настройки
CHROMA_PERSIST_DIRECTORY="./src/rag/index"
CHROMA_COLLECTION_NAME="admissions_knowledge"

# Ограничения RAG
RAG_MAX_CHUNKS="5"
RAG_CHUNK_SIZE="1000"
RAG_SIMILARITY_THRESHOLD="0.3"
```

## Конфигурация моделей AI

### Доступные модели Gemini

```env
# Быстрая модель для большинства задач
GEMINI_DEFAULT_MODEL="gemini-2.0-flash-exp"

# Продвинутая модель для сложных запросов
GEMINI_PRO_MODEL="gemini-2.0-pro-exp"

# Устаревшие но стабильные модели
GEMINI_FLASH_MODEL="gemini-1.5-flash"
GEMINI_PRO_LEGACY="gemini-1.5-pro"

# Модели эмбеддингов
GEMINI_EMBEDDING_MODEL="text-embedding-004"
GEMINI_EMBEDDING_LEGACY="models/embedding-001"
```

### Настройка параметров генерации

В файле `src/rag/genai.py` можно настроить:

```python
# Температура (креативность ответов)
temperature = 0.3  # 0.0 - консервативно, 1.0 - креативно

# Максимальная длина ответа
max_output_tokens = 1000

# Top-p (разнообразие ответов)
top_p = 0.8

# Top-k (количество рассматриваемых токенов)
top_k = 40
```

## Конфигурация базы данных

### SQLite (по умолчанию)

```env
DATABASE_URL="sqlite+aiosqlite:///./data/bot.db"
```

### PostgreSQL (рекомендуется для продакшна)

```env
DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/admissions_bot"
```

### MySQL

```env
DATABASE_URL="mysql+aiomysql://user:password@localhost:3306/admissions_bot"
```

## Конфигурация Telegram бота

### Базовые настройки

```env
# Токен бота
TELEGRAM_BOT_TOKEN="your_token_here"

# Webhook настройки (для продакшна)
TELEGRAM_WEBHOOK_URL="https://yourdomain.com/webhook"
TELEGRAM_WEBHOOK_SECRET="your_webhook_secret"

# Polling настройки (для разработки)
TELEGRAM_POLLING_TIMEOUT="60"
TELEGRAM_POLLING_LIMIT="100"
```

### Настройки поведения бота

В файле `src/bot/config.py`:

```python
# Максимальная длина сообщения пользователя
MAX_MESSAGE_LENGTH = 1000

# Таймаут ожидания ответа от AI
AI_RESPONSE_TIMEOUT = 30

# Количество попыток при ошибке
MAX_RETRIES = 3

# Задержка между попытками (секунды)
RETRY_DELAY = 2
```

## Конфигурация RAG системы

### ChromaDB настройки

```env
# Директория для хранения индекса
CHROMA_PERSIST_DIRECTORY="./src/rag/index"

# Имя коллекции
CHROMA_COLLECTION_NAME="admissions_knowledge"

# Функция расстояния (cosine, l2, ip)
CHROMA_DISTANCE_FUNCTION="cosine"
```

### Параметры поиска

```env
# Максимальное количество найденных фрагментов
RAG_MAX_CHUNKS="5"

# Размер фрагмента текста (в символах)
RAG_CHUNK_SIZE="1000"

# Перекрытие между фрагментами
RAG_CHUNK_OVERLAP="200"

# Минимальный порог схожести
RAG_SIMILARITY_THRESHOLD="0.3"

# Максимальная длина контекста для AI
RAG_MAX_CONTEXT_LENGTH="4000"
```

## Конфигурация логирования

### Базовая настройка

```env
# Уровень логирования
LOG_LEVEL="INFO"

# Формат логов
LOG_FORMAT="%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Файл для логов (опционально)
LOG_FILE="./logs/app.log"

# Ротация логов
LOG_MAX_SIZE="10MB"
LOG_BACKUP_COUNT="5"
```

### Детальная настройка в коде

В файле `src/app/config.py`:

```python
import logging

# Настройка логирования для разных компонентов
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "INFO",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "detailed",
            "filename": "logs/app.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
        }
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["console", "file"],
            "level": "INFO",
        },
        "src.bot": {
            "level": "DEBUG",
        },
        "src.rag": {
            "level": "DEBUG",
        },
        "httpx": {
            "level": "WARNING",
        }
    }
}
```

## Продакшн конфигурация

### Рекомендуемые настройки для продакшна

```env
# Безопасность
LOG_LEVEL="WARNING"
API_RELOAD="false"

# Производительность
GEMINI_DEFAULT_MODEL="gemini-2.0-flash-exp"
RAG_MAX_CHUNKS="3"
RAG_SIMILARITY_THRESHOLD="0.4"

# Мониторинг
SENTRY_DSN="https://your-sentry-dsn"
ENABLE_METRICS="true"

# База данных
DATABASE_URL="postgresql+asyncpg://user:password@db:5432/admissions_bot"
DATABASE_POOL_SIZE="20"
DATABASE_MAX_OVERFLOW="30"
```

### Docker Compose для продакшна

```yaml
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: admissions_bot
      POSTGRES_USER: bot_user
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  app:
    build: .
    environment:
      DATABASE_URL: "postgresql+asyncpg://bot_user:secure_password@db:5432/admissions_bot"
      TELEGRAM_BOT_TOKEN: "${TELEGRAM_BOT_TOKEN}"
      GEMINI_API_KEY: "${GEMINI_API_KEY}"
      LOG_LEVEL: "WARNING"
    depends_on:
      - db
    restart: unless-stopped
    volumes:
      - app_data:/app/data
      - logs:/app/logs

volumes:
  postgres_data:
  app_data:
  logs:
```

## Валидация конфигурации

### Проверка настроек

```bash
# Проверка переменных окружения
python -c "from src.app.config import settings; print(settings.dict())"

# Проверка подключения к базе данных
python -c "from src.app.db import test_connection; import asyncio; asyncio.run(test_connection())"

# Проверка Gemini API
python -c "from src.rag.genai import test_connection; print(test_connection())"

# Проверка Telegram API
python -c "from src.bot.runner import test_bot_token; import asyncio; asyncio.run(test_bot_token())"
```

### Автоматическая проверка

Создайте скрипт `scripts/validate_config.py`:

```python
#!/usr/bin/env python3
"""Проверка конфигурации системы."""

import os
import sys
import asyncio
from pathlib import Path

async def validate_config():
    """Проверяет все аспекты конфигурации."""
    errors = []
    
    # Проверка .env файла
    if not Path(".env").exists():
        errors.append("❌ Файл .env не найден")
    
    # Проверка обязательных переменных
    required_vars = ["TELEGRAM_BOT_TOKEN", "GEMINI_API_KEY"]
    for var in required_vars:
        if not os.getenv(var):
            errors.append(f"❌ Переменная {var} не установлена")
    
    # Проверка подключений
    try:
        from src.app.db import test_connection
        await test_connection()
        print("✅ База данных доступна")
    except Exception as e:
        errors.append(f"❌ База данных недоступна: {e}")
    
    # Вывод результатов
    if errors:
        print("\n".join(errors))
        sys.exit(1)
    else:
        print("✅ Конфигурация валидна")

if __name__ == "__main__":
    asyncio.run(validate_config())
```

## Примеры конфигураций

### Разработка

```env
# .env для разработки
TELEGRAM_BOT_TOKEN="test_token"
GEMINI_API_KEY="test_key"
LOG_LEVEL="DEBUG"
API_RELOAD="true"
DATABASE_URL="sqlite+aiosqlite:///./data/test.db"
```

### Тестирование

```env
# .env.test
TELEGRAM_BOT_TOKEN="test_token"
GEMINI_API_KEY="test_key"
LOG_LEVEL="ERROR"
DATABASE_URL="sqlite+aiosqlite:///:memory:"
CHROMA_PERSIST_DIRECTORY="./test_index"
```

### Продакшн

```env
# .env.production
TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN}"
GEMINI_API_KEY="${GEMINI_API_KEY}"
LOG_LEVEL="WARNING"
API_RELOAD="false"
DATABASE_URL="postgresql+asyncpg://user:pass@db:5432/bot"
SENTRY_DSN="${SENTRY_DSN}"
```

## Миграция конфигурации

### Обновление с предыдущих версий

```bash
# Резервная копия текущей конфигурации
cp .env .env.backup

# Сравнение с новым примером
diff .env.example .env

# Добавление новых параметров
cat .env.example >> .env
```

### Скрипт миграции

```python
#!/usr/bin/env python3
"""Скрипт миграции конфигурации."""

import os
from pathlib import Path

def migrate_config():
    """Мигрирует конфигурацию на новую версию."""
    
    # Читаем текущую конфигурацию
    current_env = {}
    env_file = Path(".env")
    
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                key, value = line.split("=", 1)
                current_env[key] = value
    
    # Добавляем новые параметры
    new_params = {
        "GEMINI_DEFAULT_MODEL": "gemini-2.0-flash-exp",
        "RAG_MAX_CHUNKS": "5",
        "API_HOST": "0.0.0.0",
    }
    
    for key, default_value in new_params.items():
        if key not in current_env:
            current_env[key] = default_value
            print(f"➕ Добавлен параметр {key}={default_value}")
    
    # Записываем обновленную конфигурацию
    with open(".env", "w") as f:
        for key, value in current_env.items():
            f.write(f"{key}={value}\n")
    
    print("✅ Конфигурация обновлена")

if __name__ == "__main__":
    migrate_config()
```