# 🚀 Быстрый запуск Admissions Agent

## 1. Установка зависимостей

```bash
# Создание виртуального окружения
python -m venv .venv

# Активация окружения (Linux/Mac)
source .venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt
```

## 2. Настройка

```bash
# Скопируйте файл с примером
cp .env.example .env

# Отредактируйте .env, добавив:
# TELEGRAM_BOT_TOKEN=ваш_токен_от_@BotFather
# GEMINI_API_KEY=ваш_ключ_от_Google_AI_Studio
```

## 3. Добавление данных (опционально)

Поместите файлы в папку `data/`:
- `.txt` файлы
- `.pdf` файлы  
- `.docx` файлы

## 4. Запуск

```bash
python main.py
```

Готово! Бот запущен и готов отвечать на вопросы в Telegram.

## 🔑 Где взять ключи

- **Telegram Bot Token**: @BotFather → `/newbot`
- **Gemini API Key**: https://makersuite.google.com/app/apikey