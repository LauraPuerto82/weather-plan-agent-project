from langchain.tools import tool
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE = "https://api.openweathermap.org/data/2.5/weather"
OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")

def _k_to_c(k: float) -> float:
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

    params = {"q": city, "appid": OPENWEATHER_KEY}
    r = requests.get(BASE, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()

    weather = data["weather"][0]["description"]
    main = data["main"]
    wind = data.get("wind", {})
    rain = data.get("rain", {})
    snow = data.get("snow", {})

    return {
        "city": data.get("name", city),
        "condition": weather,
        "temp_c": _k_to_c(main["temp"]),
        "feels_like_c": _k_to_c(main["feels_like"]),
        "wind_ms": wind.get("speed", 0.0),
        "humidity": main.get("humidity", 0),
        "rain_mm": rain.get("1h") or rain.get("3h") or 0.0,
        "snow_mm": snow.get("1h") or snow.get("3h") or 0.0,
    }
