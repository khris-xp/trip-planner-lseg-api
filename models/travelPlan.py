from datetime import time as dt_time
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, model_validator


class TravelPlanRequest(BaseModel):
    day: int
    country: str
    start_time: Optional[dt_time] = None
    end_time: Optional[dt_time] = None

    @model_validator()
    def check_times(self):
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValueError("start_time must be before end_time")
        if self.day < 1 and self.day > 31:
            raise ValueError("day must be between 1 and 31")
        return self


class DayPlan(BaseModel):
    time: dt_time
    start: datetime = None
    end: datetime = None
    details: str

    @model_validator()
    def check_range(self):
        if (self.start and not self.end) or (self.end and not self.start):
            raise ValueError("Both start and end must be provided together")
        if self.start and self.end and self.start >= self.end:
            raise ValueError("start must be before end")
        return self


class TravelPlanResponse(BaseModel):
    plan: List[DayPlan]
