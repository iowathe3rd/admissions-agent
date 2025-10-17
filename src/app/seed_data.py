"""Модуль для загрузки начальных данных в базу данных."""

import json
import logging
import asyncio
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db import AsyncSessionLocal, init_db
from app import models
from app.config import settings


# Настройка логирования
logger = logging.getLogger(__name__)


async def load_seed_data_to_db():
    """Загружает начальные данные из JSON файлов в базу данных."""
    logger.info("Инициализация базы данных...")
    await init_db()
    
    async with AsyncSessionLocal() as session:
        # Проверяем, есть ли уже данные в базе
        result = await session.execute(select(models.Program))
        if result.scalars().first():
            logger.info("База данных уже содержит данные. Пропускаем инициализацию.")
            return
        
        data_path = Path(settings.DATA_DIR)
        
        # Загружаем программы
        programs_file = data_path / "programs.json"
        if programs_file.exists():
            try:
                with open(programs_file, 'r', encoding='utf-8') as f:
                    programs_data = json.load(f)
                    for program_data in programs_data:
                        program = models.Program(
                            name=program_data["name"],
                            description=program_data.get("description"),
                            cost=program_data.get("cost")
                        )
                        session.add(program)
                logger.info(f"Загружено {len(programs_data)} программ.")
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                logger.error(f"Ошибка при загрузке программ из {programs_file}: {e}")
        
        # Загружаем FAQ
        faqs_file = data_path / "faqs.json"
        if faqs_file.exists():
            try:
                with open(faqs_file, 'r', encoding='utf-8') as f:
                    faqs_data = json.load(f)
                    for faq_data in faqs_data:
                        faq = models.FAQ(
                            question=faq_data["question"],
                            answer=faq_data["answer"]
                        )
                        session.add(faq)
                logger.info(f"Загружено {len(faqs_data)} FAQ.")
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                logger.error(f"Ошибка при загрузке FAQ из {faqs_file}: {e}")
        
        # Загружаем документы
        documents_file = data_path / "documents.json"
        if documents_file.exists():
            try:
                with open(documents_file, 'r', encoding='utf-8') as f:
                    documents_data = json.load(f)
                    for doc_data in documents_data:
                        document = models.Document(
                            name=doc_data["name"],
                            required=doc_data.get("required", True)
                        )
                        session.add(document)
                logger.info(f"Загружено {len(documents_data)} документов.")
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                logger.error(f"Ошибка при загрузке документов из {documents_file}: {e}")
        
        # Загружаем шаги
        steps_file = data_path / "steps.json"
        if steps_file.exists():
            try:
                with open(steps_file, 'r', encoding='utf-8') as f:
                    steps_data = json.load(f)
                    for step_data in steps_data:
                        step = models.Step(
                            step_number=step_data["step_number"],
                            description=step_data["description"]
                        )
                        session.add(step)
                logger.info(f"Загружено {len(steps_data)} шагов.")
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                logger.error(f"Ошибка при загрузке шагов из {steps_file}: {e}")
        
        try:
            await session.commit()
            logger.info("Начальные данные успешно загружены в базу данных.")
        except Exception as e:
            await session.rollback()
            logger.error(f"Ошибка при сохранении данных в базу: {e}")
            raise


if __name__ == "__main__":
    # Настройка логирования для прямого запуска
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    asyncio.run(load_seed_data_to_db())