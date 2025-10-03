import asyncio
import logging
from datetime import datetime
from typing import Optional

from models.trip_models import (
    TripRequest, TripResponse, LocationValidation, 
    TripPlan, DayPlan, ErrorResponse
)
from services.gemini_service import GeminiService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TripGeneratorService:
    """Main service for generating trip plans"""
    
    def __init__(self):
        self.gemini_service = GeminiService()
    
    async def generate_trip(self, request: TripRequest) -> TripResponse:
        """
        Generate a complete trip plan including validation and planning
        
        Args:
            request: TripRequest containing all trip details
            
        Returns:
            TripResponse with validation results and trip plan
        """
        try:
            logger.info(f"Starting trip generation for {request.destination}")
            
            # Step 1: Validate location with Gemini
            validation_result = await self.gemini_service.validate_location(
                request.destination
            )
            
            location_validation = LocationValidation(**validation_result)
            
            # Step 2: If location is valid, generate trip plan
            trip_plan = None
            if location_validation.is_valid:
                logger.info("Location validated successfully, generating trip plan")
                
                trip_plan_data = await self.gemini_service.generate_trip_plan(
                    destination=location_validation.destination,
                    trip_days=request.trip_days
                )
                
                # Convert daily plans data to DayPlan objects
                daily_plans = [
                    DayPlan(**day_data) for day_data in trip_plan_data["daily_plans"]
                ]
                
                trip_plan = TripPlan(
                    destination=trip_plan_data["destination"],
                    total_days=trip_plan_data["total_days"],
                    daily_plans=daily_plans,
                    total_estimated_cost=trip_plan_data.get("total_estimated_cost"),
                    best_time_to_visit=trip_plan_data.get("best_time_to_visit"),
                    local_currency=trip_plan_data.get("local_currency"),
                    important_notes=trip_plan_data.get("important_notes", [])
                )
                
                logger.info("Trip plan generated successfully")
                
                return TripResponse(
                    success=True,
                    message=f"Trip plan generated successfully for {location_validation.destination}",
                    location_validation=location_validation,
                    trip_plan=trip_plan
                )
            else:
                logger.warning(f"Location validation failed: {location_validation.message}")
                return TripResponse(
                    success=False,
                    message=f"Location validation failed: {location_validation.message}",
                    location_validation=location_validation,
                    trip_plan=None
                )
                
        except Exception as e:
            logger.error(f"Error generating trip: {str(e)}")
            return TripResponse(
                success=False,
                message=f"Failed to generate trip: {str(e)}",
                location_validation=LocationValidation(
                    is_valid=False,
                    destination=request.destination,
                    message=f"Error occurred during processing: {str(e)}"
                ),
                trip_plan=None
            )
    
    async def validate_location_only(self, destination: str) -> LocationValidation:
        """
        Validate location without generating trip plan
        
        Args:
            destination: Destination string (e.g., "Paris, France")
            
        Returns:
            LocationValidation object
        """
        try:
            validation_result = await self.gemini_service.validate_location(destination)
            return LocationValidation(**validation_result)
        except Exception as e:
            logger.error(f"Error validating location: {str(e)}")
            return LocationValidation(
                is_valid=False,
                destination=destination,
                message=f"Error validating location: {str(e)}"
            )