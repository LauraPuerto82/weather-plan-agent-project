from weather_service import get_current, OpenWeatherError
import requests
import streamlit as st
from config import get_openweather_api_key

# Note: No @tool decorator needed - create_agent() automatically
# wraps functions as tools based on type hints and docstrings.


def get_weather(city: str) -> dict:
    """
    Retrieve the **current weather conditions** for a given city.

    Args
    ----
    city : str
        City name, e.g. "Madrid", "New York".

    Returns
    -------
    dict
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

    Notes
    -----
    - All values are in metric units.
    - Always call this tool before making plans that depend on weather conditions
      (e.g. outdoor activities, safety checks, or day planning).
    """
    try:
        return get_current(city)
    except OpenWeatherError as e:
        return {"error": str(e)}


OPENWEATHER_API_KEY = get_openweather_api_key()

# Global variable to store coordinates for tool access
# This is set by the UI before invoking the agent
_current_coords = None

def set_user_coordinates(coords: dict):
    """Set the current user coordinates for get_location() to use."""
    global _current_coords
    _current_coords = coords


def get_location() -> dict:
    """
    Tool: get_location
    -------------------
    Returns the user's current city using browser-based geolocation.

    How it works
    ------------
    - The frontend (Streamlit) captures the user's real latitude and longitude
      through the browser using `streamlit_geolocation()`.
    - Those coordinates are stored in `st.session_state['coords']`.
    - This tool reads those coordinates and performs a reverse geocoding lookup
      using the OpenWeather Geocoding API to determine the actual city name.

    Returns
    -------
    dict
        A structured response with:
        - "city": str | None
              The inferred city name (e.g. "Teruel").
        - "lat": float | None
              Latitude obtained from the browser.
        - "lon": float | None
              Longitude obtained from the browser.
        - "error": str | None
              Error message if the city cannot be determined.
              If an error exists, the agent should ask the user for their city.
    """

    # 0) Ensure we have an API key configured
    if not OPENWEATHER_API_KEY:
        return {
            "city": None,
            "lat": None,
            "lon": None,
            "error": "OPENWEATHER_API_KEY is missing. Ask the user for their city."
        }

    # 1) Extract browser coordinates from global variable (set by UI)
    # This works even when called from agent threads where session_state isn't available
    global _current_coords
    coords = _current_coords

    # Fallback to session_state if called directly (e.g., from debug panel)
    if not coords:
        try:
            coords = st.session_state.get("coords")
        except Exception:
            pass
    if not coords:
        return {
            "city": None,
            "lat": None,
            "lon": None,
            "error": "No browser coordinates available. Ask the user for their city."
        }

    lat = coords.get("latitude")
    lon = coords.get("longitude")

    if lat is None or lon is None:
        return {
            "city": None,
            "lat": lat,
            "lon": lon,
            "error": "Incomplete coordinates. Ask the user for their city."
        }

    # 2) Reverse geocoding request to OpenWeather
    url = "https://api.openweathermap.org/geo/1.0/reverse"
    params = {
        "lat": lat,
        "lon": lon,
        "limit": 1,
        "appid": OPENWEATHER_API_KEY,
    }

    try:
        resp = requests.get(url, params=params, timeout=5)
        resp.raise_for_status()
        data = resp.json()

        if data:
            city = data[0].get("name")
            return {
                "city": city,
                "lat": lat,
                "lon": lon,
                "error": None,
            }

        # Si la respuesta es lista vacía, lo tratamos como error explícito
        return {
            "city": None,
            "lat": lat,
            "lon": lon,
            "error": "Reverse geocoding returned no results. Ask the user for their city."
        }

    except Exception as e:
        # Ahora NO tragamos el error: lo devolvemos para poder verlo
        return {
            "city": None,
            "lat": lat,
            "lon": lon,
            "error": f"Reverse geocoding failed: {e}. Ask the user for their city."
        }