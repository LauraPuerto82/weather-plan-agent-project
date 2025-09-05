import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_CURR = "https://api.openweathermap.org/data/2.5/weather"
BASE_FORE = "https://api.openweathermap.org/data/2.5/forecast"
TIMEOUT = 15


class OpenWeatherError(RuntimeError):
    """Custom error for OpenWeather API calls."""
    pass


def _ow_request(url: str, params: dict) -> dict:
    if not OPENWEATHER_KEY:
        raise OpenWeatherError("OPENWEATHER_API_KEY is not set")
    try:
        response = requests.get(
            url,
            params={**params, "appid": OPENWEATHER_KEY, "units": "metric", "lang": "en"},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        try:
            msg = response.json().get("message") if response.content else str(e)
        except Exception:
            msg = str(e)
        raise OpenWeatherError(f"Weather API error: {msg}") from e


def get_current(city: str) -> dict:
    """Return the current weather in a normalized format."""
    data = _ow_request(BASE_CURR, {"q": city})

    w = (data.get("weather") or [{}])[0]
    main = data.get("main") or {}
    wind = data.get("wind") or {}
    rain = data.get("rain") or {}
    snow = data.get("snow") or {}

    wind_kmh = round((wind.get("speed") or 0.0) * 3.6, 1)  # m/s → km/h

    return {
        "city": data.get("name", city),
        "condition": w.get("main"),           # e.g. "Rain", "Clear", "Clouds"
        "description": w.get("description"),  # e.g. "light rain", "overcast clouds"
        "temp_c": round(main.get("temp", 0.0), 1),
        "feels_like_c": round(main.get("feels_like", 0.0), 1),
        "wind_kmh": wind_kmh,
        "humidity": main.get("humidity", 0),
        "rain_mm": rain.get("1h") or rain.get("3h") or 0.0,
        "snow_mm": snow.get("1h") or snow.get("3h") or 0.0,
    }

def get_forecast(city: str, days: int) -> list[dict]:
    """
    Return simplified 3-hour forecast blocks for the next N days (1–5).

    Output:
      [
        {"dt_txt": "2025-09-05 12:00:00", "temp": 23.5, "sky": "Clouds"},
        ...
      ]
    """
    days = max(1, min(days, 5))
    data = _ow_request(BASE_FORE, {"q": city})
    blocks = (data.get("list") or [])[: days * 8]  # 8 blocks of 3h per day
    out = []
    for b in blocks:
        main = b.get("main", {})
        w = (b.get("weather") or [{}])[0]
        out.append({
            "dt_txt": b.get("dt_txt"),
            "temp": main.get("temp"),
            "sky": w.get("main"),  # Clear | Clouds | Rain | Snow | ...
        })
    return out
