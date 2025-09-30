# ⚡ Быстрый старт - Admissions Agent

## 🚀 Запуск за 5 минут

### 1. Установка
```bash
cd /home/baur/home/dev/github.com/alt-ai/admissions-agent
poetry install
```

### 2. Настройка API ключей
```bash
# Создаем .env файл
cat > .env << EOF
TELEGRAM_BOT_TOKEN=your_bot_token_here
GEMINI_API_KEY=your_gemini_key_here
EOF
```

### 3. Запуск
```bash
# Запускаем всё сразу (RAG + Bot + API)
python run.py full
```

## 📄 Куда класть данные для RAG

### Папка данных: `src/data/seed/`

```
src/data/seed/
├── 📝 programs.json      # Программы обучения  
├── ❓ faqs.json         # Вопросы-ответы
├── 📋 documents.json    # Документы для поступления
├── 📊 steps.json        # Шаги поступления
├── 📄 your_file.txt     # 🆕 Любые TXT файлы
├── 📄 handbook.pdf      # 🆕 Любые PDF документы  
└── 📝 rules.docx        # 🆕 Любые DOCX файлы
```

### Что добавлять:

#### ✅ **JSON файлы** (структурированные данные)
```json
// programs.json
[
  {
    "name": "Информатика", 
    "cost": 250000,
    "description": "Программа готовит программистов"
  }
]

// faqs.json  
[
  {
    "question": "Когда подавать документы?",
    "answer": "С 20 июня по 25 июля"
  }
]
```

#### ✅ **TXT файлы** (текстовая информация)
```txt
# admission_info.txt
Общая информация о поступлении в ALT University.
Адрес: г. Москва, ул. Университетская, д. 1
Телефон: +7 (495) 123-45-67
```

#### ✅ **PDF/DOCX** (документы)
- Положите любые PDF или DOCX файлы
- Система автоматически извлечет текст

## 🔄 Процесс обновления данных

### Добавили новые файлы?
```bash
# 1. Скопируйте файлы в src/data/seed/
cp your_new_document.pdf src/data/seed/

# 2. Переиндексируйте данные
python run.py ingest

# 3. Готово! Бот знает новую информацию
```

## 🧪 Проверка работы

### Быстрый тест
```bash
# Проверяем что всё работает
python -c "
from src.app.config import settings
print('✅ Конфиг загружен')
from src.rag.document_loader import DocumentLoader  
print('✅ Загрузчик документов готов')
print('🎯 Система готова к работе!')
"
```

### Тест RAG через консоль
```python
python -c "
from src.rag.retriever import retrieve_context
results = retrieve_context('программы обучения')
print(f'Найдено {len(results)} релевантных документов')
for r in results[:2]:
    print(f'- {r.source}: {r.text[:100]}...')
"
```

## 📱 Использование бота

1. **Запустите**: `python run.py full`
2. **Найдите бота** в Telegram по токену
3. **Отправьте** `/start`
4. **Задавайте вопросы**:
   - "Какие программы обучения есть?"
   - "Сколько стоит обучение?"
   - "Когда подавать документы?"
   - "Какие нужны документы?"

## 🔍 Примеры данных

В проекте уже есть примеры:

- ✅ `programs.json` - программы обучения
- ✅ `faqs.json` - часто задаваемые вопросы  
- ✅ `documents.json` - необходимые документы
- ✅ `steps.json` - шаги поступления
- ✅ `admission_info.txt` - общая информация
- ✅ `admission_rules.txt` - правила приема

**Просто замените их своими данными!**

## ⚡ Команды для управления

```bash
python run.py ingest    # Только индексация данных
python run.py bot       # Только Telegram бот  
python run.py api       # Только FastAPI сервер
python run.py test      # Запуск тестов
python run.py full      # Всё сразу (рекомендуется)
```

## 🎯 Результат

После запуска `python run.py full` у вас будет:

- 🤖 **Умный Telegram бот** отвечающий на вопросы о поступлении
- 🔍 **RAG система** ищущая ответы в ваших документах  
- 🌐 **API сервер** для интеграций (http://localhost:8000)
- 📊 **Автоматическая обработка** всех форматов файлов

**Бот будет отвечать на основе ВАШИХ документов!** 🎉

---

💡 **Совет**: Начните с примеров данных, проверьте что всё работает, затем замените своими файлами и переиндексируйте.