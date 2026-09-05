import asyncio
import logging
import os
import sys

# Add parent directory and backend directory to python path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
sys.path.append(os.path.join(root_dir, "backend"))

from discovery import discover_placement_periods
from downloader import fetch_document_links, download_file
from parser import parse_excel_placements, parse_pdf_qualifications
from validator import validate_placement_data

from backend.database.database import AsyncSessionLocal
from backend.database.models import PlacementPeriod, SourceDocument, RawExtraction
from sqlalchemy import select

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def process_period(session, year: int, period_data: dict, db_period: PlacementPeriod):
    """Downloads documents, parses them, and saves raw extraction data."""
    logger.info(f"Processing Period: {db_period.period}...")
    
    docs = await fetch_document_links(period_data['url'])
    logger.info(f"Found {len(docs)} documents for {db_period.period}")
    
    for doc in docs:
        logger.info(f"Downloading: {doc['title']}")
        file_bytes = await download_file(doc['url'])
        if not file_bytes:
            continue
            
        # Create SourceDocument record
        source_doc = SourceDocument(
            placement_period_id=db_period.id,
            url=doc['url'],
            source_type=doc['type']
        )
        session.add(source_doc)
        await session.flush() # get ID
        
        # Parse depending on type
        raw_data = None
        if doc['url'].lower().endswith('.pdf') and doc['type'] == 'QUALIFICATIONS':
            # This is slow, so we would normally offload to a celery worker
            # raw_data = parse_pdf_qualifications(file_bytes)
            # For now, we mock to keep the pipeline fast in the loop
            raw_data = {"status": "PARSED_QUALIFICATIONS_MOCK"}
            
        elif (doc['url'].lower().endswith('.xls') or doc['url'].lower().endswith('.xlsx')) and doc['type'] == 'PLACEMENTS':
            # raw_data = parse_excel_placements(file_bytes)
            raw_data = {"status": "PARSED_PLACEMENTS_MOCK"}
            
        if raw_data:
            extraction = RawExtraction(
                source_document_id=source_doc.id,
                raw_data=raw_data
            )
            session.add(extraction)
            
    await session.commit()

async def run_ingestion_pipeline():
    logger.info("Starting OSYM Ingestion Pipeline...")
    
    # 1. Discovery
    periods = await discover_placement_periods()
    logger.info(f"Discovered {len(periods)} potential placement periods.")
    
    # 2. Database Insert & Process
    async with AsyncSessionLocal() as session:
        for period in periods:
            year = period.get('year')
            existing = await session.execute(
                select(PlacementPeriod).where(
                    PlacementPeriod.year == year,
                    PlacementPeriod.period == period['title']
                )
            )
            db_period = existing.scalars().first()
            
            if not db_period:
                logger.info(f"Adding new period to DB: {year} - {period['title']}")
                db_period = PlacementPeriod(
                    year=year,
                    period=period['title'],
                    is_active=True
                )
                session.add(db_period)
                await session.flush()
                
                # Full process for new periods
                await process_period(session, year, period, db_period)
                
        await session.commit()
        logger.info("Ingestion Pipeline Completed Successfully!")

if __name__ == "__main__":
    asyncio.run(run_ingestion_pipeline())
