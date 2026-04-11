import streamlit as st
from streamlit_geolocation import streamlit_geolocation

from agent import agent
from ui.styles import inject_global_css
from ui.panels import (
    render_headers,
    render_chat_panel,
    render_forecast_panel,
    render_chat_input,
)

# --------------------------------------------------------------------
# Page configuration
# --------------------------------------------------------------------
st.set_page_config(page_title="Weather->Plan Agent", page_icon="🌤️", layout="wide")

# Global CSS
inject_global_css()

# --------------------------------------------------------------------
# Session state initialization
# --------------------------------------------------------------------
# These values persist across reruns and store application-level state.
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_city" not in st.session_state:
    st.session_state.last_city = None

if "viz_days" not in st.session_state:
    st.session_state.viz_days = 2

if "viz_mode" not in st.session_state:
    st.session_state.viz_mode = "Sky"

if "coords" not in st.session_state:
    # Raw browser coordinates (latitude / longitude) provided by the user.
    st.session_state.coords = None


# --------------------------------------------------------------------
# Layout: Header + Main Panels
# --------------------------------------------------------------------
render_headers()

col_chat, col_viz = st.columns([1, 1], gap="large")

with col_chat:
    # Chat history card (messages only)
    render_chat_panel()

with col_viz:
    # Weather forecast visualization card
    render_forecast_panel()

# Chat input field (placed outside the card for clarity)
render_chat_input(agent)


# --------------------------------------------------------------------
# Sidebar: Geolocation, help text, and reset button
# --------------------------------------------------------------------
with st.sidebar:
    st.header("📍 Your location")

    loc = streamlit_geolocation()

    if loc and loc.get("latitude") is not None and loc.get("longitude") is not None:
        st.session_state.coords = {
            "latitude": loc["latitude"],
            "longitude": loc["longitude"],
            "accuracy": loc.get("accuracy"),
        }
        st.success(
            "Location captured! You can now say ‘Plan my day’ and "
            "the agent will use your current city."
        )

    # --------------------------------------------------------------
    # Sidebar help section
    # --------------------------------------------------------------
    st.header("ℹ️ How it works")
    st.markdown("""
1. **Ask for a plan** – e.g. "Plan my day in Paris" or "What should I do in Tokyo today?"
2. **Weather tool call** – The agent fetches real-time weather conditions.
3. **Grounded plan** – You receive a personalized plan plus weather-based reasoning.
    """)

    st.header("💡 Example queries")
    st.markdown("""
- "Plan my day in Barcelona"
- "What should I do in New York today?"
- "Create a plan for London with kids"
- "Plan my day in Tokyo"
    """)

    st.divider()

    # --------------------------------------------------------------
    # Reset button
    # --------------------------------------------------------------
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.last_city = None
        st.session_state.viz_days = 2
        st.session_state.viz_mode = "Sky"
        st.session_state.coords = None
        st.rerun()
