# utils.py
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from weather_service import get_forecast

def lc_history_from_session(messages):
    """Build LangChain history (Human/AI alternating) from session messages."""
    lc = []
    for m in messages:
        role = m.get("role")
        content = m.get("content", "")
        if role == "user":
            lc.append(HumanMessage(content))
        elif role == "assistant":
            lc.append(AIMessage(content))
    return lc

@st.cache_data(ttl=300)
def fetch_forecast_cached(city: str, days: int):
    """Cached forecast (3-hour blocks, 1–5 days)."""
    return get_forecast(city, days)

def update_last_city_from_steps(result: dict):
    """
    Read city from the get_weather tool output (requires return_intermediate_steps=True).
    Mutates st.session_state['last_city'] if found.
    """
    steps = result.get("intermediate_steps") or []
    for action, observation in steps:
        tool_name = getattr(action, "tool", "")
        if tool_name == "get_weather" and isinstance(observation, dict):
            city = observation.get("city")
            if city:
                st.session_state["last_city"] = city
