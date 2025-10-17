import logging
from typing import List, Optional

import chromadb

from app.config import settings
from app.schemas import RAGContext

from .genai import USER_PROMPT_TEMPLATE, embed_texts

logger = logging.getLogger(__name__)

# Инициализируем ChromaDB клиент
# Предполагается, что индекс уже создан скриптом ingest.py
client = None
collection = None

def get_collection():
    """Получает коллекцию ChromaDB с повторными попытками"""
    global client, collection
    
    if collection is not None:
        return collection
        
    try:
        if client is None:
            client = chromadb.PersistentClient(path=str(settings.INDEX_DIR))
        
        collection = client.get_collection(name="admissions_docs")
        logger.info(f"ChromaDB коллекция получена успешно: {collection.count()} документов")
        return collection
        
    except Exception as e:
        logger.error(f"Ошибка получения ChromaDB коллекции: {e}")
        
        # Пытаемся получить или создать коллекцию
        try:
            if client is None:
                client = chromadb.PersistentClient(path=str(settings.INDEX_DIR))
            
            collection = client.get_or_create_collection(name="admissions_docs")
            logger.info(f"ChromaDB коллекция создана/получена: {collection.count()} документов")
            return collection
            
        except Exception as e2:
            logger.error(f"Критическая ошибка ChromaDB: {e2}")
            return None

def retrieve_context(query: str) -> List[RAGContext]:
    """Получает релевантный контекст из векторного хранилища на основе запроса."""
    collection = get_collection()
    
    if not collection:
        logger.warning("ChromaDB коллекция недоступна")
        return []

    try:
        # 1. Векторизуем запрос пользователя
        query_embedding = embed_texts([query])
        if not query_embedding or len(query_embedding) == 0:
            logger.error("Не удалось векторизовать запрос")
            return []

        # 2. Запрашиваем коллекцию
        try:
            results = collection.query(
                query_embeddings=query_embedding[0],
                n_results=settings.RAG_TOP_K,
                include=["documents", "metadatas", "distances"]
            )
        except Exception as e:
            logger.error(f"Ошибка при запросе к ChromaDB: {e}")
            return []

        # 3. Фильтруем и форматируем результаты
        contexts = []
        if results and results.get("ids") and results["ids"][0]:
            for i in range(len(results["ids"][0])):
                # Безопасное получение distance
                distance = 1.0
                if i < len(results.get("distances", [[]])[0]) if results.get("distances") else False:
                    distance = results["distances"][0][i]
                
                # Chroma использует косинусное расстояние, поэтому 1 - distance = косинусное сходство
                similarity = 1 - distance

                if similarity >= settings.RAG_RELEVANCE_THRESHOLD:
                    # Безопасное получение metadata
                    metadata = {}
                    if i < len(results.get("metadatas", [[]])[0]) if results.get("metadatas") else False:
                        metadata = results["metadatas"][0][i] or {}
                    
                    source = str(metadata.get("source", "unknown"))
                    
                    # Безопасное получение текста документа
                    text = ""
                    if i < len(results.get("documents", [[]])[0]) if results.get("documents") else False:
                        text = results["documents"][0][i] or ""
                
                    contexts.append(RAGContext(
                        source=source,
                        text=text,
                        score=similarity
                    ))
                
        logger.info(f"Найдено {len(contexts)} релевантных контекстов для запроса: '{query[:50]}{'...' if len(query) > 50 else ''}'")
        
        # Логируем статистику релевантности
        if contexts:
            scores = [ctx.score for ctx in contexts]
            max_score = max(scores)
            min_score = min(scores)
            avg_score = sum(scores) / len(scores)
            logger.info(f"Релевантность: мин={min_score:.3f}, макс={max_score:.3f}, сред={avg_score:.3f}")
        
        return contexts
    
    except Exception as e:
        logger.error(f"Ошибка при поиске контекста: {e}")
        return []

def construct_prompt(user_question: str, contexts: List[RAGContext]) -> str:
    """Конструирует финальный промпт для LLM."""
    if not contexts:
        # Если релевантного контекста не найдено, уведомляем об этом LLM
        context_str = "Релевантного контекста в базе знаний не найдено. Сообщите пользователю, что у вас нет информации по этому вопросу, и предложите обратиться в приёмную комиссию напрямую."
    else:
        context_str = "\n---\n".join([f"Источник: {c.source}\nСодержание: {c.text}\nРелевантность: {c.score:.3f}" for c in contexts])

    return USER_PROMPT_TEMPLATE.format(user_question=user_question, context_chunks_with_sources=context_str)
