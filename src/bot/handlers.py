import json
import logging
from typing import Optional

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app import models
from app.db import AsyncSessionLocal
from src.rag.genai import llm_answer
from src.rag.retriever import construct_prompt, retrieve_context

from .keyboards import back_to_menu_keyboard, main_menu_keyboard

router = Router()
logger = logging.getLogger(__name__)

async def safe_answer(callback: CallbackQuery, text: str, **kwargs):
    """Безопасная отправка ответа через callback."""
    if callback.message:
        await safe_answer(callback, text, **kwargs)


@router.message(Command("start"))
async def start_handler(message: Message):
    """Обработчик команды /start."""
    user_name = message.from_user.first_name if message.from_user and message.from_user.first_name else "Абитуриент"
    welcome_text = f"""
👋 Здравствуйте, {user_name}!

Я — бот-ассистент приёмной комиссии ALT University. 

🎯 **Что я умею:**
• Отвечаю на вопросы о поступлении
• Показываю информацию о программах обучения
• Помогаю с подачей документов
• Отвечаю на часто задаваемые вопросы

Выберите интересующий раздел или просто задайте вопрос!
"""
    await message.answer(
        welcome_text,
        reply_markup=main_menu_keyboard()
    )


@router.message(Command("help"))
async def help_handler(message: Message):
    """Обработчик команды /help."""
    help_text = """
🆘 **Справка по боту**

**Доступные команды:**
/start - Начать работу с ботом
/help - Показать эту справку
/menu - Показать главное меню

**Возможности:**
• Задавайте любые вопросы о поступлении
• Используйте кнопки для быстрого доступа к информации
• Получайте актуальную информацию о программах и документах

**Примеры вопросов:**
- "Какие сроки подачи документов?"
- "Сколько стоит обучение на информатике?"
- "Какие документы нужны для поступления?"
"""
    await message.answer(help_text, reply_markup=main_menu_keyboard())


@router.message(Command("menu"))
async def menu_handler(message: Message):
    """Обработчик команды /menu."""
    await message.answer(
        "Выберите интересующий раздел:",
        reply_markup=main_menu_keyboard()
    )


@router.callback_query(F.data == "show_programs")
async def show_programs_handler(callback: CallbackQuery):
    """Обрабатывает нажатие кнопки 'Программы'."""
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(models.Program).order_by(models.Program.name))
            programs = result.scalars().all()
            if not programs:
                await safe_answer(callback, "Информация о программах пока не добавлена.")
            else:
                response_text = "🎓 **Наши программы:**\n\n"
                for p in programs:
                    # Правильная проверка для SQLAlchemy объектов
                    cost_value = getattr(p, 'cost', None)
                    cost = f"{cost_value:,} руб.".replace(",", " ") if cost_value else "бесплатно"
                    response_text += f"• **{p.name}** - {cost}\n"
                    
                    # Правильная проверка для description
                    desc_value = getattr(p, 'description', None)
                    if desc_value:
                        response_text += f"  _{desc_value}_\n\n"
                    else:
                        response_text += "\n"
                await safe_answer(callback, response_text, parse_mode="Markdown", reply_markup=back_to_menu_keyboard())
    except Exception as e:
        logger.error(f"Ошибка при получении программ: {e}")
        await safe_answer(callback, 
            "Произошла ошибка при получении информации о программах. Попробуйте позже.",
            reply_markup=back_to_menu_keyboard()
        )
    await callback.answer()


@router.callback_query(F.data == "show_guide")
async def show_guide_handler(callback: CallbackQuery):
    """Обрабатывает нажатие кнопки 'Шаги подачи документов'."""
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(models.Step).order_by(models.Step.step_number))
            steps = result.scalars().all()
            if not steps:
                await safe_answer(callback, 
                    "Пошаговое руководство пока не добавлено.",
                    reply_markup=back_to_menu_keyboard()
                )
            else:
                response_text = "📝 **Пошаговое руководство по подаче документов:**\n\n"
                for s in steps:
                    response_text += f"**{s.step_number}.** {s.description}\n\n"
                
                response_text += "💡 *Рекомендуем следовать шагам последовательно для успешного поступления.*"
                
                await safe_answer(callback, response_text, reply_markup=back_to_menu_keyboard())
    except Exception as e:
        logger.error(f"Ошибка при получении шагов: {e}")
        await safe_answer(callback, 
            "Произошла ошибка при получении пошагового руководства. Попробуйте позже.",
            reply_markup=back_to_menu_keyboard()
        )
    await callback.answer()


@router.callback_query(F.data == "show_faq")
async def show_faq_handler(callback: CallbackQuery):
    """Обрабатывает нажатие кнопки 'FAQ'."""
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(models.FAQ).order_by(models.FAQ.id))
            faqs = result.scalars().all()
            if not faqs:
                await safe_answer(callback, 
                    "Раздел FAQ пока пуст.",
                    reply_markup=back_to_menu_keyboard()
                )
            else:
                response_text = "❓ **Часто задаваемые вопросы:**\n\n"
                for i, f in enumerate(faqs, 1):
                    response_text += f"**{i}. {f.question}**\n{f.answer}\n\n"
                
                response_text += "💬 *Если не нашли ответ на свой вопрос, задайте его мне напрямую!*"
                
                await safe_answer(callback, response_text, reply_markup=back_to_menu_keyboard())
    except Exception as e:
        logger.error(f"Ошибка при получении FAQ: {e}")
        await safe_answer(callback, 
            "Произошла ошибка при получении FAQ. Попробуйте позже.",
            reply_markup=back_to_menu_keyboard()
        )
    await callback.answer()


@router.callback_query(F.data == "check_docs")
async def check_docs_handler(callback: CallbackQuery):
    """Обрабатывает нажатие кнопки 'Список документов'."""
    try:
        async with AsyncSessionLocal() as session:
            # Получаем обязательные документы
            result = await session.execute(select(models.Document).filter(models.Document.required == True))
            required_docs = result.scalars().all()
            
            # Получаем дополнительные документы
            result = await session.execute(select(models.Document).filter(models.Document.required == False))
            optional_docs = result.scalars().all()
            
            if not required_docs:
                await safe_answer(callback, 
                    "Список обязательных документов пока не определен.",
                    reply_markup=back_to_menu_keyboard()
                )
            else:
                response_text = "📋 **Необходимые документы для поступления:**\n\n"
                
                response_text += "✅ **Обязательные документы:**\n"
                for i, d in enumerate(required_docs, 1):
                    response_text += f"{i}. {d.name}\n"
                
                if optional_docs:
                    response_text += "\n📎 **Дополнительные документы:**\n"
                    for i, d in enumerate(optional_docs, 1):
                        response_text += f"{i}. {d.name}\n"
                
                response_text += "\n💡 *Убедитесь, что у вас готовы сканы всех документов в хорошем качестве.*"
                response_text += "\n\n📧 *Документы можно подать через личный кабинет или принести лично в приёмную комиссию.*"
                
                await safe_answer(callback, response_text, reply_markup=back_to_menu_keyboard())
    except Exception as e:
        logger.error(f"Ошибка при получении документов: {e}")
        await safe_answer(callback, 
            "Произошла ошибка при получении списка документов. Попробуйте позже.",
            reply_markup=back_to_menu_keyboard()
        )
    await callback.answer()


@router.message(F.text)
async def rag_answer_handler(message: Message):
    """Обрабатывает любое текстовое сообщение через RAG-пайплайн и логирует взаимодействие."""
    if not message.text or not message.from_user:
        return

    # Отправляем сообщение о поиске
    search_message = await message.answer("Ищу информацию... 🧠")

    try:
        # 1. Получаем контекст
        contexts = retrieve_context(message.text)

        # 2. Конструируем промпт
        prompt = construct_prompt(message.text, contexts)

        # 3. Получаем ответ от LLM
        answer = llm_answer(prompt)
        
        # 4. Логируем взаимодействие в базе данных
        try:
            async with AsyncSessionLocal() as session:
                # Находим или создаем кандидата
                result = await session.execute(
                    select(models.Candidate).filter(models.Candidate.telegram_id == message.from_user.id)
                )
                candidate = result.scalars().first()
                if not candidate:
                    candidate = models.Candidate(
                        telegram_id=message.from_user.id,
                        full_name=message.from_user.full_name
                    )
                    session.add(candidate)
                    await session.flush()  # Флашируем для получения ID кандидата

                # Создаем запись взаимодействия
                interaction = models.Interaction(
                    candidate_id=candidate.id,
                    user_message=message.text,
                    bot_response=answer,
                    contexts_json=json.dumps([{"source": c.source, "text": c.text, "score": c.score} for c in contexts], ensure_ascii=False)
                )
                session.add(interaction)
                await session.commit()
        except Exception as e:
            logger.error(f"Ошибка при сохранении взаимодействия в БД: {e}")
            # Продолжаем работу, даже если не удалось сохранить в БД

        # 5. Удаляем сообщение о поиске и отправляем ответ
        await search_message.delete()
        
        # Ограничиваем длину ответа для Telegram
        if len(answer) > 4096:
            answer = answer[:4093] + "..."
            
        await message.answer(answer, disable_web_page_preview=True)
        
    except Exception as e:
        logger.error(f"Ошибка при обработке RAG-запроса: {e}")
        await search_message.delete()
        await message.answer("Извините, произошла ошибка при обработке вашего запроса. Попробуйте переформулировать вопрос или воспользуйтесь кнопками меню.")
        
        # Показываем главное меню при ошибке
        await message.answer("Выберите один из вариантов:", reply_markup=main_menu_keyboard())


@router.callback_query(F.data == "show_contacts")
async def show_contacts_handler(callback: CallbackQuery):
    """Обрабатывает нажатие кнопки 'Контакты'."""
    contact_text = """
📞 **Контактная информация**

🏢 **Приёмная комиссия ALT University**

📧 **Email:** admissions@alt.university
📱 **Телефон:** +7 (495) 123-45-67
🌐 **Сайт:** https://alt.university

📍 **Адрес:** 
г. Москва, ул. Университетская, д. 1

🕐 **Часы работы приёмной комиссии:**
Пн-Пт: 09:00 - 18:00
Сб: 10:00 - 15:00
Вс: выходной

📋 **Личный кабинет абитуриента:**
https://cabinet.alt.university
"""
    await safe_answer(callback, contact_text, reply_markup=back_to_menu_keyboard())
    await callback.answer()


@router.callback_query(F.data == "ask_question")
async def ask_question_handler(callback: CallbackQuery):
    """Обрабатывает нажатие кнопки 'Задать вопрос'."""
    question_text = """
🔍 **Задайте свой вопрос**

Просто напишите ваш вопрос, и я постараюсь найти ответ в нашей базе знаний!

**Примеры вопросов:**
• Какие сроки подачи документов?
• Сколько стоит обучение?
• Какие экзамены нужно сдавать?
• Есть ли общежитие?
• Можно ли получить стипендию?

💡 Постарайтесь формулировать вопросы конкретно - это поможет мне дать более точный ответ!
"""
    await safe_answer(callback, question_text, reply_markup=back_to_menu_keyboard())
    await callback.answer()


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu_handler(callback: CallbackQuery):
    """Обрабатывает возврат в главное меню."""
    await safe_answer(callback, 
        "Выберите интересующий раздел:",
        reply_markup=main_menu_keyboard()
    )
    await callback.answer()
