from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app import models, schemas
from app.db import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Program])
async def read_programs(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """Retrieve all programs."""
    result = await db.execute(select(models.Program).offset(skip).limit(limit))
    programs = result.scalars().all()
    return programs

@router.get("/{program_id}", response_model=schemas.Program)
async def read_program(program_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve a single program by its ID."""
    result = await db.execute(select(models.Program).filter(models.Program.id == program_id))
    program = result.scalars().first()
    if program is None:
        raise HTTPException(status_code=404, detail="Program not found")
    return program
