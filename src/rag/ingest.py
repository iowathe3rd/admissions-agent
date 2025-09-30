import chromadb
import json
from pathlib import Path
from typing import List, Dict, Any
import asyncio
import logging

from app.config import settings
from .genai import embed_texts
from app.db import init_db

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Инициализируем ChromaDB клиент
# Это создаст директорию, если её не существует, и сохранит данные.
try:
    client = chromadb.PersistentClient(path=str(settings.INDEX_DIR))
    logger.info(f"ChromaDB клиент инициализирован с путем: {settings.INDEX_DIR}")
except Exception as e:
    logger.error(f"Ошибка инициализации ChromaDB: {e}")
    raise

# Создаем или получаем коллекцию
collection = client.get_or_create_collection(name="admissions_docs")

def load_seed_data() -> List[Dict[str, Any]]:
    """Загружает все .json файлы из директории seed данных."""
    all_docs = []
    data_path = Path(settings.DATA_DIR)
    
    if not data_path.exists():
        logger.error(f"Директория с данными не найдена: {data_path}")
        return []
    
    logger.info(f"Загружаем данные из директории: {data_path}")
    
    for json_file in data_path.glob("*.json"):
        try:
            logger.info(f"Обрабатываем файл: {json_file.name}")
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                source_name = json_file.stem
                for item in data:
                    # Простое текстовое представление
                    text = " ".join(f"{k}: {v}" for k, v in item.items())
                    all_docs.append({"source": source_name, "text": text})
        except Exception as e:
            logger.error(f"Ошибка при загрузке файла {json_file}: {e}")
            continue
    
    logger.info(f"Загружено {len(all_docs)} документов из {len(list(data_path.glob('*.json')))} файлов")
    return all_docs

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> List[str]:
    """Basic text chunking based on character count."""
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

async def ingest_data():
    """Управляет процессом индексации данных."""
    logger.info("Инициализация базы данных...")
    try:
        await init_db()
        logger.info("База данных инициализирована.")
    except Exception as e:
        logger.error(f"Ошибка инициализации БД: {e}")
        return

    logger.info("Начинаем индексацию данных...")
    
    # Проверяем, не проиндексированы ли уже данные
    collection = None
    try:
        collection = client.get_or_create_collection(name="admissions_docs")
        current_count = collection.count()
        if current_count > 0:
            logger.info(f"Коллекция уже содержит {current_count} документов. Очищаем...")
            # Удаляем существующую коллекцию и создаем новую
            client.delete_collection(name="admissions_docs")
            collection = client.create_collection(name="admissions_docs")
    except Exception as e:
        logger.error(f"Ошибка работы с коллекцией: {e}")
        collection = client.create_collection(name="admissions_docs")
    
    if not collection:
        logger.error("Не удалось создать коллекцию")
        return
    
    # 1. Загружаем данные
    docs = load_seed_data()
    if not docs:
        logger.error("Данные для индексации не найдены. Прерываем процесс.")
        return

    # 2. Разбиваем документы на чанки
    all_chunks = []
    metadatas = []
    ids = []
    chunk_id = 1

    for doc in docs:
        chunks = chunk_text(doc["text"])
        for chunk in chunks:
            all_chunks.append(chunk)
            metadatas.append({"source": doc["source"]})
            ids.append(f"chunk_{chunk_id}")
            chunk_id += 1

    logger.info(f"Создано {len(all_chunks)} чанков из {len(docs)} документов.")

    # 3. Генерируем эмбеддинги (порциями для безопасности)
    batch_size = 32  # API Gemini имеет лимиты, батчинг - хорошая практика
    all_embeddings = []
    
    for i in range(0, len(all_chunks), batch_size):
        batch_texts = all_chunks[i:i+batch_size]
        logger.info(f"Векторизация батча {i//batch_size + 1}/{(len(all_chunks) + batch_size - 1)//batch_size}...")
        
        batch_embeddings = embed_texts(batch_texts)
        if batch_embeddings:
            all_embeddings.extend(batch_embeddings)
            logger.info(f"Батч {i//batch_size + 1} обработан успешно")
        else:
            logger.error(f"Не удалось векторизовать батч {i//batch_size + 1}. Прерываем процесс.")
            return

    if not all_embeddings or len(all_embeddings) != len(all_chunks):
        logger.error("Векторизация провалилась или вернула неправильное количество эмбеддингов. Прерываем процесс.")
        return

    # 4. Добавляем в ChromaDB
    logger.info("Добавление эмбеддингов в ChromaDB...")
    try:
        collection.add(
            embeddings=all_embeddings,
            documents=all_chunks,
            metadatas=metadatas,
            ids=ids
        )
        logger.info("Индексация данных завершена.")
        logger.info(f"Общее количество элементов в коллекции: {collection.count()}")
    except Exception as e:
        logger.error(f"Ошибка при добавлении в ChromaDB: {e}")
        return

if __name__ == "__main__":
    # Это позволяет запускать скрипт напрямую для заполнения БД
    # Пример: python -m src.rag.ingest
    try:
        asyncio.run(ingest_data())
    except KeyboardInterrupt:
        logger.info("Индексация прервана пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка при индексации: {e}")
        raise
