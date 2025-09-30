"""Модуль для загрузки начальных данных в базу данных."""

import json
import asyncio
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db import AsyncSessionLocal, init_db
from app import models
from app.config import settings


async def load_seed_data_to_db():
    """Загружает начальные данные из JSON файлов в базу данных."""
    print("Инициализация базы данных...")
    await init_db()
    
    async with AsyncSessionLocal() as session:
        # Проверяем, есть ли уже данные в базе
        result = await session.execute(select(models.Program))
        if result.scalars().first():
            print("База данных уже содержит данные. Пропускаем инициализацию.")
            return
        
        data_path = Path(settings.DATA_DIR)
        
        # Загружаем программы
        programs_file = data_path / "programs.json"
        if programs_file.exists():
            with open(programs_file, 'r', encoding='utf-8') as f:
                programs_data = json.load(f)
                for program_data in programs_data:
                    program = models.Program(
                        name=program_data["name"],
                        description=program_data.get("description"),
                        cost=program_data.get("cost")
                    )
                    session.add(program)
            print(f"Загружено {len(programs_data)} программ.")
        
        # Загружаем FAQ
        faqs_file = data_path / "faqs.json"
        if faqs_file.exists():
            with open(faqs_file, 'r', encoding='utf-8') as f:
                faqs_data = json.load(f)
                for faq_data in faqs_data:
                    faq = models.FAQ(
                        question=faq_data["question"],
                        answer=faq_data["answer"]
                    )
                    session.add(faq)
            print(f"Загружено {len(faqs_data)} FAQ.")
        
        # Загружаем документы
        documents_file = data_path / "documents.json"
        if documents_file.exists():
            with open(documents_file, 'r', encoding='utf-8') as f:
                documents_data = json.load(f)
                for doc_data in documents_data:
                    document = models.Document(
                        name=doc_data["name"],
                        required=doc_data.get("required", True)
                    )
                    session.add(document)
            print(f"Загружено {len(documents_data)} документов.")
        
        # Загружаем шаги
        steps_file = data_path / "steps.json"
        if steps_file.exists():
            with open(steps_file, 'r', encoding='utf-8') as f:
                steps_data = json.load(f)
                for step_data in steps_data:
                    step = models.Step(
                        step_number=step_data["step_number"],
                        description=step_data["description"]
                    )
                    session.add(step)
            print(f"Загружено {len(steps_data)} шагов.")
        
        await session.commit()
        print("Начальные данные успешно загружены в базу данных.")


if __name__ == "__main__":
    asyncio.run(load_seed_data_to_db())