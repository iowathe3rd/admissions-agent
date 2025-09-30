from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app import models, schemas
from app.db import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Document])
async def read_documents(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """Retrieve all documents."""
    result = await db.execute(select(models.Document).offset(skip).limit(limit))
    documents = result.scalars().all()
    return documents
