import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from aiogram.types import Message, User, Chat, CallbackQuery
from aiogram.enums import ChatType

from src.bot.handlers import start_handler, rag_answer_handler, show_programs_handler


@pytest.fixture
def mock_user():
    """Фикстура для мокирования пользователя Telegram."""
    return User(
        id=12345,
        is_bot=False,
        first_name="Тест",
        last_name="Пользователь",
        username="testuser"
    )

@pytest.fixture 
def mock_chat():
    """Фикстура для мокирования чата."""
    return Chat(id=12345, type=ChatType.PRIVATE)

@pytest.fixture
def mock_message(mock_user, mock_chat):
    """Фикстура для мокирования сообщения."""
    message = MagicMock(spec=Message)
    message.from_user = mock_user
    message.chat = mock_chat
    message.text = "Тестовое сообщение"
    message.answer = AsyncMock()
    return message

@pytest.fixture
def mock_callback_query(mock_user, mock_message):
    """Фикстура для мокирования callback query."""
    callback = MagicMock(spec=CallbackQuery)
    callback.from_user = mock_user
    callback.message = mock_message
    callback.answer = AsyncMock()
    return callback

@pytest.mark.asyncio
async def test_start_handler(mock_message):
    """Тестирует обработчик команды /start."""
    await start_handler(mock_message)
    
    # Проверяем, что был вызван метод answer
    mock_message.answer.assert_called_once()
    
    # Проверяем содержимое ответа
    call_args = mock_message.answer.call_args
    assert "Здравствуйте" in call_args[0][0]
    assert "ALT University" in call_args[0][0]
    assert "reply_markup" in call_args[1]

@pytest.mark.asyncio
async def test_show_programs_handler_success(mock_callback_query):
    """Тестирует успешное получение программ."""
    with patch('src.bot.handlers.AsyncSessionLocal') as mock_session_local:
        # Настраиваем мок сессии
        mock_session = AsyncMock()
        mock_session_local.return_value.__aenter__.return_value = mock_session
        
        # Мокируем результат запроса программ
        mock_program = MagicMock()
        mock_program.name = "Прикладная информатика"
        mock_program.cost = 250000
        mock_program.description = "Описание программы"
        
        mock_result = AsyncMock()
        mock_result.scalars.return_value.all.return_value = [mock_program]
        mock_session.execute.return_value = mock_result
        
        await show_programs_handler(mock_callback_query)
        
        # Проверяем вызовы
        mock_callback_query.message.answer.assert_called_once()
        mock_callback_query.answer.assert_called_once()
        
        # Проверяем содержимое ответа
        call_args = mock_callback_query.message.answer.call_args
        assert "Прикладная информатика" in call_args[0][0]
        assert "250 000 руб" in call_args[0][0]

@pytest.mark.asyncio
async def test_show_programs_handler_empty(mock_callback_query):
    """Тестирует случай отсутствия программ."""
    with patch('src.bot.handlers.AsyncSessionLocal') as mock_session_local:
        mock_session = AsyncMock()
        mock_session_local.return_value.__aenter__.return_value = mock_session
        
        # Возвращаем пустой список
        mock_result = AsyncMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result
        
        await show_programs_handler(mock_callback_query)
        
        call_args = mock_callback_query.message.answer.call_args
        assert "не добавлена" in call_args[0][0]

@pytest.mark.asyncio
async def test_rag_answer_handler_success(mock_message):
    """Тестирует успешную обработку RAG запроса."""
    mock_message.text = "Сколько стоит обучение?"
    
    with patch('src.bot.handlers.retrieve_context') as mock_retrieve, \
         patch('src.bot.handlers.construct_prompt') as mock_construct, \
         patch('src.bot.handlers.llm_answer') as mock_llm, \
         patch('src.bot.handlers.AsyncSessionLocal') as mock_session_local:
        
        # Настраиваем моки
        mock_retrieve.return_value = []
        mock_construct.return_value = "Тестовый промпт"
        mock_llm.return_value = "Стоимость обучения составляет 250 000 рублей."
        
        mock_session = AsyncMock()
        mock_session_local.return_value.__aenter__.return_value = mock_session
        
        # Мокируем поиск кандидата (не найден)
        mock_result = AsyncMock()
        mock_result.scalars.return_value.first.return_value = None
        mock_session.execute.return_value = mock_result
        
        # Мокируем временное сообщение о поиске
        search_message = AsyncMock()
        search_message.delete = AsyncMock()
        mock_message.answer.return_value = search_message
        
        await rag_answer_handler(mock_message)
        
        # Проверяем, что функции были вызваны
        mock_retrieve.assert_called_once_with("Сколько стоит обучение?")
        mock_construct.assert_called_once()
        mock_llm.assert_called_once()
        
        # Проверяем, что сообщение о поиске было удалено
        search_message.delete.assert_called_once()

@pytest.mark.asyncio
async def test_rag_answer_handler_error(mock_message):
    """Тестирует обработку ошибки в RAG handler."""
    mock_message.text = "Тестовый вопрос"
    
    with patch('src.bot.handlers.retrieve_context') as mock_retrieve, \
         patch('src.bot.handlers.main_menu_keyboard') as mock_keyboard:
        
        # Симулируем ошибку
        mock_retrieve.side_effect = Exception("Тестовая ошибка")
        mock_keyboard.return_value = MagicMock()
        
        # Мокируем временное сообщение
        search_message = AsyncMock()
        search_message.delete = AsyncMock()
        mock_message.answer.return_value = search_message
        
        await rag_answer_handler(mock_message)
        
        # Проверяем, что была обработка ошибки
        search_message.delete.assert_called_once()
        assert mock_message.answer.call_count >= 2  # Сообщение о поиске + ошибка + меню

@pytest.mark.asyncio
async def test_message_without_text(mock_message):
    """Тестирует обработку сообщения без текста."""
    mock_message.text = None
    
    await rag_answer_handler(mock_message)
    
    # Не должно быть вызовов answer для пустого сообщения
    mock_message.answer.assert_not_called()

@pytest.mark.asyncio 
async def test_message_without_user(mock_message):
    """Тестирует обработку сообщения без пользователя."""
    mock_message.from_user = None
    
    await rag_answer_handler(mock_message)
    
    # Не должно быть вызовов answer для сообщения без пользователя
    mock_message.answer.assert_not_called()
