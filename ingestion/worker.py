import asyncio
import logging
import os
import sys

# Add parent directory and backend directory to python path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
sys.path.append(os.path.join(root_dir, "backend"))

from discovery import discover_placement_periods
from backend.database.database import AsyncSessionLocal
from backend.database.models import PlacementPeriod
from sqlalchemy import select

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_ingestion_pipeline():
    logger.info("Starting OSYM Ingestion Pipeline...")
    
    # 1. Discovery
    periods = await discover_placement_periods()
    logger.info(f"Discovered {len(periods)} potential placement periods.")
    
    # 2. Database Insert for Periods
    async with AsyncSessionLocal() as session:
        for period in periods:
            # Extract year and period number (e.g. 2024/1 -> year: 2024, is_first: True)
            year = period.get('year')
            # Check if it already exists
            existing = await session.execute(
                select(PlacementPeriod).where(
                    PlacementPeriod.year == year,
                    PlacementPeriod.name == period['title']
                )
            )
            
            if not existing.scalars().first():
                logger.info(f"Adding new period to DB: {year} - {period['title']}")
                new_period = PlacementPeriod(
                    year=year,
                    name=period['title'],
                    is_active=True
                )
                session.add(new_period)
                
        await session.commit()
        logger.info("Saved all new placement periods to Neon Database!")
        
    logger.info("Ingestion Pipeline Completed.")

if __name__ == "__main__":
    asyncio.run(run_ingestion_pipeline())
