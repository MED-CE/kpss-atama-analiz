from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class CityBase(BaseModel):
    name: str
    normalized_name: str

class CityResponse(CityBase):
    id: str
    model_config = ConfigDict(from_attributes=True)

class InstitutionBase(BaseModel):
    name: str
    normalized_name: str

class InstitutionResponse(InstitutionBase):
    id: str
    model_config = ConfigDict(from_attributes=True)

class QualificationBase(BaseModel):
    code: str

class QualificationResponse(QualificationBase):
    id: str
    model_config = ConfigDict(from_attributes=True)

class PlacementPeriodBase(BaseModel):
    year: int
    period: str

class PlacementPeriodResponse(PlacementPeriodBase):
    id: str
    model_config = ConfigDict(from_attributes=True)

class PlacementScoreBase(BaseModel):
    placed_count: int
    empty_quota: int
    min_score: Optional[float]
    max_score: Optional[float]

class PlacementScoreResponse(PlacementScoreBase):
    id: str
    model_config = ConfigDict(from_attributes=True)

class PositionBase(BaseModel):
    title: str
    quota: int
    special_conditions: Optional[str]

class PositionResponse(PositionBase):
    id: str
    period: PlacementPeriodResponse
    institution: InstitutionResponse
    city: CityResponse
    scores: Optional[PlacementScoreResponse]
    qualifications: List[QualificationResponse]
    
    model_config = ConfigDict(from_attributes=True)

class YearlyAnalyticsResponse(BaseModel):
    year: int
    total_quota: int
    total_placed: int
    min_score_overall: Optional[float]
    max_score_overall: Optional[float]
    cities_count: int
    institutions_count: int
    
class QualificationAnalyticsResponse(BaseModel):
    code: str
    yearly_stats: List[YearlyAnalyticsResponse]
