import google.genai as genai
from typing import List
import logging

from app.config import settings

logger = logging.getLogger(__name__)

# Настраиваем клиент
try:
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    logger.info("Gemini клиент инициализирован успешно")
except Exception as e:
    logger.error(f"Ошибка инициализации Gemini клиента: {e}")
    # В реальном приложении стоит обрабатывать это более изящно
    client = None

# --- Prompt Templates ---

SYSTEM_PROMPT = """
Ты — ассистент приёмной комиссии ALT University.

ПРАВИЛА ОТВЕТОВ:
1. Отвечай коротко, точно и дружелюбно на русском языке
2. Используй ТОЛЬКО факты из предоставленного КОНТЕКСТА
3. Если данных недостаточно — честно скажи об этом и предложи обратиться в приёмную комиссию
4. Форматируй списки и шаги аккуратно
5. Цифры, даты и суммы пиши точно как в КОНТЕКСТЕ
6. В конце ответа предлагай дополнительную помощь или переход к другим разделам

СТИЛЬ: Профессиональный, но дружелюбный. Используй эмодзи умеренно.
"""

USER_PROMPT_TEMPLATE = """
ВОПРОС ПОЛЬЗОВАТЕЛЯ:
{{user_question}}

КОНТЕКСТ ИЗ БАЗЫ ЗНАНИЙ:
{{context_chunks_with_sources}}

ЗАДАЧА:
1) Ответь строго на основе КОНТЕКСТА; не придумывай информацию
2) Если вопрос про программы/стоимость/сроки/документы — приведи конкретные данные из КОНТЕКСТА
3) Если контекста недостаточно — предложи обратиться в приёмную комиссию
4) В конце предложи дополнительную помощь или использование кнопок меню
"""

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
        return f"Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже или обратитесь в приёмную комиссию."

def embed_texts(texts: List[str], model: str = settings.GEMINI_EMBEDDING_MODEL) -> List[List[float]]:
    """Векторизует список текстов используя указанную модель эмбеддингов."""
    if not client:
        logger.error("Gemini клиент не инициализирован")
        return []
    
    try:
        logger.info(f"Векторизация {len(texts)} текстов с помощью модели {model}")
        r = client.models.embed_content(model=model, contents=texts)
        
        if not r or not r.embeddings:
            logger.warning("Модель вернула пустые эмбеддинги")
            return []
            
        embeddings = []
        for e in r.embeddings:
            if e and e.values:
                embeddings.append(e.values)
            else:
                logger.warning("Получен пустой эмбеддинг")
                embeddings.append([])
        
        logger.info(f"Успешно получено {len(embeddings)} эмбеддингов")
        return embeddings
        
    except Exception as e:
        logger.error(f"Ошибка при векторизации: {e}")
        return []
