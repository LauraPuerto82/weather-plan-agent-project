from weather_service import get_current, OpenWeatherError
import requests

# Note: No @tool decorator needed - create_agent() automatically
# wraps functions as tools based on type hints and docstrings

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
    
def get_location():
    """
    Detects the user's approximate geographic location based on their public IP address.

    This tool should only be used when the user does not specify any city or location.
    If the user explicitly mentions a city (e.g., "weather in Madrid"), this function
    should not be called.

    The function queries the public `ip-api.com` geolocation service and returns:
    - city
    - region
    - country

    Returns
    -------
    dict
        A dictionary containing the detected city, region, and country. Missing fields
        will be returned as None.
    """                   

    try:
        response = requests.get("http://ip-api.com/json/", timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") == "fail":
            return {"error": "Unable to detect location"}
            
        return {
            "city": data.get("city"),
            "region": data.get("regionName"),
            "country": data.get("country")
        }
    except requests.RequestException as e:
        return {"error": "Location detection failed. Please specify your city."}


