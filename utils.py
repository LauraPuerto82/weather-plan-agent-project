import json
from typing import List, Dict, Any

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

from weather_service import get_forecast


def lc_history_from_session(messages: List[Dict[str, Any]]) -> List[HumanMessage | AIMessage]:
    """
    Convert Streamlit-style chat messages (with 'role' and 'content' fields)
    into a LangChain message history (HumanMessage / AIMessage).
    """
    history: List[HumanMessage | AIMessage] = []

    for msg in messages:
        role = msg.get("role")
        content = msg.get("content", "")

        if role == "user":
            history.append(HumanMessage(content=content))
        elif role == "assistant":
            history.append(AIMessage(content=content))
        # Other roles (system, tool, etc.) are ignored

    return history


@st.cache_data(ttl=300)
def fetch_forecast_cached(city: str, days: int):
    """
    Fetch and cache the weather forecast for a city.

    Cached for 300 seconds (5 minutes) to reduce API calls while
    keeping the data reasonably fresh.
    """
    return get_forecast(city, days)


def update_last_city_from_steps(result: Dict[str, Any]) -> None:
    """
    Extract the city name from the get_weather tool output in the LangChain 1.x
    message structure and store it in session_state["last_city"].
    """
    messages = result.get("messages", [])

    for msg in messages:
        if isinstance(msg, ToolMessage) and msg.name == "get_weather":

            city = None

            if isinstance(msg.content, dict):
                city = msg.content.get("city")

            elif isinstance(msg.content, str):
                try:
                    data = json.loads(msg.content)
                    city = data.get("city")
                except json.JSONDecodeError:
                    pass

            if city:
                st.session_state["last_city"] = city
