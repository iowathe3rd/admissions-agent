import chromadb
from typing import List
import logging

from app.config import settings
from app.schemas import RAGContext
from .genai import embed_texts, USER_PROMPT_TEMPLATE

logger = logging.getLogger(__name__)

# Инициализируем ChromaDB клиент
# Предполагается, что индекс уже создан скриптом ingest.py
try:
    client = chromadb.PersistentClient(path=str(settings.INDEX_DIR))
    collection = client.get_collection(name="admissions_docs")
    logger.info("ChromaDB клиент инициализирован успешно")
except Exception as e:
    logger.error(f"Ошибка инициализации ChromaDB клиента или получения коллекции: {e}")
    logger.error("Убедитесь, что запустили скрипт индексации первым.")
    collection = None

def retrieve_context(query: str) -> List[RAGContext]:
    """Получает релевантный контекст из векторного хранилища на основе запроса."""
    if not collection:
        logger.warning("ChromaDB коллекция недоступна")
        return []

    try:
        # 1. Векторизуем запрос пользователя
        query_embedding = embed_texts([query])
        if not query_embedding:
            logger.error("Не удалось векторизовать запрос")
            return []

        # 2. Запрашиваем коллекцию
        try:
            # ChromaDB принимает первый элемент списка эмбеддингов
            results = collection.query(
                query_embeddings=query_embedding[0] if query_embedding else [],
                n_results=settings.RAG_TOP_K,
                include=["documents", "metadatas", "distances"]  # type: ignore
            )
        except Exception as e:
            logger.error(f"Ошибка при запросе к ChromaDB: {e}")
            return []

        # 3. Фильтруем и форматируем результаты
        contexts = []
        if results and results.get("ids") and results.get("ids") and len(results["ids"]) > 0 and results["ids"][0]:
            for i in range(len(results["ids"][0])):
                # Безопасное получение distance
                distance = 1.0
                distances = results.get("distances")
                if distances and len(distances) > 0 and distances[0] and len(distances[0]) > i:
                    distance = distances[0][i]
                
                # Chroma использует косинусное расстояние, поэтому 1 - distance = косинусное сходство
                similarity = 1 - distance

                if similarity >= settings.RAG_RELEVANCE_THRESHOLD:
                    # Безопасное получение metadata
                    metadata = {}
                    metadatas = results.get("metadatas")
                    if metadatas and len(metadatas) > 0 and metadatas[0] and len(metadatas[0]) > i:
                        metadata = metadatas[0][i] or {}
                    
                    source = str(metadata.get("source", "unknown"))
                    
                    # Безопасное получение текста документа
                    text = ""
                    documents = results.get("documents")
                    if documents and len(documents) > 0 and documents[0] and len(documents[0]) > i:
                        text = documents[0][i] or ""
                    
                    contexts.append(RAGContext(
                        source=source,
                        text=text,
                        score=similarity
                    ))
                    
        logger.info(f"Найдено {len(contexts)} релевантных контекстов для запроса: {query[:50]}...")
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

    prompt = USER_PROMPT_TEMPLATE.replace("{{user_question}}", user_question)
    prompt = prompt.replace("{{context_chunks_with_sources}}", context_str)
    
    return prompt
