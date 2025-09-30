import pytest
from unittest.mock import patch, MagicMock
from src.rag.retriever import retrieve_context, construct_prompt
from src.rag.genai import llm_answer
from src.app.schemas import RAGContext

def test_construct_prompt_with_context():
    """Тестирует конструирование промпта с контекстом."""
    test_contexts = [
        RAGContext(
            source="programs",
            text="Прикладная информатика стоит 250000 рублей",
            score=0.9
        )
    ]
    
    user_question = "Сколько стоит прикладная информатика?"
    prompt = construct_prompt(user_question, test_contexts)
    
    assert user_question in prompt
    assert "Прикладная информатика стоит 250000 рублей" in prompt
    assert "programs" in prompt

def test_construct_prompt_without_context():
    """Тестирует конструирование промпта без контекста."""
    user_question = "Какая форма у охраны в университете?"
    prompt = construct_prompt(user_question, [])
    
    assert user_question in prompt
    assert "не найдено" in prompt.lower()

@pytest.mark.asyncio
async def test_retrieval_relevance():
    """Тестирует релевантность поиска RAG."""
    # Мокируем ChromaDB для тестирования
    with patch('src.rag.retriever.collection') as mock_collection:
        with patch('src.rag.retriever.embed_texts') as mock_embed:
            
            # Настраиваем моки
            mock_embed.return_value = [[0.1, 0.2, 0.3]]  # Фиктивный эмбеддинг
            
            mock_collection.query.return_value = {
                "ids": [["chunk_1"]],
                "documents": [["Прием документов начинается 20 июня"]],
                "metadatas": [[{"source": "faqs"}]],
                "distances": [[0.1]]  # Высокая схожесть (низкое расстояние)
            }
            
            # Тестируем поиск
            contexts = retrieve_context("сроки подачи документов")
            
            assert len(contexts) > 0
            assert "20 июня" in contexts[0].text
            assert contexts[0].source == "faqs"
            assert contexts[0].score > 0.8  # Высокая релевантность

def test_hallucination_guard():
    """Тестирует защиту от галлюцинаций."""
    # Мокируем LLM для контролируемого ответа
    with patch('src.rag.genai.client') as mock_client:
        mock_response = MagicMock()
        mock_response.text = "Извините, у меня нет информации по этому вопросу. Рекомендую обратиться в приёмную комиссию."
        mock_client.models.generate_content.return_value = mock_response
        
        # Тестируем с пустым контекстом
        user_question = "Какая форма у охраны в университете?"
        prompt = construct_prompt(user_question, [])
        answer = llm_answer(prompt)
        
        # Проверяем, что ответ указывает на отсутствие информации
        assert any(phrase in answer.lower() for phrase in ["нет информации", "обратитесь", "недостаточно"])

def test_retrieval_with_low_relevance():
    """Тестирует фильтрацию нерелевантных результатов."""
    with patch('src.rag.retriever.collection') as mock_collection:
        with patch('src.rag.retriever.embed_texts') as mock_embed:
            
            mock_embed.return_value = [[0.1, 0.2, 0.3]]
            
            mock_collection.query.return_value = {
                "ids": [["chunk_1"]],
                "documents": [["Информация о столовой"]],
                "metadatas": [[{"source": "other"}]],
                "distances": [[0.9]]  # Низкая схожесть (высокое расстояние)
            }
            
            # Поиск с низкой релевантностью должен вернуть пустой список
            contexts = retrieve_context("сроки подачи документов")
            
            assert len(contexts) == 0  # Фильтруется по порогу релевантности

@patch('src.rag.genai.client')
def test_llm_error_handling(mock_client):
    """Тестирует обработку ошибок LLM."""
    # Мокируем ошибку API
    mock_client.models.generate_content.side_effect = Exception("API Error")
    
    answer = llm_answer("Тестовый вопрос")
    
    assert "ошибка" in answer.lower()
    assert "позже" in answer.lower() or "приёмную комиссию" in answer.lower()

def test_embed_texts_error_handling():
    """Тестирует обработку ошибок при векторизации."""
    with patch('src.rag.genai.client') as mock_client:
        mock_client.models.embed_content.side_effect = Exception("Embedding Error")
        
        from src.rag.genai import embed_texts
        result = embed_texts(["test text"])
        
        assert result == []  # Должен вернуть пустой список при ошибке
