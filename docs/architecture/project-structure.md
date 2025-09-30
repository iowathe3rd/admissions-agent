# 📁 Структура проекта

Подробное описание организации кода и файлов в проекте Admissions Agent.

## Общая структура

```
admissions-agent/
├── 📄 README.md              # Основная документация
├── 📄 pyproject.toml         # Конфигурация Poetry и проекта
├── 📄 poetry.lock            # Зафиксированные версии зависимостей
├── 📄 .env.example           # Пример переменных окружения
├── 📄 .env                   # Переменные окружения (не в Git)
├── 📄 run.py                 # Скрипт запуска всех компонентов
├── 📄 Dockerfile             # Контейнеризация приложения
├── 📄 docker-compose.yml     # Локальное развертывание
├── 📄 pytest.ini            # Конфигурация тестов
├── 📄 Makefile              # Автоматизация команд
├── 📄 IMPROVEMENTS.md        # Планы развития
├── 📁 docs/                  # Документация
├── 📁 src/                   # Исходный код
├── 📁 scripts/               # Утилиты и скрипты
├── 📁 logs/                  # Файлы логов (создается автоматически)
└── 📁 data/                  # Данные приложения (создается автоматически)
```

## Исходный код (`src/`)

### Общая структура `src/`

```
src/
├── 📄 __init__.py
├── 📁 app/                   # FastAPI приложение
├── 📁 bot/                   # Telegram bot
├── 📁 rag/                   # RAG система и AI
├── 📁 data/                  # Управление данными
└── 📁 tests/                 # Тесты
```

## FastAPI приложение (`src/app/`)

```
src/app/
├── 📄 __init__.py
├── 📄 main.py                # Основной файл FastAPI приложения
├── 📄 config.py              # Конфигурация и настройки
├── 📄 db.py                  # Настройка базы данных
├── 📄 models.py              # SQLAlchemy модели
├── 📄 schemas.py             # Pydantic схемы для API
├── 📄 seed_data.py          # Загрузка начальных данных
└── 📁 routers/               # API маршруты
    ├── 📄 __init__.py
    ├── 📄 programs.py        # Эндпоинты программ обучения
    ├── 📄 faqs.py           # Эндпоинты FAQ
    ├── 📄 steps.py          # Эндпоинты шагов поступления
    ├── 📄 documents.py      # Эндпоинты документов
    └── 📄 search.py         # Эндпоинты поиска и RAG
```

### Описание файлов `app/`

#### `main.py`
```python
# Основная точка входа FastAPI приложения
# - Создание FastAPI инстанса
# - Подключение роутеров
# - Настройка CORS
# - Lifecycle события (startup/shutdown)
```

#### `config.py`
```python
# Централизованная конфигурация
# - Загрузка переменных окружения
# - Настройки базы данных
# - AI модели и API ключи
# - Валидация конфигурации
```

#### `models.py`
```python
# SQLAlchemy модели для базы данных
# - Program: Программы обучения
# - FAQ: Часто задаваемые вопросы
# - Step: Шаги поступления
# - Document: Требуемые документы
# - Interaction: Логи взаимодействий
```

#### `schemas.py`
```python
# Pydantic схемы для валидации API
# - Входные схемы (Create, Update)
# - Выходные схемы (Response)
# - Базовые схемы
```

## Telegram Bot (`src/bot/`)

```
src/bot/
├── 📄 __init__.py
├── 📄 runner.py              # Запуск бота
├── 📄 handlers.py            # Обработчики сообщений
├── 📄 keyboards.py           # Клавиатуры и кнопки
└── 📄 middleware.py          # Middleware для бота (опционально)
```

### Описание файлов `bot/`

#### `runner.py`
```python
# Основной файл запуска бота
# - Инициализация aiogram Bot и Dispatcher
# - Регистрация handlers и middleware
# - Настройка polling/webhook
# - Graceful shutdown
```

#### `handlers.py`
```python
# Обработчики команд и сообщений
# - /start, /help команды
# - Обработка текстовых сообщений
# - Callback query handlers
# - RAG интеграция
```

#### `keyboards.py`
```python
# Инлайн клавиатуры для навигации
# - Главное меню
# - Меню программ
# - Навигационные кнопки
# - Динамические клавиатуры
```

## RAG система (`src/rag/`)

```
src/rag/
├── 📄 __init__.py
├── 📄 genai.py               # Интеграция с Google Gemini
├── 📄 retriever.py           # Поиск и извлечение контекста
├── 📄 ingest.py             # Индексация данных
├── 📁 index/                 # ChromaDB индексы (создается автоматически)
└── 📁 prompts/               # Промпт шаблоны (опционально)
```

### Описание файлов `rag/`

#### `genai.py`
```python
# Интеграция с Google Gemini API
# - Инициализация клиента
# - Функции генерации ответов
# - Промпт инжиниринг
# - Обработка ошибок AI
```

#### `retriever.py`
```python
# Векторный поиск и извлечение контекста
# - Семантический поиск в ChromaDB
# - Фильтрация по релевантности
# - Формирование контекста для AI
# - Ранжирование результатов
```

#### `ingest.py`
```python
# Индексация документов и данных
# - Загрузка seed данных
# - Создание эмбеддингов
# - Сохранение в векторную базу
# - Инкрементальная индексация
```

## Управление данными (`src/data/`)

```
src/data/
├── 📄 __init__.py
└── 📁 seed/                  # Начальные данные
    ├── 📄 programs.json      # Программы обучения
    ├── 📄 faqs.json         # Часто задаваемые вопросы
    ├── 📄 steps.json        # Шаги поступления
    └── 📄 documents.json    # Требуемые документы
```

### Формат seed данных

#### `programs.json`
```json
[
  {
    "id": 1,
    "name": "Компьютерные науки",
    "description": "Бакалавриат по информатике...",
    "duration": "4 года",
    "cost": "500000",
    "requirements": ["ЕГЭ по математике", "ЕГЭ по информатике"],
    "category": "bachelor"
  }
]
```

#### `faqs.json`
```json
[
  {
    "id": 1,
    "question": "Как подать документы?",
    "answer": "Документы можно подать...",
    "category": "admission",
    "keywords": ["документы", "подача", "поступление"]
  }
]
```

## Тесты (`src/tests/`)

```
src/tests/
├── 📄 __init__.py
├── 📄 conftest.py            # Pytest конфигурация и фикстуры
├── 📄 test_api.py           # Тесты FastAPI эндпоинтов
├── 📄 test_bot.py           # Тесты Telegram бота
├── 📄 test_rag.py           # Тесты RAG системы
├── 📄 test_models.py        # Тесты database моделей
└── 📁 fixtures/              # Тестовые данные
    ├── 📄 test_programs.json
    ├── 📄 test_faqs.json
    └── 📄 sample_responses.json
```

## Документация (`docs/`)

```
docs/
├── 📄 README.md              # Главная страница документации
├── 📄 installation.md       # Установка и настройка
├── 📄 quick-start.md        # Быстрый старт
├── 📄 configuration.md      # Конфигурация
├── 📁 architecture/          # Архитектурная документация
├── 📁 development/           # Руководство разработчика
├── 📁 components/            # Описание компонентов
├── 📁 api/                   # API документация
├── 📁 deployment/            # Развертывание
├── 📁 data/                  # Управление данными
├── 📁 admin/                 # Администрирование
└── 📁 troubleshooting/       # Решение проблем
```

## Вспомогательные файлы

### `pyproject.toml`
```toml
# Основная конфигурация проекта
# - Метаданные проекта
# - Зависимости (dependencies)
# - Инструменты разработки (dev-dependencies)
# - Настройки линтеров и форматеров
```

### `run.py`
```python
# Универсальный скрипт запуска
# - run.py ingest  (индексация)
# - run.py api     (FastAPI сервер)
# - run.py bot     (Telegram бот)
# - run.py test    (тесты)
# - run.py full    (полный запуск)
```

### `docker-compose.yml`
```yaml
# Локальное развертывание
# - rag-ingest: Индексация данных
# - api: FastAPI сервер
# - bot: Telegram бот
# - Зависимости между сервисами
```

### `Dockerfile`
```dockerfile
# Контейнеризация приложения
# - Multi-stage build
# - Оптимизация размера образа
# - Безопасность (non-root user)
```

## Конвенции именования

### Файлы и папки
- **snake_case** для Python файлов: `user_service.py`
- **kebab-case** для конфигурационных файлов: `docker-compose.yml`
- **lowercase** для папок: `src/app/routers/`

### Python код
- **PascalCase** для классов: `UserService`, `DatabaseModel`
- **snake_case** для функций и переменных: `get_user_by_id`
- **UPPER_CASE** для констант: `MAX_RETRIES`, `API_VERSION`

### API эндпоинты
- **REST** стиль: `/programs/`, `/faqs/{faq_id}`
- **Множественное число** для коллекций: `/programs/`
- **Версионирование**: `/api/v1/programs/`

## Паттерны организации кода

### Repository Pattern
```python
# Разделение бизнес-логики и доступа к данным
class ProgramRepository:
    async def get_all(self) -> List[Program]: ...
    async def get_by_id(self, id: int) -> Program: ...
    async def create(self, program: ProgramCreate) -> Program: ...
```

### Service Layer
```python
# Бизнес-логика в отдельном слое
class ProgramService:
    def __init__(self, repo: ProgramRepository):
        self.repo = repo
    
    async def get_program_with_details(self, id: int) -> ProgramDetail: ...
```

### Dependency Injection
```python
# FastAPI DI для внедрения зависимостей
@app.get("/programs/{program_id}")
async def get_program(
    program_id: int,
    service: ProgramService = Depends(get_program_service)
):
    return await service.get_program_with_details(program_id)
```

## Миграции и версионирование

### Database Migrations
```
migrations/
├── versions/
│   ├── 001_initial_schema.py
│   ├── 002_add_interactions_table.py
│   └── 003_add_user_preferences.py
└── alembic.ini
```

### API Versioning
```python
# Версионирование через роутеры
app.include_router(v1_router, prefix="/api/v1")
app.include_router(v2_router, prefix="/api/v2")
```

## Плагинная архитектура (будущее развитие)

```
src/plugins/
├── __init__.py
├── base.py                   # Базовый класс плагина
├── admission_calculator/     # Плагин калькулятора шансов
├── document_parser/          # Плагин парсинга документов
└── notification_sender/      # Плагин уведомлений
```

Эта структура обеспечивает:
- **Модульность**: Четкое разделение компонентов
- **Масштабируемость**: Легкость добавления новых функций
- **Тестируемость**: Изолированные модули для тестирования
- **Поддерживаемость**: Понятная организация кода