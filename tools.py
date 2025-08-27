from langchain.tools import tool
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE = "https://api.openweathermap.org/data/2.5/weather"
OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")

def _k_to_c(k: float) -> float:
    """
    Convert a temperature from Kelvin to Celsius, rounded to one decimal place.

    Args:
        k: Temperature in Kelvin.

    Returns:
        Temperature in Celsius, rounded to one decimal.
    """
    return round(k - 273.15, 1)

@tool
def get_weather(city: str) -> dict:    
    """
    Use this tool to retrieve the current weather for any specified city. 
    Always call this tool before making plans that depend on weather conditions.

    Args:
        city: The name of the city to get weather information for.

    Returns:
        A dictionary with the following keys:
        - city: The official city name as returned by the weather service.
        - condition: A brief text description of the current weather (e.g., "clear sky", "rain", "snow").
        - temp_c: Current temperature in Celsius.
        - feels_like_c: "Feels like" temperature in Celsius, accounting for wind and humidity.
        - wind_ms: Wind speed in meters per second.
        - humidity: Humidity percentage (0-100).
        - rain_mm: Rainfall in millimeters over the last hour or three hours (0.0 if none).
        - snow_mm: Snowfall in millimeters over the last hour or three hours (0.0 if none).

    All temperature values are in Celsius, wind speed in m/s, and precipitation in mm.
    Use the returned data to inform and personalize your day plan, checklist, and recommendations.
    """
    if not OPENWEATHER_KEY:
        raise RuntimeError("OPENWEATHER_API_KEY is not set")

    try:
        resp = requests.get(
            BASE,
            params={"q": city, "appid": OPENWEATHER_KEY, "units": "metric", "lang": "en"},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        return {"error": f"Weather API error: {e}", "city": city}

    main = data.get("main") or {}
    wind = data.get("wind") or {}
    weather = (data.get("weather") or [{}])[0].get("description", "unknown")
    rain = (data.get("rain") or {})
    snow = (data.get("snow") or {})

    return {
        "city": data.get("name", city),
        "condition": weather,
        "temp_c": round(main.get("temp", 0.0), 1),
        "feels_like_c": round(main.get("feels_like", 0.0), 1),
        "wind_ms": wind.get("speed", 0.0),              # m/s
        "humidity": main.get("humidity", 0),
        "rain_mm": rain.get("1h") or rain.get("3h") or 0.0,
        "snow_mm": snow.get("1h") or snow.get("3h") or 0.0,
    }
