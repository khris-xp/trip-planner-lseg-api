# Trip Planner API with Google Gemini

An AI-powered trip planning service that uses Google Gemini to validate destinations and generate detailed travel itineraries.

## Features

- **Location Validation**: Uses Gemini AI to validate if cities and countries exist
- **Smart Trip Planning**: Generates detailed day-by-day itineraries based on:
  - Trip duration (1-30 days)
  - Budget preferences
  - User interests
  - Travel style (budget, balanced, luxury)
- **RESTful API**: Built with FastAPI for high performance
- **Error Handling**: Comprehensive error handling and validation

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd trip-planner-lseg-api
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Google Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

4. **Get Google Gemini API Key**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy it to your `.env` file

## Running the Application

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:
- **Interactive API docs**: `http://localhost:8000/docs`
- **ReDoc documentation**: `http://localhost:8000/redoc`

## API Endpoints

### Health Check
```http
GET /health
```

### Validate Location
```http
POST /validate-location?city=Paris&country=France
```

### Generate Trip Plan
```http
POST /generate-trip
Content-Type: application/json

{
  "city": "Paris",
  "country": "France",
  "trip_days": 5,
  "budget": 1500,
  "interests": ["culture", "food", "museums"],
  "travel_style": "balanced"
}
```

## Request/Response Examples

### Trip Generation Request
```json
{
  "city": "Tokyo",
  "country": "Japan",
  "trip_days": 7,
  "budget": 2000,
  "interests": ["culture", "food", "technology"],
  "travel_style": "balanced"
}
```

### Trip Generation Response
```json
{
  "success": true,
  "message": "Trip plan generated successfully",
  "location_validation": {
    "is_valid": true,
    "city": "Tokyo",
    "country": "Japan",
    "message": "Location validated successfully"
  },
  "trip_plan": {
    "destination": "Tokyo, Japan",
    "total_days": 7,
    "daily_plans": [
      {
        "day": 1,
        "title": "Arrival and Shibuya Exploration",
        "activities": [
          "Arrive at Narita/Haneda Airport",
          "Check into hotel in Shibuya",
          "Explore Shibuya Crossing",
          "Visit Hachiko Statue",
          "Dinner at local izakaya"
        ],
        "estimated_cost": 150.0,
        "transportation": "Airport express + JR Yamanote Line",
        "accommodation_suggestion": "Shibuya area hotels"
      }
    ],
    "total_estimated_cost": 1800.0,
    "best_time_to_visit": "Spring (March-May) or Fall (September-November)",
    "local_currency": "JPY",
    "important_notes": [
      "Get JR Pass for unlimited train travel",
      "Download Google Translate app",
      "Carry cash as many places don't accept cards"
    ]
  },
  "generated_at": "2025-10-03T10:30:00Z"
}
```

## Project Structure

```
trip-planner-lseg-api/
├── main.py                          # FastAPI application entry point
├── requirements.txt                 # Python dependencies
├── .env.example                    # Environment variables template
├── models/
│   ├── __init__.py
│   └── trip_models.py              # Pydantic models for requests/responses
├── services/
│   ├── __init__.py
│   ├── gemini_service.py           # Google Gemini API integration
│   └── trip_generator_service.py   # Main trip generation logic
└── config/
    ├── __init__.py
    └── settings.py                 # Application configuration
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key (required) | None |
| `DEBUG` | Enable debug mode | false |
| `REQUESTS_PER_MINUTE` | Rate limiting | 60 |

## Error Handling

The API provides comprehensive error handling:

- **400 Bad Request**: Invalid input parameters
- **500 Internal Server Error**: API configuration issues or processing errors
- **Validation Errors**: Detailed field-level validation messages

## Development

### Running Tests
```bash
pytest
```

### Code Structure
- **Models**: Define request/response schemas using Pydantic
- **Services**: Business logic separated into focused service classes
- **Config**: Centralized configuration management
- **Main**: FastAPI application setup and routing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.