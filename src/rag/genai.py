import google.genai as genai
from typing import List, Optional
import logging
import os
from pathlib import Path

from ..app.config import settings

logger = logging.getLogger(__name__)

# Настраиваем клиент - сначала пробуем с JSON credentials, затем с API key
client = None
try:
    # Проверяем, есть ли путь к JSON credentials
    if settings.GOOGLE_CREDENTIALS_PATH and Path(settings.GOOGLE_CREDENTIALS_PATH).exists():
        # Устанавливаем переменную окружения для использования JSON credentials
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.GOOGLE_CREDENTIALS_PATH
        
        # Используем Vertex AI с JSON credentials
        # Проверяем, что проект и локация заданы
        if not settings.GOOGLE_CLOUD_PROJECT:
            logger.warning("GOOGLE_CLOUD_PROJECT не задан в настройках. Пожалуйста, укажите его в настройках.")
            project_id = "your-project-id"  # Пользователь должен заменить на свой реальный ID проекта
        else:
            project_id = settings.GOOGLE_CLOUD_PROJECT
            
        location = settings.GOOGLE_CLOUD_LOCATION
        
        client = genai.Client(
            vertexai=True,
            project=project_id,
            location=location
        )
        logger.info("Gemini клиент инициализирован с JSON credentials")
    elif settings.GEMINI_API_KEY:
        # Резервный вариант: используем API key
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        logger.info("Gemini клиент инициализирован с API key")
    else:
        logger.error("Не найдены ни JSON credentials, ни API key для Gemini")
        
except Exception as e:
    logger.error(f"Ошибка инициализации Gemini клиента: {e}")
    client = None

# --- Prompt Templates ---

SYSTEM_PROMPT = """Ты — ассистент приёмной комиссии ALT University.

ПРАВИЛА ОТВЕТОВ:
1. Отвечай коротко, точно и дружелюбно на русском языке
2. Используй ТОЛЬКО факты из предоставленного КОНТЕКСТА
3. Если данных недостаточно — честно скажи об этом и предложи обратиться в приёмную комиссию
4. Форматируй списки и шаги аккуратно
5. Цифры, даты и суммы пиши точно как в КОНТЕКСТЕ
6. В конце ответа предлагай дополнительную помощь или переход к другим разделам

СТИЛЬ: Профессиональный, но дружелюбный. Используй эмодзи умеренно."""

USER_PROMPT_TEMPLATE = """ВОПРОС ПОЛЬЗОВАТЕЛЯ:
{user_question}

КОНТЕКСТ ИЗ БАЗЫ ЗНАНИЙ:
{context_chunks_with_sources}

ЗАДАЧА:
1) Ответь строго на основе КОНТЕКСТА; не придумывай информацию
2) Если вопрос про программы/стоимость/сроки/документы — приведи конкретные данные из КОНТЕКСТА
3) Если контекста недостаточно — предложи обратиться в приёмную комиссию
4) В конце предложи дополнительную помощь или использование кнопок меню"""


# --- Core Functions ---

def llm_answer(prompt: str, model: str = settings.GEMINI_DEFAULT_MODEL) -> str:
    """Генерирует ответ используя указанную модель Gemini."""
    if not client:
        logger.error("Gemini клиент не инициализирован")
        return "Извините, сервис временно недоступен. Пожалуйста, обратитесь в приёмную комиссию напрямую."
    
    try:
        # Добавляем системный промпт к каждому вызову
        full_prompt = f"{SYSTEM_PROMPT}\n\n{prompt}"
        
        logger.info(f"Отправляем запрос к модели {model}")
        r = client.models.generate_content(model=model, contents=full_prompt)
        
        if not r or not r.text:
            logger.warning("Модель вернула пустой ответ")
            return "Извините, не удалось получить ответ. Попробуйте переформулировать вопрос."
            
        logger.info("Ответ от модели получен успешно")
        return r.text
        
    except Exception as e:
        # Базовая обработка ошибок
        logger.error(f"Ошибка при генерации ответа: {e}")
        return "Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже или обратитесь в приёмную комиссию."


def embed_texts(texts: List[str], model: str = settings.GEMINI_EMBEDDING_MODEL) -> List[List[float]]:
    """Векторизует список текстов используя указанную модель эмбеддингов."""
    if not client:
        logger.error("Gemini клиент не инициализирован")
        return []
    
    if not texts:
        return []

    try:
        logger.info(f"Векторизация {len(texts)} текстов с помощью модели {model}")
        r = client.models.embed_content(model=model, contents=texts)
        
        if not r or not r.embeddings:
            logger.warning("Модель вернула пустые эмбеддинги")
            return []
            
        embeddings = []
        for i, e in enumerate(r.embeddings):
            if e and e.values:
                embeddings.append(e.values)
                # Проверяем качество векторизации
                if len(e.values) == 0:
                    logger.warning(f"Пустой вектор для текста {i}")
                elif all(v == 0 for v in e.values):
                    logger.warning(f"Нулевой вектор для текста {i}")
            else:
                logger.warning(f"Получен пустой эмбеддинг для текста {i}")
                embeddings.append([])
        
        logger.info(f"Успешно получено {len([e for e in embeddings if e])} качественных эмбеддингов из {len(embeddings)}")
        return embeddings
        
    except Exception as e:
        logger.error(f"Ошибка при векторизации: {e}")
        return []
