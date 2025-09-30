from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app import models, schemas
from app.db import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.FAQ])
async def read_faqs(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """Retrieve all FAQs."""
    result = await db.execute(select(models.FAQ).offset(skip).limit(limit))
    faqs = result.scalars().all()
    return faqs

# The POST /faqs/search is conceptually replaced by the RAG endpoint.
# A simple keyword search could be added here if needed, but the primary
# search mechanism is via the /search/rag endpoint.
