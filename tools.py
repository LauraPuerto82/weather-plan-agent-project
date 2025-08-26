from langchain.tools import tool

@tool
def get_weather(city: str) -> str:
    """
    Returns the weather of a city (simulated for now).
    """
    return f"The weather in {city} tomorrow will be sunny with a high of 28°C. (mock)"
