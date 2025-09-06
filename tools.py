from langchain.tools import tool
from weather_service import get_current, OpenWeatherError

@tool
def get_weather(city: str) -> dict:
    """
    Retrieve the **current weather conditions** for a given city.

    Args:
        city (str): City name, e.g. "Madrid", "New York".

    Returns (dict):
        {
            "city": str,           # City name resolved by API
            "condition": str,      # Main category (Clear, Rain, Snow, Clouds...)
            "description": str,    # Human-friendly detail ("light rain", "overcast clouds")
            "temp_c": float,       # Temperature in Celsius
            "feels_like_c": float, # Perceived temperature in Celsius
            "wind_kmh": float,     # Wind speed in km/h
            "humidity": int,       # Humidity percentage (0-100)
            "rain_mm": float,      # Rain volume (mm, last 1-3h)
            "snow_mm": float       # Snow volume (mm, last 1-3h)
        }

    Notes:
        - All values are in metric units.
        - Always call this tool before making plans that depend on weather conditions
          (e.g. outdoor activities, safety checks, or day planning).
    """
    try:
        return get_current(city)
    except OpenWeatherError as e:
        return {"error": str(e)}
