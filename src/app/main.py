from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.db import init_db
from app.routers import programs, faqs, steps, documents, search
from app.seed_data import load_seed_data_to_db

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup
    logger.info("Запуск приложения...")
    try:
        await load_seed_data_to_db()
        logger.info("База данных инициализирована и данные загружены.")
    except Exception as e:
        logger.error(f"Ошибка при инициализации базы данных: {e}")
        raise
    
    yield
    
    # On shutdown
    logger.info("Завершение работы приложения.")

app = FastAPI(
    title="Admissions Agent API",
    description="API for the Admissions Agent Telegram Bot",
    version="0.1.0",
    lifespan=lifespan
)

# Добавляем CORS для возможности работы с фронтендом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене следует указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz", tags=["Health"])
async def health_check():
    """Проверка здоровья сервиса."""
    return {"status": "ok", "message": "Admissions Agent API is running"}

# Include routers
app.include_router(programs.router, prefix="/programs", tags=["Programs"])
app.include_router(faqs.router, prefix="/faqs", tags=["FAQs"])
app.include_router(steps.router, prefix="/steps", tags=["Application Steps"])
app.include_router(documents.router, prefix="/documents", tags=["Documents"])
app.include_router(search.router, prefix="/search", tags=["RAG Search"])
