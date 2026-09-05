from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from typing import List, Optional

from database.database import get_db
from database import models
from schemas import schemas

router = APIRouter()

@router.get("/qualifications", response_model=List[schemas.QualificationResponse])
async def get_qualifications(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Qualification).order_by(models.Qualification.code))
    return result.scalars().all()

@router.get("/qualifications/{code}", response_model=schemas.QualificationResponse)
async def get_qualification(code: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Qualification).where(models.Qualification.code == code))
    qual = result.scalars().first()
    if not qual:
        raise HTTPException(status_code=404, detail="Qualification not found")
    return qual

@router.get("/placements", response_model=List[schemas.PositionResponse])
async def get_placements(
    qualification_code: Optional[str] = None,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    city: Optional[str] = None,
    institution: Optional[str] = None,
    min_score: Optional[float] = None,
    max_score: Optional[float] = None,
    limit: int = Query(50, le=100),
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    query = select(models.Position).options(
        selectinload(models.Position.period),
        selectinload(models.Position.institution),
        selectinload(models.Position.city),
        selectinload(models.Position.scores),
        selectinload(models.Position.qualifications)
    )
    
    # Joins for filtering
    if qualification_code:
        query = query.join(models.Position.qualifications).filter(models.Qualification.code == qualification_code)
    if year_from or year_to:
        query = query.join(models.Position.period)
        if year_from:
            query = query.filter(models.PlacementPeriod.year >= year_from)
        if year_to:
            query = query.filter(models.PlacementPeriod.year <= year_to)
    if city:
        query = query.join(models.Position.city).filter(models.City.normalized_name.ilike(f"%{city}%"))
    if institution:
        query = query.join(models.Position.institution).filter(models.Institution.normalized_name.ilike(f"%{institution}%"))
    if min_score or max_score:
        query = query.join(models.Position.scores)
        if min_score:
            query = query.filter(models.PlacementScore.min_score >= min_score)
        if max_score:
            query = query.filter(models.PlacementScore.max_score <= max_score)
            
    query = query.limit(limit).offset(offset)
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/placements/{id}", response_model=schemas.PositionResponse)
async def get_placement(id: str, db: AsyncSession = Depends(get_db)):
    query = select(models.Position).options(
        selectinload(models.Position.period),
        selectinload(models.Position.institution),
        selectinload(models.Position.city),
        selectinload(models.Position.scores),
        selectinload(models.Position.qualifications)
    ).where(models.Position.id == id)
    
    result = await db.execute(query)
    pos = result.scalars().first()
    if not pos:
        raise HTTPException(status_code=404, detail="Placement not found")
    return pos

@router.get("/years", response_model=List[int])
async def get_years(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.PlacementPeriod.year).distinct().order_by(models.PlacementPeriod.year.desc()))
    return result.scalars().all()

@router.get("/cities", response_model=List[schemas.CityResponse])
async def get_cities(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.City).order_by(models.City.normalized_name))
    return result.scalars().all()

@router.get("/institutions", response_model=List[schemas.InstitutionResponse])
async def get_institutions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Institution).order_by(models.Institution.normalized_name))
    return result.scalars().all()
