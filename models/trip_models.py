from pydantic import BaseModel, Field, model_validator
from typing import List, Optional, Dict, Any
from datetime import date, datetime, time as dt_time

class TravelPlanRequest(BaseModel):
    day: int
    country: str
    start_time: Optional[dt_time] = None
    end_time: Optional[dt_time] = None

    @model_validator(mode="after")
    def check_times(self):
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValueError("start_time must be before end_time")
        if self.day < 1 or self.day > 31:
            raise ValueError("day must be between 1 and 31")
        return self

class TripRequest(BaseModel):
    """Model for trip generation request"""
    destination: str = Field(..., description="Destination (e.g., 'Paris, France' or 'Tokyo, Japan')")
    trip_days: int = Field(..., ge=1, le=30, description="Number of days for the trip (1-30)")
    
class LocationValidation(BaseModel):
    """Model for location validation result"""
    is_valid: bool
    destination: str
    message: str
    suggested_alternatives: Optional[List[str]] = None
    
class DayPlan(BaseModel):
    day: int
    time: dt_time
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    details: str

    @model_validator(mode="after")
    def check_range(self):
        if (self.start and not self.end) or (self.end and not self.start):
            raise ValueError("Both start and end must be provided together")
        if self.start and self.end and self.start >= self.end:
            raise ValueError("start must be before end")
        return self
    
class TravelPlanResponse(BaseModel):
    plan: List[DayPlan]

class TripPlan(BaseModel):
    """Model for complete trip plan"""
    destination: str
    total_days: int
    daily_plans: List[DayPlan]
    total_estimated_cost: Optional[float] = None
    best_time_to_visit: Optional[str] = None
    local_currency: Optional[str] = None
    important_notes: Optional[List[str]] = None
    
class TripResponse(BaseModel):
    """Model for trip generation response"""
    success: bool
    message: str
    location_validation: LocationValidation
    trip_plan: Optional[TripPlan] = None
    generated_at: datetime = Field(default_factory=datetime.utcnow)

class ErrorResponse(BaseModel):
    """Model for error responses"""
    success: bool = False
    error: str
    details: Optional[Dict[str, Any]] = None