"""
Утилита для диагностики и тестирования RAG системы
"""
import asyncio
import sys
import logging
from typing import List
from pathlib import Path

# Добавляем src в путь
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Теперь импортируем
from src.rag.retriever import retrieve_context
from src.rag.genai import embed_texts, llm_answer
from src.app.config import settings

# Импортируем collection отдельно
import chromadb
try:
    client = chromadb.PersistentClient(path=str(settings.INDEX_DIR))
    collection = client.get_collection(name="admissions_docs")
except:
    collection = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_collection_status():
    """Проверяет состояние коллекции ChromaDB"""
    print("=== ДИАГНОСТИКА КОЛЛЕКЦИИ ===")
    
    if not collection:
        print("❌ Коллекция не инициализирована")
        return False
    
    try:
        count = collection.count()
        print(f"✅ Документов в коллекции: {count}")
        
        if count == 0:
            print("⚠️ Коллекция пустая - запустите индексацию")
            return False
            
        # Получаем примеры документов
        sample = collection.get(limit=3, include=['documents', 'metadatas'])
        print("\n📄 Примеры документов:")
        for i, (doc, meta) in enumerate(zip(sample['documents'], sample['metadatas'])):
            source = meta.get('source', 'unknown')
            print(f"{i+1}. Источник: {source}")
            print(f"   Длина: {len(doc)} символов")
            print(f"   Превью: {doc[:100]}...")
            
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при обращении к коллекции: {e}")
        return False

def test_embedding_quality():
    """Тестирует качество векторизации"""
    print("\n=== ТЕСТ ВЕКТОРИЗАЦИИ ===")
    
    test_texts = [
        "стоимость обучения",
        "направления подготовки", 
        "контакты университета"
    ]
    
    try:
        embeddings = embed_texts(test_texts)
        
        if not embeddings:
            print("❌ Векторизация не работает")
            return False
            
        print(f"✅ Векторизация работает")
        print(f"   Количество векторов: {len(embeddings)}")
        
        for i, emb in enumerate(embeddings):
            if emb:
                print(f"   Вектор {i+1}: размерность {len(emb)}")
            else:
                print(f"   Вектор {i+1}: ❌ пустой")
                
        return True
        
    except Exception as e:
        print(f"❌ Ошибка векторизации: {e}")
        return False

def test_search_quality():
    """Тестирует качество поиска"""
    print("\n=== ТЕСТ КАЧЕСТВА ПОИСКА ===")
    
    test_queries = [
        ("стоимость обучения", "стоимость"),
        ("направления подготовки", "программы"),
        ("контакты", "телефон"),
        ("проходные баллы", "балл"),
        ("общежитие", "проживание")
    ]
    
    results = []
    
    for query, expected_keyword in test_queries:
        try:
            contexts = retrieve_context(query)
            
            if not contexts:
                print(f"❌ '{query}': контекст не найден")
                results.append(False)
                continue
                
            # Проверяем релевантность
            max_score = max(ctx.score for ctx in contexts)
            
            # Проверяем наличие ожидаемого ключевого слова
            has_keyword = any(expected_keyword.lower() in ctx.text.lower() for ctx in contexts)
            
            if max_score >= settings.RAG_RELEVANCE_THRESHOLD and has_keyword:
                print(f"✅ '{query}': найдено {len(contexts)} контекстов, релевантность {max_score:.3f}")
                results.append(True)
            else:
                print(f"⚠️ '{query}': найдено {len(contexts)}, но качество низкое (релевантность {max_score:.3f}, ключевое слово: {has_keyword})")
                results.append(False)
                
        except Exception as e:
            print(f"❌ '{query}': ошибка поиска - {e}")
            results.append(False)
    
    success_rate = sum(results) / len(results) * 100
    print(f"\n📊 Качество поиска: {success_rate:.1f}% ({sum(results)}/{len(results)})")
    
    return success_rate >= 80

def test_end_to_end():
    """Тестирует полную цепочку RAG"""
    print("\n=== КОМПЛЕКСНЫЙ ТЕСТ ===")
    
    query = "Сколько стоит обучение на экономическом факультете?"
    
    try:
        # 1. Поиск контекста
        contexts = retrieve_context(query)
        
        if not contexts:
            print("❌ Контекст не найден")
            return False
            
        print(f"✅ Найдено контекстов: {len(contexts)}")
        
        # 2. Генерация ответа
        from src.rag.retriever import construct_prompt
        prompt = construct_prompt(query, contexts)
        answer = llm_answer(prompt)
        
        if not answer or len(answer) < 50:
            print("❌ Ответ слишком короткий или пустой")
            return False
            
        print(f"✅ Ответ сгенерирован ({len(answer)} символов)")
        print(f"   Превью: {answer[:200]}...")
        
        # 3. Проверяем содержит ли ответ релевантную информацию
        relevant_keywords = ["160,000", "руб", "экономика", "стоимость"]
        has_relevant_info = any(keyword.lower() in answer.lower() for keyword in relevant_keywords)
        
        if has_relevant_info:
            print("✅ Ответ содержит релевантную информацию")
            return True
        else:
            print("⚠️ Ответ может не содержать релевантной информации")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка в комплексном тесте: {e}")
        return False

async def main():
    """Главная функция диагностики"""
    print("🔍 ДИАГНОСТИКА RAG СИСТЕМЫ")
    print("=" * 50)
    
    # Проверяем настройки
    print(f"📋 Настройки:")
    print(f"   RAG_RELEVANCE_THRESHOLD: {settings.RAG_RELEVANCE_THRESHOLD}")
    print(f"   RAG_TOP_K: {settings.RAG_TOP_K}")
    print(f"   INDEX_DIR: {settings.INDEX_DIR}")
    print(f"   DATA_DIR: {settings.DATA_DIR}")
    
    # Запускаем тесты
    tests = [
        ("Коллекция", test_collection_status),
        ("Векторизация", test_embedding_quality),
        ("Поиск", test_search_quality),
        ("Комплексный тест", test_end_to_end)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Ошибка в тесте '{test_name}': {e}")
            results.append((test_name, False))
    
    # Итоги
    print("\n" + "=" * 50)
    print("🎯 ИТОГИ ДИАГНОСТИКИ:")
    
    for test_name, result in results:
        status = "✅ ПРОЙДЕН" if result else "❌ ПРОВАЛЕН"
        print(f"   {test_name}: {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    if passed == total:
        print(f"\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! RAG система работает отлично.")
    elif passed >= total * 0.75:
        print(f"\n⚠️ СИСТЕМА РАБОТАЕТ С ОГРАНИЧЕНИЯМИ ({passed}/{total} тестов пройдено)")
    else:
        print(f"\n❌ СИСТЕМА НЕИСПРАВНА ({passed}/{total} тестов пройдено)")

if __name__ == "__main__":
    asyncio.run(main())