# 🚀 Установка и настройка

## Системные требования

### Минимальные требования
- **Python**: 3.10 или выше
- **RAM**: 2 GB свободной памяти
- **Диск**: 1 GB свободного места
- **ОС**: Linux, macOS, Windows

### Рекомендуемые требования
- **Python**: 3.11+
- **RAM**: 4 GB или больше
- **Диск**: 5 GB свободного места
- **ОС**: Ubuntu 20.04+ или macOS 12+

## Предварительная подготовка

### 1. Установка Python

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev
```

#### macOS
```bash
# Используя Homebrew
brew install python@3.11
```

#### Windows
Скачайте и установите Python с [официального сайта](https://python.org/downloads/)

### 2. Установка Poetry

```bash
# Установка Poetry (рекомендуемый способ)
curl -sSL https://install.python-poetry.org | python3 -

# Или через pip
pip install poetry

# Проверка установки
poetry --version
```

### 3. Установка Docker (опционально)

#### Ubuntu
```bash
sudo apt update
sudo apt install docker.io docker-compose
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

#### macOS
Установите [Docker Desktop for Mac](https://docs.docker.com/desktop/mac/install/)

#### Windows
Установите [Docker Desktop for Windows](https://docs.docker.com/desktop/windows/install/)

## Клонирование репозитория

```bash
git clone https://github.com/alt-ai/admissions-agent.git
cd admissions-agent
```

## Установка зависимостей

### Вариант 1: С помощью Poetry (рекомендуется)

```bash
# Установка зависимостей
poetry install

# Активация виртуального окружения
poetry shell
```

### Вариант 2: С помощью pip

```bash
# Создание виртуального окружения
python -m venv venv

# Активация окружения
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate

# Установка зависимостей
pip install -e .
```

## Получение API ключей

### Telegram Bot Token

1. Найдите [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям:
   - Выберите имя для бота (например, "ALT Admissions Bot")
   - Выберите username (например, "alt_admissions_bot")
4. Сохраните полученный токен

### Google Gemini API Key

1. Перейдите на [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Войдите в свой Google аккаунт
3. Нажмите "Create API Key"
4. Выберите проект или создайте новый
5. Скопируйте созданный API ключ

## Настройка конфигурации

### Создание .env файла

```bash
# Копирование примера конфигурации
cp .env.example .env
```

### Заполнение .env файла

Откройте файл `.env` и заполните его:

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN="ваш_telegram_bot_token"

# Google Gemini API Configuration
GEMINI_API_KEY="ваш_gemini_api_key"

# Optional: Database Configuration (по умолчанию SQLite)
# DATABASE_URL="sqlite+aiosqlite:///./data/bot.db"

# Optional: Logging Level
# LOG_LEVEL="INFO"

# Optional: Custom models
# GEMINI_DEFAULT_MODEL="gemini-2.0-flash-exp"
# GEMINI_EMBEDDING_MODEL="text-embedding-004"
```

## Проверка установки

### Проверка окружения

```bash
# Проверка Python версии
python --version

# Проверка Poetry
poetry --version

# Проверка зависимостей
poetry check
```

### Тестовый запуск

```bash
# Проверка импортов
python -c "from src.app.main import app; print('✅ FastAPI импорт успешен')"
python -c "from src.bot.runner import main; print('✅ Bot импорт успешен')"
python -c "from src.rag.genai import llm_answer; print('✅ RAG импорт успешен')"
```

## Структура после установки

После успешной установки ваша структура проекта должна выглядеть так:

```
admissions-agent/
├── .env                    # Ваш конфигурационный файл
├── .env.example           # Пример конфигурации
├── poetry.lock            # Зафиксированные версии зависимостей
├── pyproject.toml         # Конфигурация проекта
├── run.py                 # Скрипт запуска
├── src/                   # Исходный код
│   ├── app/              # FastAPI приложение
│   ├── bot/              # Telegram бот
│   ├── rag/              # RAG система
│   └── data/             # Данные
└── docs/                  # Документация
```

## Решение проблем установки

### Ошибка Poetry not found

```bash
# Добавьте Poetry в PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Ошибки с Python версией

```bash
# Убедитесь что используете правильную версию Python
poetry env use python3.11
```

### Проблемы с правами (Linux)

```bash
# Если ошибки с правами доступа
sudo chown -R $USER:$USER .
chmod +x run.py
```

### Проблемы с зависимостями

```bash
# Очистка кэша и переустановка
poetry cache clear pypi --all
poetry install --no-cache
```

## Следующие шаги

После успешной установки переходите к:
- [Быстрому старту](./quick-start.md)
- [Конфигурации](./configuration.md)
- [Локальной разработке](./development/local-development.md)