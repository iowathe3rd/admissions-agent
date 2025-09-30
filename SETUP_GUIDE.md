# 🚀 Полный гайд по запуску Admissions Agent

## 📋 Предварительные требования

- Python 3.10+
- Poetry (для управления зависимостями)
- API ключ Google Gemini
- Telegram Bot Token

## 🔧 Установка и настройка

### 1. Клонирование и установка зависимостей

```bash
# Переходим в папку проекта
cd /home/baur/home/dev/github.com/alt-ai/admissions-agent

# Устанавливаем зависимости
poetry install

# Или через pip (если нет Poetry)
pip install -e .
```

### 2. Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```bash
# Создаем .env файл
touch .env
```

Добавьте в `.env`:

```env
# API ключи
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
GEMINI_API_KEY=your_google_gemini_api_key_here

# Опциональные настройки
RAG_RELEVANCE_THRESHOLD=0.75
RAG_TOP_K=5
```

### 3. Получение API ключей

#### Telegram Bot Token:
1. Найдите [@BotFather](https://t.me/botfather) в Telegram
2. Отправьте `/newbot`
3. Следуйте инструкциям
4. Скопируйте токен в `.env`

#### Google Gemini API Key:
1. Идите на [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Создайте новый API ключ
3. Скопируйте ключ в `.env`

## 📄 Подготовка данных для RAG

### Структура папок данных

```
src/data/seed/          # 📂 Основная папка с данными
├── programs.json       # ✅ Программы обучения
├── faqs.json          # ✅ Часто задаваемые вопросы
├── documents.json     # ✅ Необходимые документы
├── steps.json         # ✅ Шаги поступления
├── admission_info.txt # 🆕 Общая информация (TXT)
├── rules.pdf          # 🆕 Правила приема (PDF)
└── handbook.docx      # 🆕 Справочник (DOCX)
```

### Поддерживаемые форматы файлов

#### 📝 JSON файлы (основной формат)
```json
// programs.json
[
  {
    "id": 1,
    "name": "Прикладная информатика",
    "description": "Программа готовит специалистов в области разработки ПО",
    "cost": 250000,
    "duration": "4 года",
    "entrance_exams": ["Математика", "Информатика", "Русский язык"]
  }
]

// faqs.json
[
  {
    "id": 1,
    "question": "Какие сроки подачи документов?",
    "answer": "Документы принимаются с 20 июня по 25 июля"
  }
]
```

#### 📄 TXT файлы
```txt
Общая информация о поступлении

ALT University - современный университет...
Адрес: г. Москва, ул. Университетская, д. 1
Телефон: +7 (495) 123-45-67
```

#### 📄 PDF и DOCX файлы
- Положите любые PDF или DOCX документы в папку `src/data/seed/`
- Система автоматически извлечет из них текст

## 🚀 Запуск проекта

### Проверка готовности

```bash
# Проверяем настройки
python -c "
from src.app.config import settings
print(f'✅ Telegram Token: {bool(settings.TELEGRAM_BOT_TOKEN)}')
print(f'✅ Gemini API Key: {bool(settings.GEMINI_API_KEY)}')
print(f'✅ Data Dir: {settings.DATA_DIR}')
"
```

### Полный запуск (рекомендуется)

```bash
# Запускаем полную систему (RAG + Bot + API)
python run.py full
```

### Поэтапный запуск

#### 1. Только индексация данных
```bash
# Индексируем данные в RAG систему
python run.py ingest
```

Ожидаемый вывод:
```
✅ Загружено документов: {
  "total_documents": 8,
  "successful": 7,
  "failed": 1,
  "supported_formats": ["JSON", "TXT", "PDF", "DOCX"]
}
✅ Создано 156 чанков из 7 документов
✅ Индексация данных завершена
```

#### 2. Только Telegram бот
```bash
# Запускаем только телеграм бота
python run.py bot
```

#### 3. Только API сервер
```bash
# Запускаем только FastAPI сервер
python run.py api
```

#### 4. Только тесты
```bash
# Запускаем тесты
python run.py test
```

## 📊 Как добавить свои данные

### Добавление JSON данных

1. **Программы обучения** (`programs.json`):
```json
[
  {
    "name": "Ваша программа",
    "description": "Описание программы",
    "cost": 200000,
    "duration": "4 года",
    "requirements": ["ЕГЭ по математике", "ЕГЭ по физике"]
  }
]
```

2. **FAQ** (`faqs.json`):
```json
[
  {
    "question": "Ваш вопрос?",
    "answer": "Ваш ответ на вопрос"
  }
]
```

### Добавление документов

1. **Скопируйте файлы** в `src/data/seed/`:
```bash
cp your_document.pdf src/data/seed/
cp your_handbook.docx src/data/seed/
cp your_info.txt src/data/seed/
```

2. **Переиндексируйте** данные:
```bash
python run.py ingest
```

## 🔍 Проверка работы RAG

### Тестирование через API

```bash
# Запустите API сервер
python run.py api

# В другом терминале протестируйте:
curl -X POST "http://localhost:8000/rag/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Какие программы обучения доступны?"}'
```

### Тестирование через Telegram

1. Запустите бота: `python run.py bot`
2. Найдите вашего бота в Telegram
3. Отправьте `/start`
4. Задайте вопрос: "Расскажи о программах обучения"

## 🐛 Решение проблем

### Ошибка "ChromaDB коллекция недоступна"
```bash
# Переиндексируйте данные
python run.py ingest
```

### Ошибка "Google API Key not found"
```bash
# Проверьте .env файл
cat .env | grep GEMINI_API_KEY
```

### Ошибка "Не найдено документов для индексации"
```bash
# Проверьте наличие файлов
ls -la src/data/seed/
```

### Ошибка импорта PyPDF2 или python-docx
```bash
# Переустановите зависимости
poetry install
# или
pip install PyPDF2 python-docx
```

## 📈 Мониторинг работы

### Логи индексации
```bash
# Смотрите детальную информацию при индексации
python run.py ingest
```

### Проверка базы ChromaDB
```python
# Проверить количество проиндексированных документов
python -c "
import chromadb
from src.app.config import settings
client = chromadb.PersistentClient(path=str(settings.INDEX_DIR))
collection = client.get_collection('admissions_docs')
print(f'Документов в базе: {collection.count()}')
"
```

## 🎯 Рекомендуемый workflow

1. **Подготовьте данные** в `src/data/seed/`
2. **Настройте `.env`** с API ключами
3. **Запустите индексацию**: `python run.py ingest`
4. **Запустите полную систему**: `python run.py full`
5. **Протестируйте** через Telegram бота

## 📞 Результат

После успешного запуска у вас будет:

- ✅ **Telegram бот** с умными ответами на вопросы о поступлении
- ✅ **FastAPI сервер** с REST API для интеграций
- ✅ **RAG система** с векторным поиском по вашим документам
- ✅ **Автоматическая обработка** JSON, TXT, PDF, DOCX файлов

**Бот будет отвечать на вопросы, используя информацию из ваших документов!** 🎉