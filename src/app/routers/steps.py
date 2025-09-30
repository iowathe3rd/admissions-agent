from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app import models, schemas
from app.db import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Step])
async def read_steps(
    db: AsyncSession = Depends(get_db)
):
    """Retrieve all application steps, ordered by step number."""
    result = await db.execute(select(models.Step).order_by(models.Step.step_number))
    steps = result.scalars().all()
    return steps
