# 🚀 Быстрый запуск Admissions Agent

## Простая установка и запуск

### 1. Подготовка окружения
```bash
# Создаем виртуальное окружение
python -m venv .venv

# Активируем его
source .venv/bin/activate  # Linux/Mac
# или
.venv\Scripts\activate     # Windows

# Устанавливаем зависимости
pip install -r requirements.txt
```

### 2. Настройка переменных окружения
```bash
# Копируем файл настроек
cp .env.example .env

# Редактируем .env файл
```

Заполните в `.env`:
```env
BOT_TOKEN=your_telegram_bot_token_here
GOOGLE_API_KEY=your_google_api_key_here
```

### 3. Подготовка данных (опционально)
```bash
# Создаем папку для документов
mkdir data

# Помещаем туда файлы .txt, .pdf, .docx
# Например:
# cp ~/Documents/admission_info.pdf data/
# cp ~/Documents/faq.txt data/
```

### 4. Запуск
```bash
python main.py
```

## 📋 Что происходит при запуске?

1. **Инициализация БД** - создается SQLite база данных
2. **Проверка API ключей** - проверяются токены
3. **Индексация документов** - если есть файлы в `data/`
4. **Запуск бота** - бот готов к работе!

## 📄 Поддерживаемые форматы

- **TXT** - простые текстовые файлы
- **PDF** - PDF документы
- **DOCX** - документы Microsoft Word

## 🤖 Тестирование бота

После запуска:
1. Найдите своего бота в Telegram
2. Отправьте `/start`
3. Попробуйте задать вопросы

## ⚠️ Частые проблемы

### Ошибка "No module named 'chromadb'"
```bash
pip install chromadb
```

### Ошибка "BOT_TOKEN не установлен"
- Проверьте файл `.env`
- Убедитесь что токен получен от @BotFather

### Ошибка с PyPDF2 или python-docx
```bash
pip install PyPDF2 python-docx
```

## 📁 Структура проекта
```
├── data/              # 📄 Документы для RAG
├── src/
│   ├── app/           # 🏗️ Основное приложение
│   ├── bot/           # 🤖 Telegram бот
│   ├── rag/           # 🔍 RAG система
│   └── tests/         # 🧪 Тесты
├── main.py            # 🚀 Точка входа
├── requirements.txt   # 📦 Зависимости
└── .env              # ⚙️ Переменные окружения
```