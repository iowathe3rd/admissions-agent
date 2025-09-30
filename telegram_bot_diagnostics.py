"""
Диагностическая утилита для проверки интеграции Telegram бота с RAG
"""
import asyncio
import sys
import logging
from pathlib import Path

# Добавляем src в путь
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.app.config import settings
from src.rag.retriever import retrieve_context, construct_prompt
from src.rag.genai import llm_answer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_bot_integration():
    """Тестирует интеграцию бота с RAG"""
    print("🤖 ДИАГНОСТИКА ИНТЕГРАЦИИ TELEGRAM БОТА С RAG")
    print("=" * 60)
    
    # 1. Проверяем настройки
    print("📋 ПРОВЕРКА НАСТРОЕК:")
    print(f"   BOT_TOKEN: {'✅ Установлен' if settings.BOT_TOKEN else '❌ Не установлен'}")
    print(f"   GEMINI_API_KEY: {'✅ Установлен' if settings.GEMINI_API_KEY else '❌ Не установлен'}")
    print(f"   RAG_RELEVANCE_THRESHOLD: {settings.RAG_RELEVANCE_THRESHOLD}")
    
    if not settings.BOT_TOKEN or not settings.GEMINI_API_KEY:
        print("❌ Критические настройки отсутствуют!")
        return False
    
    # 2. Тестируем импорты
    print("\n📦 ПРОВЕРКА ИМПОРТОВ:")
    try:
        from src.bot.handlers import router, rag_answer_handler
        print("   ✅ Bot handlers импортированы")
        
        from src.bot.runner import main as bot_main
        print("   ✅ Bot runner импортирован")
        
        # Проверяем количество обработчиков
        message_handlers = len(router.message.handlers)
        print(f"   📊 Message handlers: {message_handlers}")
        
        if message_handlers < 4:
            print("   ⚠️ Недостаточно обработчиков сообщений")
        
    except Exception as e:
        print(f"   ❌ Ошибка импорта: {e}")
        return False
    
    # 3. Тестируем RAG цепочку
    print("\n🧠 ТЕСТ RAG ЦЕПОЧКИ:")
    test_queries = [
        "стоимость обучения",
        "направления подготовки", 
        "контакты университета"
    ]
    
    rag_working = True
    for query in test_queries:
        try:
            contexts = retrieve_context(query)
            if contexts:
                prompt = construct_prompt(query, contexts)
                answer = llm_answer(prompt)
                print(f"   ✅ '{query}': {len(contexts)} контекстов, ответ {len(answer)} символов")
            else:
                print(f"   ⚠️ '{query}': контекст не найден")
                
        except Exception as e:
            print(f"   ❌ '{query}': ошибка - {e}")
            rag_working = False
    
    # 4. Тестируем обработчик бота
    print("\n🎯 ТЕСТ ОБРАБОТЧИКА БОТА:")
    
    class MockUser:
        id = 999999
        first_name = 'TestUser'
        full_name = 'Test User'
    
    class MockMessage:
        def __init__(self, text):
            self.text = text
            self.from_user = MockUser()
            self._responses = []
        
        async def answer(self, text, **kwargs):
            self._responses.append(text)
            print(f"      📤 BOT: {text[:100]}{'...' if len(text) > 100 else ''}")
            return self  # Возвращаем себя как mock для delete()
        
        async def delete(self):
            print(f"      🗑️ Сообщение удалено")
    
    try:
        test_message = MockMessage("сколько стоит обучение")
        print(f"   📝 Тестируем сообщение: '{test_message.text}'")
        
        await rag_answer_handler(test_message)
        
        if len(test_message._responses) >= 2:  # "Ищу информацию..." + реальный ответ
            print("   ✅ Обработчик работает корректно")
            bot_handler_working = True
        else:
            print("   ❌ Обработчик не сгенерировал ответы")
            bot_handler_working = False
            
    except Exception as e:
        print(f"   ❌ Ошибка обработчика: {e}")
        bot_handler_working = False
    
    # 5. Проверяем Telegram API
    print("\n📡 ПРОВЕРКА TELEGRAM API:")
    try:
        from aiogram import Bot
        bot = Bot(token=settings.BOT_TOKEN)
        
        # Тестируем базовый вызов API
        bot_info = await bot.get_me()
        print(f"   ✅ Подключение к Telegram API успешно")
        print(f"   🤖 Имя бота: {bot_info.first_name}")
        print(f"   🆔 Username: @{bot_info.username}")
        
        await bot.session.close()
        telegram_working = True
        
    except Exception as e:
        print(f"   ❌ Ошибка Telegram API: {e}")
        telegram_working = False
    
    # 6. Итоговая диагностика
    print("\n" + "=" * 60)
    print("🎯 ИТОГИ ДИАГНОСТИКИ:")
    
    components = [
        ("Настройки", settings.BOT_TOKEN and settings.GEMINI_API_KEY),
        ("RAG система", rag_working),
        ("Bot обработчик", bot_handler_working),
        ("Telegram API", telegram_working)
    ]
    
    all_working = True
    for name, status in components:
        status_icon = "✅" if status else "❌"
        print(f"   {status_icon} {name}")
        if not status:
            all_working = False
    
    if all_working:
        print("\n🎉 ВСЕ КОМПОНЕНТЫ РАБОТАЮТ! Бот должен отвечать на вопросы.")
        print("\n💡 ВОЗМОЖНЫЕ ПРИЧИНЫ ПРОБЛЕМ В TELEGRAM:")
        print("   1. Убедитесь что бот запущен командой: python main.py")
        print("   2. Проверьте что бот не заблокирован в Telegram")
        print("   3. Попробуйте команду /start в боте")
        print("   4. Убедитесь что отправляете текстовые сообщения (не медиа)")
        print("   5. Проверьте что нет конфликтующих webhook'ов")
    else:
        print("\n❌ НАЙДЕНЫ ПРОБЛЕМЫ! Требуется исправление компонентов выше.")
    
    return all_working

async def test_webhook_conflict():
    """Проверяет конфликты webhook'ов"""
    print("\n🔍 ПРОВЕРКА WEBHOOK КОНФЛИКТОВ:")
    
    try:
        from aiogram import Bot
        bot = Bot(token=settings.BOT_TOKEN)
        
        webhook_info = await bot.get_webhook_info()
        
        if webhook_info.url:
            print(f"   ⚠️ Установлен webhook: {webhook_info.url}")
            print("   💡 Для работы через polling нужно удалить webhook:")
            print("      await bot.delete_webhook()")
        else:
            print("   ✅ Webhook не установлен - polling должен работать")
            
        await bot.session.close()
        
    except Exception as e:
        print(f"   ❌ Ошибка проверки webhook: {e}")

async def main():
    """Главная функция"""
    success = await test_bot_integration()
    await test_webhook_conflict()
    
    if success:
        print("\n🚀 Попробуйте запустить бота: python main.py")
        print("   И отправьте ему сообщение в Telegram")
    else:
        print("\n🔧 Исправьте проблемы выше перед запуском бота")

if __name__ == "__main__":
    asyncio.run(main())