# 🔧 Финальные исправления для Pylance ошибок

## ✅ Исправлено в pyproject.toml
- Добавлены все необходимые зависимости

## ✅ Создайте __init__.py файлы для правильных импортов

```bash
# Создание недостающих __init__.py
touch src/__init__.py
touch src/app/__init__.py
touch src/bot/__init__.py  
touch src/rag/__init__.py
```

## ✅ Альтернативный импорт для config.py

Если `pydantic-settings` не устанавливается, используйте:

```python
# src/app/config.py - альтернативная версия
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self.TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
        
        # LLM Model IDs
        self.GEMINI_DEFAULT_MODEL = "gemini-2.5-flash"
        self.GEMINI_PRO_MODEL = "gemini-2.5-pro"
        self.GEMINI_LITE_MODEL = "gemini-2.5-flash-lite"
        self.GEMINI_EMBEDDING_MODEL = "gemini-embedding-001"

        # RAG Settings
        self.RAG_RELEVANCE_THRESHOLD = 0.75
        self.RAG_TOP_K = 5

        # Project paths
        self.ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.DATA_DIR = os.path.join(self.ROOT_DIR, "src", "data", "seed")
        self.INDEX_DIR = os.path.join(self.ROOT_DIR, "src", "rag", "index")

settings = Settings()
```

## ✅ Быстрые команды для проверки

После `poetry install`:

```bash
# Создание недостающих файлов
touch src/__init__.py src/app/__init__.py src/bot/__init__.py src/rag/__init__.py

# Проверка импортов
python -c "
try:
    from src.app.db import AsyncSessionLocal
    print('✅ DB imports OK')
except Exception as e:
    print(f'❌ DB imports: {e}')

try:
    from src.bot.handlers import router
    print('✅ Bot imports OK')
except Exception as e:
    print(f'❌ Bot imports: {e}')

try:
    from src.rag.genai import embed_texts
    print('✅ RAG imports OK')
except Exception as e:
    print(f'❌ RAG imports: {e}')
"

# Полный запуск
python run.py full
```

## 🎯 Ожидаемый результат

После всех исправлений количество ошибок Pylance должно снизиться с 30+ до 0-5 (только dev-зависимости).

Основные рабочие импорты и типы должны быть исправлены.

Проект должен запускаться без критических ошибок.