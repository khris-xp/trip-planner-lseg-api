from pydantic import BaseModel
from datetime import time as dt_time
from typing import Optional, List
import json


class TravelPlanRequest(BaseModel):
    day: int
    country: str
    startTime: Optional[dt_time] = None
    endTime: Optional[dt_time] = None


class DayPlan(BaseModel):
    day: int
    time: str
    start: Optional[dt_time] = None
    end: Optional[dt_time] = None
    detials: str


class TravelPlanResponse(BaseModel):
    __root__: List[DayPlan]
