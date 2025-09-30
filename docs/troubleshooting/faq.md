# ❓ Часто задаваемые вопросы

Ответы на самые распространенные вопросы по использованию, настройке и разработке Admissions Agent.

## 🚀 Установка и запуск

### Q: Как быстро запустить проект?

**A:** Самый простой способ:

```bash
# 1. Клонируйте репозиторий
git clone https://github.com/alt-ai/admissions-agent.git
cd admissions-agent

# 2. Установите зависимости
poetry install

# 3. Настройте .env файл
cp .env.example .env
# Отредактируйте .env, добавив ваши API ключи

# 4. Запустите все сразу
python run.py full
```

### Q: Где получить API ключи?

**A:** 
- **Telegram Bot Token**: Создайте бота через [@BotFather](https://t.me/BotFather)
- **Google Gemini API**: Получите на [Google AI Studio](https://aistudio.google.com/)

### Q: Что делать если `poetry` не найден?

**A:** Установите Poetry:

```bash
# Linux/macOS
curl -sSL https://install.python-poetry.org | python3 -

# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

# Через pip (альтернатива)
pip install poetry
```

### Q: Ошибка "Python 3.10+ required"

**A:** Обновите Python:

```bash
# Ubuntu
sudo apt update
sudo apt install python3.11

# macOS
brew install python@3.11

# Или используйте pyenv
pyenv install 3.11.0
pyenv global 3.11.0
```

## 🤖 Работа с ботом

### Q: Бот не отвечает на сообщения

**A:** Проверьте несколько вещей:

1. **Токен корректен**:
   ```bash
   # Проверьте токен в .env файле
   grep TELEGRAM_BOT_TOKEN .env
   ```

2. **Бот запущен**:
   ```bash
   # Проверьте логи бота
   python run.py bot
   ```

3. **Бот добавлен в чат**:
   - Найдите бота по username
   - Отправьте `/start`

### Q: Бот отвечает "Извините, произошла ошибка"

**A:** Это обычно проблема с RAG системой:

1. **Проверьте Gemini API ключ**:
   ```bash
   python -c "from src.rag.genai import test_connection; print(test_connection())"
   ```

2. **Переиндексируйте данные**:
   ```bash
   python run.py ingest
   ```

3. **Проверьте логи**:
   ```bash
   tail -f logs/app.log
   ```

### Q: Как добавить новые команды боту?

**A:** Добавьте обработчик в `src/bot/handlers.py`:

```python
@router.message(Command("mycommand"))
async def my_command_handler(message: Message):
    await message.answer("Ответ на вашу команду!")
```

### Q: Можно ли изменить приветственное сообщение?

**A:** Да, отредактируйте функцию `start_handler` в `src/bot/handlers.py`:

```python
welcome_text = f"""
👋 Ваше новое приветствие, {user_name}!

Здесь ваш текст...
"""
```

## 🌐 API вопросы

### Q: API недоступен на localhost:8000

**A:** Проверьте:

1. **Порт свободен**:
   ```bash
   lsof -i :8000
   ```

2. **API запущен**:
   ```bash
   python run.py api
   ```

3. **Firewall настройки**:
   ```bash
   # Linux
   sudo ufw allow 8000
   ```

### Q: Как получить список всех эндпоинтов?

**A:** После запуска API идите на:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Q: Как добавить аутентификацию к API?

**A:** Добавьте middleware в `src/app/main.py`:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def verify_token(token: str = Depends(security)):
    if token.credentials != "your-secret-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return token

# Защитите эндпоинты
@app.get("/protected", dependencies=[Depends(verify_token)])
async def protected_endpoint():
    return {"message": "Protected data"}
```

## 🧠 RAG и AI

### Q: Как улучшить качество ответов AI?

**A:** Несколько способов:

1. **Обновите данные** в `src/data/seed/`:
   - Добавьте больше FAQ
   - Улучшите описания программ
   - Переиндексируйте: `python run.py ingest`

2. **Настройте промпты** в `src/rag/genai.py`:
   ```python
   # Измените температуру для более консервативных ответов
   temperature = 0.1  # вместо 0.3
   ```

3. **Увеличьте контекст**:
   ```env
   RAG_MAX_CHUNKS=7  # вместо 5
   ```

### Q: RAG не находит релевантную информацию

**A:** Проверьте несколько вещей:

1. **Данные проиндексированы**:
   ```bash
   # Проверьте наличие индекса
   ls -la src/rag/index/
   
   # Переиндексируйте
   python run.py ingest
   ```

2. **Понизьте порог схожести**:
   ```env
   RAG_SIMILARITY_THRESHOLD=0.2  # вместо 0.3
   ```

3. **Проверьте формат данных** в `src/data/seed/`.

### Q: Как сменить модель Gemini?

**A:** Обновите настройки в `.env`:

```env
# Для более быстрых ответов
GEMINI_DEFAULT_MODEL="gemini-2.0-flash-exp"

# Для более качественных ответов
GEMINI_DEFAULT_MODEL="gemini-2.0-pro-exp"

# Для экономии (устаревшие модели)
GEMINI_DEFAULT_MODEL="gemini-1.5-flash"
```

### Q: Ошибка "API quota exceeded"

**A:** У вас превышена квота Gemini API:

1. **Проверьте лимиты** на [Google AI Studio](https://makersuite.google.com/)
2. **Добавьте обработку ошибок**:
   ```python
   # В src/rag/genai.py
   try:
       response = await self.client.generate_content(...)
   except QuotaExceededError:
       return "Временно недоступно. Попробуйте позже."
   ```

## 🗄️ База данных

### Q: Как сбросить базу данных?

**A:** Удалите файл базы данных:

```bash
# SQLite
rm data/bot.db

# Затем перезапустите приложение
python run.py api
```

### Q: Как перейти на PostgreSQL?

**A:** Обновите `DATABASE_URL` в `.env`:

```env
DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/admissions_bot"
```

Установите зависимости:
```bash
poetry add asyncpg psycopg2-binary
```

### Q: Как сделать бэкап данных?

**A:** Для SQLite:

```bash
# Простое копирование
cp data/bot.db data/bot_backup_$(date +%Y%m%d).db

# Или экспорт в SQL
sqlite3 data/bot.db .dump > backup.sql
```

Для PostgreSQL:
```bash
pg_dump -h localhost -U user -d admissions_bot > backup.sql
```

## 🐳 Docker

### Q: Как запустить в Docker?

**A:** Используйте Docker Compose:

```bash
# Настройте .env файл
cp .env.example .env

# Запустите все сервисы
docker-compose up --build
```

### Q: Ошибка "port already in use"

**A:** Измените порт в `docker-compose.yml`:

```yaml
services:
  api:
    ports:
      - "8001:8000"  # вместо 8000:8000
```

### Q: Как обновить данные в контейнере?

**A:** Перестройте образ:

```bash
# После изменения данных в src/data/seed/
docker-compose down
docker-compose up --build
```

## 🔧 Настройка и конфигурация

### Q: Где находятся все настройки?

**A:** Настройки разбросаны по нескольким местам:

1. **Переменные окружения**: `.env` файл
2. **Настройки приложения**: `src/app/config.py`
3. **Настройки Poetry**: `pyproject.toml`
4. **Docker настройки**: `docker-compose.yml`

### Q: Как изменить порт API?

**A:** В `.env` файле:

```env
API_PORT=8001
```

Или при запуске:
```bash
uvicorn src.app.main:app --host 0.0.0.0 --port 8001
```

### Q: Как настроить логирование?

**A:** В `src/app/config.py`:

```python
import logging

# Базовый уровень
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR

# Файлы логов
logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Консоль
        logging.FileHandler('logs/app.log')  # Файл
    ]
)
```

## 📊 Производительность

### Q: Бот отвечает медленно

**A:** Несколько способов ускорения:

1. **Используйте более быструю модель**:
   ```env
   GEMINI_DEFAULT_MODEL="gemini-2.0-flash-exp"
   ```

2. **Уменьшите контекст**:
   ```env
   RAG_MAX_CHUNKS=3
   ```

3. **Включите кеширование** (если настроено):
   ```env
   ENABLE_CACHE=true
   ```

### Q: API потребляет много памяти

**A:** Оптимизируйте настройки:

1. **Ограничьте пул соединений БД**:
   ```python
   # В src/app/db.py
   engine = create_async_engine(
       DATABASE_URL,
       pool_size=5,  # вместо 20
       max_overflow=10  # вместо 30
   )
   ```

2. **Используйте более легкую модель эмбеддингов**.

3. **Настройте сборщик мусора**:
   ```python
   import gc
   gc.set_threshold(100, 10, 10)
   ```

## 🧪 Тестирование

### Q: Как запустить тесты?

**A:** Используйте команду:

```bash
# Все тесты
python run.py test

# Конкретный файл
poetry run pytest src/tests/test_api.py -v

# С покрытием
poetry run pytest --cov=src --cov-report=html
```

### Q: Тесты падают с ошибками базы данных

**A:** Убедитесь что используется тестовая база:

```python
# В conftest.py
@pytest.fixture
async def test_session():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",  # В памяти
        echo=False
    )
    # ...
```

### Q: Как добавить новые тесты?

**A:** Создайте файл в `src/tests/`:

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_my_feature():
    # Ваш тест
    assert True
```

## 🚀 Развертывание

### Q: Как развернуть на продакшн сервере?

**A:** Рекомендуемые шаги:

1. **Используйте Docker**:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

2. **Настройте reverse proxy** (nginx):
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       
       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

3. **Используйте PostgreSQL** вместо SQLite.

4. **Настройте мониторинг**.

### Q: Как настроить SSL/HTTPS?

**A:** Используйте Let's Encrypt с nginx:

```bash
# Установите certbot
sudo apt install certbot python3-certbot-nginx

# Получите сертификат
sudo certbot --nginx -d yourdomain.com

# Настройка автообновления
sudo crontab -e
# Добавьте: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 🔍 Отладка

### Q: Как включить детальные логи?

**A:** Установите уровень логирования:

```bash
# При запуске
LOG_LEVEL=DEBUG python run.py bot

# Или в .env
LOG_LEVEL=DEBUG
```

### Q: Где смотреть логи ошибок?

**A:** Логи находятся в:

- **Консоль**: При запуске `python run.py ...`
- **Файлы**: `logs/app.log` (если настроено)
- **Docker**: `docker-compose logs -f`

### Q: Как отладить RAG запросы?

**A:** Добавьте детальное логирование в `src/rag/retriever.py`:

```python
logger.info(f"Запрос: {query}")
logger.info(f"Найдено фрагментов: {len(context_chunks)}")
for i, chunk in enumerate(context_chunks):
    logger.info(f"Фрагмент {i}: {chunk['similarity']:.3f} - {chunk['content'][:100]}...")
```

## 💡 Лучшие практики

### Q: Как структурировать новые функции?

**A:** Следуйте принципам:

1. **Один компонент = одна ответственность**
2. **Используйте асинхронные функции**
3. **Добавляйте типы данных (type hints)**
4. **Пишите тесты**
5. **Документируйте изменения**

### Q: Как обновить проект на новую версию?

**A:** 

```bash
# 1. Сделайте бэкап
cp -r . ../backup_$(date +%Y%m%d)

# 2. Обновите код
git pull origin main

# 3. Обновите зависимости
poetry install

# 4. Примените миграции БД
alembic upgrade head

# 5. Переиндексируйте данные
python run.py ingest

# 6. Перезапустите сервисы
python run.py full
```

### Q: Что делать если ничего не работает?

**A:** Последовательность диагностики:

1. **Проверьте .env файл** - корректны ли API ключи?
2. **Проверьте логи** - есть ли ошибки?
3. **Переустановите зависимости** - `poetry install --no-cache`
4. **Пересоздайте базу данных** - удалите и переиндексируйте
5. **Проверьте порты** - свободны ли 8000?
6. **Создайте issue** на GitHub с описанием проблемы

Если вопроса нет в этом FAQ, создайте issue в GitHub репозитории!