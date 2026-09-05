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

@router.get("/analytics/yearly", response_model=List[schemas.YearlyAnalyticsResponse])
async def get_yearly_analytics(db: AsyncSession = Depends(get_db)):
    # Group by year, sum quota, sum placed, min/max score, count distinct cities/institutions
    query = (
        select(
            models.PlacementPeriod.year,
            func.sum(models.Position.quota).label("total_quota"),
            func.sum(models.PlacementScore.placed_count).label("total_placed"),
            func.min(models.PlacementScore.min_score).label("min_score_overall"),
            func.max(models.PlacementScore.max_score).label("max_score_overall"),
            func.count(func.distinct(models.Position.city_id)).label("cities_count"),
            func.count(func.distinct(models.Position.institution_id)).label("institutions_count"),
        )
        .select_from(models.PlacementPeriod)
        .join(models.Position, models.Position.placement_period_id == models.PlacementPeriod.id)
        .join(models.PlacementScore, models.PlacementScore.position_id == models.Position.id)
        .group_by(models.PlacementPeriod.year)
        .order_by(models.PlacementPeriod.year.desc())
    )
    
    result = await db.execute(query)
    rows = result.all()
    
    return [
        schemas.YearlyAnalyticsResponse(
            year=row.year,
            total_quota=row.total_quota or 0,
            total_placed=row.total_placed or 0,
            min_score_overall=row.min_score_overall,
            max_score_overall=row.max_score_overall,
            cities_count=row.cities_count or 0,
            institutions_count=row.institutions_count or 0
        )
        for row in rows
    ]

@router.get("/qualifications/{code}/analytics", response_model=schemas.QualificationAnalyticsResponse)
async def get_qualification_analytics(code: str, db: AsyncSession = Depends(get_db)):
    # Verify qualification exists
    qual_query = await db.execute(select(models.Qualification).where(models.Qualification.code == code))
    qual = qual_query.scalars().first()
    if not qual:
        raise HTTPException(status_code=404, detail="Qualification not found")
        
    query = (
        select(
            models.PlacementPeriod.year,
            func.sum(models.Position.quota).label("total_quota"),
            func.sum(models.PlacementScore.placed_count).label("total_placed"),
            func.min(models.PlacementScore.min_score).label("min_score_overall"),
            func.max(models.PlacementScore.max_score).label("max_score_overall"),
            func.count(func.distinct(models.Position.city_id)).label("cities_count"),
            func.count(func.distinct(models.Position.institution_id)).label("institutions_count"),
        )
        .select_from(models.PlacementPeriod)
        .join(models.Position, models.Position.placement_period_id == models.PlacementPeriod.id)
        .join(models.position_qualifications, models.position_qualifications.c.position_id == models.Position.id)
        .join(models.PlacementScore, models.PlacementScore.position_id == models.Position.id)
        .where(models.position_qualifications.c.qualification_id == qual.id)
        .group_by(models.PlacementPeriod.year)
        .order_by(models.PlacementPeriod.year.desc())
    )
    
    result = await db.execute(query)
    rows = result.all()
    
    yearly_stats = [
        schemas.YearlyAnalyticsResponse(
            year=row.year,
            total_quota=row.total_quota or 0,
            total_placed=row.total_placed or 0,
            min_score_overall=row.min_score_overall,
            max_score_overall=row.max_score_overall,
            cities_count=row.cities_count or 0,
            institutions_count=row.institutions_count or 0
        )
        for row in rows
    ]
    
    return schemas.QualificationAnalyticsResponse(
        code=code,
        yearly_stats=yearly_stats
    )
