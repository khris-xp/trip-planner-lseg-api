import google.generativeai as genai
import json
import logging
from typing import Dict, Any, Optional
from config.settings import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiService:
    """Service for interacting with Google Gemini API"""
    
    def __init__(self):
        if not settings.validate_gemini_api_key():
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
        
    async def validate_location(self, destination: str) -> Dict[str, Any]:
        """
        Validate if the given destination exists and is correct
        
        Args:
            destination: Destination string (e.g., "Paris, France" or "Tokyo, Japan")
            
        Returns:
            Dictionary containing validation results
        """
        prompt = f"""
        Validate if the destination "{destination}" exists and is a valid location.
        
        IMPORTANT: Respond with ONLY valid JSON, no markdown formatting, no additional text.
        
        Return this exact JSON structure:
        {{
            "is_valid": true,
            "destination": "corrected_destination_name",
            "message": "explanation of the validation result",
            "suggested_alternatives": null
        }}
        
        Rules:
        1. If the destination exists: is_valid: true with proper capitalized format (City, Country)
        2. If invalid: is_valid: false with suggested_alternatives array of similar valid destinations
        3. Always return proper capitalized names in "City, Country" format
        4. Handle various input formats (with or without commas, different separators)
        5. Return ONLY the JSON object, nothing else
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            logger.info(f"Raw Gemini response: {response_text}")
            
            # Try to extract JSON from the response (in case there's extra text)
            try:
                # First, try to parse as-is
                result = json.loads(response_text)
            except json.JSONDecodeError:
                # If that fails, try to find JSON within the response
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                else:
                    raise ValueError("No valid JSON found in response")
            
            logger.info(f"Location validation result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error validating location: {str(e)}")
            return {
                "is_valid": False,
                "destination": destination,
                "message": f"Error validating location: {str(e)}",
                "suggested_alternatives": []
            }
    
    async def generate_trip_plan(self, destination: str, trip_days: int) -> Dict[str, Any]:
        """
        Generate a detailed trip plan for the validated destination
        
        Args:
            destination: Destination string (e.g., "Paris, France")
            trip_days: Number of days for the trip
            
        Returns:
            Dictionary containing the trip plan
        """
        
        # Generate sequential dates starting from today
        from datetime import datetime, timedelta
        start_date = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
        
        # Create example for the first day
        day1_start = start_date.isoformat()
        day1_end = start_date.replace(hour=20).isoformat()
        
        prompt = f"""
        Create a detailed {trip_days}-day trip plan for {destination}.
        
        Trip Requirements:
        - Duration: {trip_days} days
        
        IMPORTANT: Respond with ONLY valid JSON, no markdown formatting, no additional text.
        
        Return this exact JSON structure:
        {{
            "destination": "{destination}",
            "total_days": {trip_days},
            "daily_plans": [
                {{
                    "day": 1,
                    "time": "08:00:00",
                    "start": "{day1_start}",
                    "end": "{day1_end}",
                    "details": "Day 1: Cultural Exploration & Local Flavors\\n\\n8:00 AM - Start your day with breakfast at a local cafe\\n10:00 AM - Visit major attraction\\n12:00 PM - Lunch at recommended restaurant\\n2:00 PM - Explore cultural site\\n4:00 PM - Shopping or leisure activity\\n6:00 PM - Dinner at local restaurant\\n8:00 PM - Evening entertainment or rest"
                }}
            ],
            "total_estimated_cost": 500.0,
            "best_time_to_visit": "season/months",
            "local_currency": "currency code",
            "important_notes": ["note1", "note2"]
        }}
        
        Guidelines:
        1. Each day must have a "day" field with the day number (1, 2, 3, etc.)
        2. For each day, use "time" field with HH:MM:SS format (e.g., "08:00:00")
        3. Use ISO 8601 datetime format for "start" and "end" fields (increment dates for each day)
        4. Day 1 starts on {start_date.strftime('%Y-%m-%d')}, Day 2 on {(start_date + timedelta(days=1)).strftime('%Y-%m-%d')}, etc.
        5. Each day should start at 8:00 AM and end at 8:00 PM (12-hour day)
        6. In details field, create a comprehensive day plan with timeline
        7. Include specific times for each activity (8:00 AM, 10:00 AM, etc.)
        8. Include popular attractions, local experiences, and cultural activities
        9. Include general tourism activities suitable for most travelers
        10. Use \\n\\n for line breaks in the details field
        11. Return ONLY the JSON object, nothing else
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            logger.info(f"Raw Gemini trip response: {response_text}")
            
            # Try to extract JSON from the response
            try:
                # First, try to parse as-is
                result = json.loads(response_text)
            except json.JSONDecodeError:
                # If that fails, try to find JSON within the response
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                else:
                    raise ValueError("No valid JSON found in response")
            
            logger.info(f"Generated trip plan for {destination}")
            return result
        except Exception as e:
            logger.error(f"Error generating trip plan: {str(e)}")
            raise Exception(f"Failed to generate trip plan: {str(e)}")