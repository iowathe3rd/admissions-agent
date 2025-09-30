# Быстрый запуск Admissions Agent

## Установка и запуск

1. **Создание виртуального окружения:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # или
   venv\Scripts\activate     # Windows
   ```

2. **Установка зависимостей:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Настройка переменных окружения:**
   Скопируйте `.env.example` в `.env` и заполните:
   ```bash
   cp .env.example .env
   ```
   
   Отредактируйте `.env`:
   ```
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   GOOGLE_API_KEY=your_google_api_key
   DATABASE_URL=sqlite+aiosqlite:///./admissions.db
   CHROMA_PERSIST_DIRECTORY=./chroma_db
   ```

4. **Добавление данных для RAG (опционально):**
   Создайте папку `data` и поместите туда документы:
   ```bash
   mkdir data
   # Скопируйте файлы .txt, .pdf, .docx в эту папку
   ```

5. **Запуск системы:**
   ```bash
   python main.py
   ```

## Что происходит при запуске

1. Инициализация базы данных SQLite
2. Проверка конфигурации (токены API)
3. Индексация документов из папки `data` (если есть)
4. Запуск Telegram бота

## Поддерживаемые форматы документов

- `.txt` - текстовые файлы
- `.pdf` - PDF документы
- `.docx` - документы Microsoft Word

## Логи

Логи сохраняются в файл `admissions_agent.log` и выводятся в консоль.