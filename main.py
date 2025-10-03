from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from models.trip_models import TripRequest, TripResponse, LocationValidation, ErrorResponse, TravelPlanRequest, TravelPlanResponse
from services.trip_generator_service import TripGeneratorService
from config.settings import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered trip planner using Google Gemini"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
trip_generator_service = TripGeneratorService()

@app.get("/")
async def read_root():
    """Root endpoint with API information"""
    return {
        "message": "Trip Planner API",
        "version": settings.APP_VERSION,
        "status": "active",
        "gemini_configured": settings.validate_gemini_api_key()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "gemini_api_configured": settings.validate_gemini_api_key()
    }

@app.post("/validate-location", response_model=LocationValidation)
async def validate_location(destination: str):
    """
    Validate if a destination exists
    
    Args:
        destination: Destination string (e.g., "Paris, France" or "Tokyo, Japan")
        
    Returns:
        LocationValidation object with validation results
    """
    try:
        if not settings.validate_gemini_api_key():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Gemini API key not configured"
            )
        
        result = await trip_generator_service.validate_location_only(destination)
        return result
        
    except Exception as e:
        logger.error(f"Error in validate_location endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to validate location: {str(e)}"
        )

@app.post("/generate-trip", response_model=TripResponse)
async def generate_trip(request: TripRequest):
    """
    Generate a complete trip plan including location validation
    
    Args:
        request: TripRequest containing all trip details
        
    Returns:
        TripResponse with validation results and trip plan
    """
    try:
        if not settings.validate_gemini_api_key():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Gemini API key not configured"
            )
        
        logger.info(f"Received trip request: {request.destination} for {request.trip_days} days")
        
        result = await trip_generator_service.generate_trip(request)
        return result
        
    except Exception as e:
        logger.error(f"Error in generate_trip endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate trip: {str(e)}"
        )

@app.post("/travel-plan", response_model=TravelPlanResponse)
async def create_travel_plan(request: TravelPlanRequest):
    """
    Create a travel plan for a specific day and country
    
    Args:
        request: TravelPlanRequest containing day, country, and optional time constraints
        
    Returns:
        TravelPlanResponse with plan details
    """
    try:
        if not settings.validate_gemini_api_key():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Gemini API key not configured"
            )
        
        logger.info(f"Creating travel plan for day {request.day} in {request.country}")
        
        # Create a simplified trip request for single day
        trip_request = TripRequest(
            destination=request.country,
            trip_days=1
        )
        
        # Generate the trip plan
        result = await trip_generator_service.generate_trip(trip_request)
        
        if result.success and result.trip_plan:
            # Extract the daily plans and return as TravelPlanResponse
            travel_plan_response = TravelPlanResponse(
                plan=result.trip_plan.daily_plans
            )
            return travel_plan_response
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.message
            )
        
    except Exception as e:
        logger.error(f"Error in travel-plan endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create travel plan: {str(e)}"
        )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Global exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "Internal server error",
            "details": str(exc) if settings.DEBUG else None
        }
    )
