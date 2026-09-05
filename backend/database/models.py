import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text, JSON, Table
from sqlalchemy.orm import relationship
from database.database import Base

def generate_uuid():
    return str(uuid.uuid4())

position_qualifications = Table(
    "position_qualifications",
    Base.metadata,
    Column("position_id", String, ForeignKey("positions.id"), primary_key=True),
    Column("qualification_id", String, ForeignKey("qualifications.id"), primary_key=True)
)

class PlacementPeriod(Base):
    __tablename__ = "placement_periods"
    id = Column(String, primary_key=True, default=generate_uuid)
    year = Column(Integer, nullable=False)
    period = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    
    positions = relationship("Position", back_populates="period")
    source_documents = relationship("SourceDocument", back_populates="period")

class City(Base):
    __tablename__ = "cities"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    normalized_name = Column(String, nullable=False, unique=True)
    
    positions = relationship("Position", back_populates="city")

class Institution(Base):
    __tablename__ = "institutions"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    normalized_name = Column(String, nullable=False, unique=True)
    
    positions = relationship("Position", back_populates="institution")

class Qualification(Base):
    __tablename__ = "qualifications"
    id = Column(String, primary_key=True, default=generate_uuid)
    code = Column(String, nullable=False, unique=True)
    
    versions = relationship("QualificationVersion", back_populates="qualification")
    positions = relationship("Position", secondary=position_qualifications, back_populates="qualifications")

class QualificationVersion(Base):
    __tablename__ = "qualification_versions"
    id = Column(String, primary_key=True, default=generate_uuid)
    qualification_id = Column(String, ForeignKey("qualifications.id"))
    placement_period_id = Column(String, ForeignKey("placement_periods.id"))
    description = Column(Text, nullable=False)
    
    qualification = relationship("Qualification", back_populates="versions")

class Position(Base):
    __tablename__ = "positions"
    id = Column(String, primary_key=True, default=generate_uuid)
    placement_period_id = Column(String, ForeignKey("placement_periods.id"))
    institution_id = Column(String, ForeignKey("institutions.id"))
    city_id = Column(String, ForeignKey("cities.id"))
    title = Column(String, nullable=False)
    quota = Column(Integer, nullable=False)
    special_conditions = Column(Text)
    
    period = relationship("PlacementPeriod", back_populates="positions")
    institution = relationship("Institution", back_populates="positions")
    city = relationship("City", back_populates="positions")
    qualifications = relationship("Qualification", secondary=position_qualifications, back_populates="positions")
    scores = relationship("PlacementScore", back_populates="position", uselist=False)

class PlacementScore(Base):
    __tablename__ = "placement_scores"
    id = Column(String, primary_key=True, default=generate_uuid)
    position_id = Column(String, ForeignKey("positions.id"), unique=True)
    placed_count = Column(Integer, nullable=False)
    empty_quota = Column(Integer, default=0)
    min_score = Column(Float)
    max_score = Column(Float)
    
    position = relationship("Position", back_populates="scores")

class SourceDocument(Base):
    __tablename__ = "source_documents"
    id = Column(String, primary_key=True, default=generate_uuid)
    placement_period_id = Column(String, ForeignKey("placement_periods.id"))
    url = Column(String, nullable=False)
    file_hash = Column(String)
    storage_path = Column(String)
    source_type = Column(String, default="OFFICIAL")
    
    period = relationship("PlacementPeriod", back_populates="source_documents")
    extractions = relationship("RawExtraction", back_populates="document")

class RawExtraction(Base):
    __tablename__ = "raw_extractions"
    id = Column(String, primary_key=True, default=generate_uuid)
    source_document_id = Column(String, ForeignKey("source_documents.id"))
    raw_data = Column(JSON, nullable=False)
    
    document = relationship("SourceDocument", back_populates="extractions")

class IngestionJob(Base):
    __tablename__ = "ingestion_jobs"
    id = Column(String, primary_key=True, default=generate_uuid)
    status = Column(String, default="PENDING")
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

class DataValidationLog(Base):
    __tablename__ = "data_validation_logs"
    id = Column(String, primary_key=True, default=generate_uuid)
    ingestion_job_id = Column(String, ForeignKey("ingestion_jobs.id"))
    table_name = Column(String)
    error_description = Column(Text)
