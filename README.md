# Admissions Agent ALT

Telegram-бот для приемной комиссии университета ALT с поддержкой RAG (Retrieval-Augmented Generation) для ответа на вопросы поступающих.

## 🚀 Быстрый старт

### Предварительные требования

- Python 3.10+
- Telegram Bot Token (получить от [@BotFather](https://t.me/botfather))
- Google AI API Key или JSON Credentials (получить в [Google AI Studio](https://makersuite.google.com/app/apikey) или настроить сервисный аккаунт в Google Cloud Console)

### Установка и запуск

```bash
# 1. Клонирование репозитория
git clone <repository-url>
cd admissions-agent

# 2. Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# 3. Установка зависимостей
pip install -r requirements.txt

# 4. Настройка конфигурации
cp .env.example .env
# Отредактируйте .env файл, добавив ваши токены

# 5. Создание папки для документов (для RAG)
mkdir data
# Поместите ваши документы (.txt, .pdf, .docx) в папку data/

# 6. Запуск бота
python start.py
```

## ⚙️ Конфигурация

### Переменные окружения (.env)

```env
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Google AI (один из вариантов аутентификации)
# Вариант 1: API Key (получить в Google AI Studio)
GEMINI_API_KEY=your_google_ai_api_key_here

# Вариант 2: JSON Credentials (путь к файлу учетных данных сервисного аккаунта)
# GOOGLE_CREDENTIALS_PATH=.secrets/google-credentials.json

# Настройки для Vertex AI (требуются при использовании JSON credentials)
# GOOGLE_CLOUD_PROJECT=your-project-id
# GOOGLE_CLOUD_LOCATION=us-central1

# База данных (SQLite по умолчанию)
DATABASE_URL=sqlite+aiosqlite:///./admissions.db

# ChromaDB для RAG
CHROMA_DB_PATH=./chroma_db

# Другие настройки
LOG_LEVEL=INFO
ADMIN_USER_ID=123456789  # Telegram ID администратора
```

### Добавление данных для RAG

1. Поместите документы в папку `data/`:
   - `.txt` файлы - текстовые документы
   - `.pdf` файлы - PDF документы  
   - `.docx` файлы - документы Word

2. Бот автоматически проиндексирует их при запуске

## 🤖 Использование бота

### Команды

- `/start` - Начать работу с ботом
- `/help` - Показать справку
- `/profile` - Посмотреть профиль
- `/stats` - Статистика (для администраторов)

### Функции

1. **Ответы на вопросы**: Бот использует RAG для поиска релевантной информации
2. **Анкетирование**: Сбор данных о поступающих
3. **Персонализация**: Адаптация ответов под профиль пользователя

## 🏗️ Архитектура

```
src/
├── app/                    # Основное приложение
├── bot/                    # Telegram бот
├── rag/                    # RAG система
└── tests/                  # Тесты
```

## 🔧 Разработка

```bash
# Запуск тестов
python -m pytest

# Линтинг (если установлен)
ruff check src/
```

## 📝 Лицензия

[Укажите лицензию]