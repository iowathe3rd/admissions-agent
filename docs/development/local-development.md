# 🛠️ Локальная разработка

Руководство по настройке окружения для разработки и внесения изменений в проект.

## Настройка окружения разработчика

### Предварительная подготовка

1. **Системные требования**:
   - Python 3.11+
   - Poetry
   - Git
   - VS Code или PyCharm (рекомендуется)

2. **Клонирование репозитория**:
   ```bash
   git clone https://github.com/alt-ai/admissions-agent.git
   cd admissions-agent
   ```

3. **Настройка Poetry**:
   ```bash
   # Установка зависимостей
   poetry install
   
   # Активация виртуального окружения
   poetry shell
   
   # Проверка окружения
   poetry env info
   ```

### Конфигурация IDE

#### VS Code

Создайте `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "./.venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.ruffEnabled": true,
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length", "88"],
    "python.sortImports.args": ["--profile", "black"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    },
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        ".pytest_cache": true,
        "*.egg-info": true
    }
}
```

Рекомендуемые расширения для VS Code:
```json
{
    "recommendations": [
        "ms-python.python",
        "ms-python.black-formatter",
        "charliermarsh.ruff",
        "ms-python.isort",
        "ms-vscode.vscode-json",
        "redhat.vscode-yaml",
        "ms-python.pytest"
    ]
}
```

#### PyCharm

1. **Настройка интерпретатора**:
   - File → Settings → Project → Python Interpreter
   - Выберите Poetry environment

2. **Настройка кодстайла**:
   - File → Settings → Editor → Code Style → Python
   - Scheme: Black
   - Line length: 88

3. **Настройка линтеров**:
   - File → Settings → Tools → External Tools
   - Добавьте Ruff и Black

### Настройка pre-commit hooks

```bash
# Установка pre-commit
pip install pre-commit

# Установка хуков
pre-commit install
```

Создайте `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-merge-conflict

  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.0.270
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
```

## Структура разработки

### Workflow разработки

1. **Создание ветки**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Разработка**:
   - Внесите изменения
   - Следуйте стандартам кодирования
   - Пишите тесты

3. **Тестирование**:
   ```bash
   # Запуск тестов
   python run.py test
   
   # Запуск линтеров
   poetry run ruff check src/
   poetry run black --check src/
   poetry run isort --check-only src/
   ```

4. **Коммит**:
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

5. **Push и PR**:
   ```bash
   git push origin feature/your-feature-name
   # Создайте Pull Request на GitHub
   ```

### Конвенции коммитов

Используйте [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Новая функциональность
git commit -m "feat: add user authentication"

# Исправление бага
git commit -m "fix: resolve database connection issue"

# Документация
git commit -m "docs: update API documentation"

# Рефакторинг
git commit -m "refactor: simplify user service"

# Тесты
git commit -m "test: add unit tests for bot handlers"

# Стили кода
git commit -m "style: format code with black"

# Производительность
git commit -m "perf: optimize database queries"
```

## Разработка компонентов

### Добавление новых API эндпоинтов

1. **Создайте модель** в `src/app/models.py`:
   ```python
   class NewEntity(Base):
       __tablename__ = "new_entities"
       
       id = Column(Integer, primary_key=True, index=True)
       name = Column(String, nullable=False)
       description = Column(Text)
       created_at = Column(DateTime, default=datetime.utcnow)
   ```

2. **Создайте схемы** в `src/app/schemas.py`:
   ```python
   class NewEntityBase(BaseModel):
       name: str
       description: Optional[str] = None
   
   class NewEntityCreate(NewEntityBase):
       pass
   
   class NewEntity(NewEntityBase):
       id: int
       created_at: datetime
       
       class Config:
           from_attributes = True
   ```

3. **Создайте роутер** в `src/app/routers/new_entities.py`:
   ```python
   from fastapi import APIRouter, Depends, HTTPException
   from sqlalchemy.ext.asyncio import AsyncSession
   from app.db import get_session
   from app import models, schemas
   
   router = APIRouter(prefix="/new-entities", tags=["New Entities"])
   
   @router.get("/", response_model=List[schemas.NewEntity])
   async def get_new_entities(
       session: AsyncSession = Depends(get_session)
   ):
       result = await session.execute(select(models.NewEntity))
       return result.scalars().all()
   
   @router.post("/", response_model=schemas.NewEntity)
   async def create_new_entity(
       entity: schemas.NewEntityCreate,
       session: AsyncSession = Depends(get_session)
   ):
       db_entity = models.NewEntity(**entity.dict())
       session.add(db_entity)
       await session.commit()
       await session.refresh(db_entity)
       return db_entity
   ```

4. **Подключите роутер** в `src/app/main.py`:
   ```python
   from app.routers import new_entities
   
   app.include_router(new_entities.router)
   ```

### Добавление новых обработчиков бота

1. **Создайте обработчик** в `src/bot/handlers.py`:
   ```python
   @router.callback_query(F.data == "new_feature")
   async def new_feature_callback(callback: CallbackQuery):
       """Обработчик новой функции."""
       
       await callback.message.edit_text(
           "🆕 Новая функция!\n\nОписание функции...",
           reply_markup=back_to_menu_keyboard()
       )
       await callback.answer()
   ```

2. **Добавьте кнопку** в `src/bot/keyboards.py`:
   ```python
   def main_menu_keyboard() -> InlineKeyboardMarkup:
       keyboard = [
           # ... существующие кнопки
           [
               InlineKeyboardButton(
                   text="🆕 Новая функция",
                   callback_data="new_feature"
               )
           ]
       ]
       return InlineKeyboardMarkup(inline_keyboard=keyboard)
   ```

### Расширение RAG системы

1. **Добавление нового типа данных**:
   ```python
   # В src/rag/ingest.py
   async def _ingest_new_data_type(self):
       """Индексация нового типа данных."""
       
       data_file = Path("src/data/seed/new_data.json")
       
       with open(data_file, 'r', encoding='utf-8') as f:
           data = json.load(f)
       
       documents = []
       metadatas = []
       ids = []
       
       for item in data:
           text = self._format_new_data_text(item)
           
           documents.append(text)
           metadatas.append({
               "type": "new_data",
               "id": item["id"],
               "category": item.get("category", "general")
           })
           ids.append(f"new_data_{item['id']}")
       
       embeddings = await self._create_embeddings(documents)
       
       self.collection.add(
           documents=documents,
           embeddings=embeddings,
           metadatas=metadatas,
           ids=ids
       )
   ```

2. **Обновление основной функции индексации**:
   ```python
   async def ingest_data(self):
       # ... существующий код
       await self._ingest_new_data_type()  # Добавить эту строку
   ```

## Тестирование

### Структура тестов

```
src/tests/
├── conftest.py              # Фикстуры pytest
├── test_api.py             # Тесты API
├── test_bot.py             # Тесты бота
├── test_rag.py             # Тесты RAG
├── test_models.py          # Тесты моделей
├── integration/            # Интеграционные тесты
│   ├── test_full_flow.py
│   └── test_api_bot.py
└── fixtures/               # Тестовые данные
    ├── test_data.json
    └── mock_responses.py
```

### Написание тестов

#### Тесты API

```python
import pytest
from httpx import AsyncClient
from src.app.main import app

@pytest.mark.asyncio
async def test_get_programs():
    """Тест получения списка программ."""
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/programs/")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_create_program():
    """Тест создания новой программы."""
    
    program_data = {
        "name": "Test Program",
        "description": "Test description",
        "duration": "4 года",
        "cost": "100000"
    }
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/programs/", json=program_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Program"
```

#### Тесты бота

```python
import pytest
from unittest.mock import AsyncMock, patch
from aiogram.types import Message, User, Chat
from src.bot.handlers import start_handler

@pytest.fixture
def mock_message():
    """Мок объект сообщения."""
    message = AsyncMock(spec=Message)
    message.from_user = User(id=123, is_bot=False, first_name="Test")
    message.chat = Chat(id=123, type="private")
    return message

@pytest.mark.asyncio
async def test_start_handler(mock_message):
    """Тест команды /start."""
    
    await start_handler(mock_message)
    
    mock_message.answer.assert_called_once()
    args = mock_message.answer.call_args[0]
    assert "Здравствуйте, Test!" in args[0]

@pytest.mark.asyncio
@patch('src.bot.handlers.retrieve_context')
@patch('src.bot.handlers.llm_answer')
async def test_rag_response(mock_llm, mock_retrieve, mock_message):
    """Тест RAG ответа."""
    
    mock_message.text = "Сколько стоит обучение?"
    mock_retrieve.return_value = [{"content": "Стоимость 100000 рублей"}]
    mock_llm.return_value = "Стоимость обучения составляет 100000 рублей."
    
    from src.bot.handlers import text_message_handler
    await text_message_handler(mock_message)
    
    mock_retrieve.assert_called_once_with("Сколько стоит обучение?")
    mock_llm.assert_called_once()
    mock_message.answer.assert_called_once()
```

#### Тесты RAG

```python
import pytest
from unittest.mock import patch, AsyncMock
from src.rag.retriever import retrieve_context
from src.rag.genai import llm_answer

@pytest.mark.asyncio
@patch('src.rag.retriever.ContextRetriever')
async def test_retrieve_context(mock_retriever_class):
    """Тест поиска контекста."""
    
    mock_retriever = AsyncMock()
    mock_retriever_class.return_value = mock_retriever
    
    mock_retriever.retrieve_context.return_value = [
        {
            'content': 'Test content',
            'metadata': {'type': 'program'},
            'similarity': 0.9
        }
    ]
    
    result = await retrieve_context("test query")
    
    assert len(result) == 1
    assert result[0]['content'] == 'Test content'
    assert result[0]['similarity'] == 0.9

@pytest.mark.asyncio
@patch('src.rag.genai.get_gemini_client')
async def test_llm_answer(mock_get_client):
    """Тест генерации ответа."""
    
    mock_client = AsyncMock()
    mock_get_client.return_value = mock_client
    
    mock_client.generate_answer.return_value = "Test response"
    
    result = await llm_answer("Test prompt")
    
    assert result == "Test response"
    mock_client.generate_answer.assert_called_once_with("Test prompt", None)
```

### Фикстуры для тестов

```python
# conftest.py
import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.app.models import Base
from src.app.db import get_session
from src.app.main import app

@pytest.fixture(scope="session")
def event_loop():
    """Создает event loop для тестов."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def test_session():
    """Создает тестовую сессию базы данных."""
    
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    TestSessionLocal = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with TestSessionLocal() as session:
        yield session

@pytest.fixture
def override_get_session(test_session):
    """Переопределяет get_session для тестов."""
    
    app.dependency_overrides[get_session] = lambda: test_session
    yield
    app.dependency_overrides.clear()
```

## Отладка

### Настройка логирования для разработки

```python
# В config.py для разработки
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('debug.log')
    ]
)

# Настройка логгеров для разных компонентов
logging.getLogger('src.bot').setLevel(logging.DEBUG)
logging.getLogger('src.rag').setLevel(logging.DEBUG)
logging.getLogger('src.app').setLevel(logging.INFO)

# Отключение verbose логов внешних библиотек
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('chromadb').setLevel(logging.WARNING)
```

### Использование debugger

```python
# Добавление точек останова
import pdb; pdb.set_trace()

# Или с ipdb (лучший интерфейс)
import ipdb; ipdb.set_trace()

# Или с VS Code
import debugpy
debugpy.breakpoint()
```

### Профилирование производительности

```python
# Простое профилирование времени
import time
import functools

def timing_decorator(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f} seconds")
        return result
    return wrapper

@timing_decorator
async def slow_function():
    # Ваш код
    pass
```

### Мониторинг в реальном времени

```python
# Простой мониторинг ресурсов
import psutil
import asyncio

async def monitor_resources():
    """Мониторит использование ресурсов."""
    
    while True:
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        
        print(f"CPU: {cpu}%, Memory: {memory}%")
        
        await asyncio.sleep(5)

# Запуск мониторинга
asyncio.create_task(monitor_resources())
```

## Полезные команды для разработки

### Poetry команды

```bash
# Управление зависимостями
poetry add package_name              # Добавить зависимость
poetry add --group dev package_name  # Добавить dev-зависимость
poetry remove package_name           # Удалить зависимость
poetry update                        # Обновить все зависимости
poetry show                          # Показать установленные пакеты

# Окружение
poetry env info                      # Информация об окружении
poetry env list                      # Список окружений
poetry shell                         # Активировать окружение
```

### Работа с базой данных

```bash
# Создание миграций
alembic revision --autogenerate -m "Description"

# Применение миграций
alembic upgrade head

# Откат миграций
alembic downgrade -1

# История миграций
alembic history
```

### Запуск в режиме разработки

```bash
# API с автоперезагрузкой
python run.py api

# Бот с детальным логированием
LOG_LEVEL=DEBUG python run.py bot

# Только индексация данных
python run.py ingest

# Полный запуск для тестирования
python run.py full
```

### Docker для разработки

```bash
# Сборка образа для разработки
docker build -t admissions-agent:dev .

# Запуск контейнера с монтированием кода
docker run -v $(pwd):/app -p 8000:8000 admissions-agent:dev

# Docker Compose для разработки
docker-compose -f docker-compose.dev.yml up
```

## Решение проблем

### Типичные проблемы и решения

1. **Проблемы с зависимостями**:
   ```bash
   poetry cache clear pypi --all
   poetry install --no-cache
   ```

2. **Проблемы с базой данных**:
   ```bash
   # Пересоздание базы
   rm data/bot.db
   python run.py ingest
   ```

3. **Проблемы с векторным индексом**:
   ```bash
   # Очистка индекса
   rm -rf src/rag/index/
   python run.py ingest
   ```

4. **Проблемы с импортами**:
   ```bash
   # Проверка PYTHONPATH
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```

### Диагностика

```bash
# Проверка конфигурации
python -c "from src.app.config import settings; print(settings.dict())"

# Проверка подключения к API
python -c "from src.rag.genai import test_connection; print(test_connection())"

# Проверка базы данных
python -c "from src.app.db import test_connection; import asyncio; asyncio.run(test_connection())"
```

Этот гайд поможет вам эффективно разрабатывать и отлаживать проект Admissions Agent.