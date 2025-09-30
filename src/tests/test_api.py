import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
import asyncio

# Для работы тестов необходимо настроить python path
# Можно запускать с помощью `python -m pytest` из корневой директории
from src.app.main import app

client = TestClient(app)

def test_healthz():
    """Тестирует эндпоинт /healthz."""
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Admissions Agent API is running"}

def test_cors_headers():
    """Тестирует наличие CORS заголовков."""
    response = client.get("/healthz")
    assert "access-control-allow-origin" in response.headers

@pytest.mark.asyncio
async def test_programs_endpoint():
    """Тестирует эндпоинт /programs с мокированной БД."""
    with patch('src.app.routers.programs.get_db') as mock_get_db:
        # Мокируем сессию БД
        mock_session = AsyncMock()
        mock_get_db.return_value.__aenter__.return_value = mock_session
        
        # Мокируем результат запроса
        mock_result = AsyncMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result
        
        response = client.get("/programs/")
        assert response.status_code == 200
        assert response.json() == []

@pytest.mark.asyncio 
async def test_search_rag_endpoint():
    """Тестирует RAG поиск эндпоинт."""
    with patch('src.rag.retriever.retrieve_context') as mock_retrieve:
        mock_retrieve.return_value = []
        
        response = client.post("/search/rag", json={"query": "тестовый запрос"})
        assert response.status_code == 200
        assert "contexts" in response.json()
        assert response.json()["contexts"] == []
