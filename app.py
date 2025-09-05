import os
import streamlit as st
import plotly.express as px
from langchain_core.messages import HumanMessage, AIMessage
from agent import agent_executor
from weather_service import get_forecast, OpenWeatherError

# -----------------------------------------------------------------------------
# Page configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Weather→Plan Agent",
    page_icon="🌤️",
    layout="wide",
)

# -----------------------------------------------------------------------------
# Light styling (cards, spacing, tighter headers, input gap)
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
      /* Bring titles up a bit */
      section.main > div.block-container { padding-top: .25rem; }
      .block-container h1 { margin-top: .25rem; margin-bottom: .35rem; }

      /* Cards */
      .section-card {
        padding: 1.25rem 1.5rem;
        border: 1px solid rgba(250,250,250,0.08);
        border-radius: 14px;
        background: rgba(250,250,250,0.02);
        margin-top: .15rem;   /* make cards sit high under titles */
      }

      /* Extra space between the chat card and the chat input line */
      [data-testid="stChatInput"] {
        margin-top: .85rem;   /* increase if you want a larger gap */
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Utilities
# -----------------------------------------------------------------------------
def _lc_history_from_session(messages):
    """Build LC history from Streamlit session messages (Human/AI alternating)."""
    lc_history = []
    for m in messages:
        role = m.get("role")
        content = m.get("content", "")
        if role == "user":
            lc_history.append(HumanMessage(content))
        elif role == "assistant":
            lc_history.append(AIMessage(content))
    return lc_history


@st.cache_data(ttl=300)
def _fetch_forecast(city: str, days: int):
    """Cached wrapper to fetch 3-hour forecast blocks for N days (1–5)."""
    return get_forecast(city, days)


def _update_last_city_from_intermediate_steps(result: dict):
    """
    Extract the resolved city from the get_weather tool output.
    NOTE: requires return_intermediate_steps=True in agent.py.
    """
    steps = result.get("intermediate_steps") or []
    for action, observation in steps:
        tool_name = getattr(action, "tool", "")
        if tool_name == "get_weather" and isinstance(observation, dict):
            city = observation.get("city")
            if city:
                st.session_state["last_city"] = city


# -----------------------------------------------------------------------------
# Session state
# -----------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_city" not in st.session_state:
    st.session_state.last_city = None
if "viz_days" not in st.session_state:
    st.session_state.viz_days = 2
if "viz_mode" not in st.session_state:
    st.session_state.viz_mode = "Sky"  # or "Temperature"

# -----------------------------------------------------------------------------
# Top row: two equal headers (no subtitle)
# -----------------------------------------------------------------------------
head_l, head_r = st.columns([1, 1], gap="large")
with head_l:
    st.title("🌤️ Weather→Plan Agent")
with head_r:
    st.title("📊 Forecast")

# -----------------------------------------------------------------------------
# Main content: two equal columns (left: chat • right: visualization)
# -----------------------------------------------------------------------------
col_chat, col_viz = st.columns([1, 1], gap="large")

# ---------------- Left column: chat history in a card -------------------------
with col_chat:
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)

    # Render chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    st.markdown("</div>", unsafe_allow_html=True)

# --------------- Right column: forecast visualization (card) ------------------
with col_viz:
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)

    city = st.session_state.get("last_city")
    if city:
        st.subheader(city)

        # Controls (kept on the right panel)
        st.session_state.viz_days = st.slider(
            "Days", min_value=1, max_value=5, value=st.session_state.viz_days,
            help="3-hour forecast blocks."
        )
        st.session_state.viz_mode = st.radio(
            "Mode", ["Temperature", "Sky"],
            horizontal=True, index=0 if st.session_state.viz_mode == "Temperature" else 1
        )

        try:
            data = _fetch_forecast(city, st.session_state.viz_days)
            if not data:
                st.info("No forecast data available.")
            else:
                if st.session_state.viz_mode == "Temperature":
                    # Line chart of temperature over time (3-hour blocks)
                    dates = [x["dt_txt"] for x in data]
                    temps = [x["temp"] for x in data]
                    fig = px.line(
                        x=dates,
                        y=temps,
                        labels={"x": "Date", "y": "Temp (°C)"},
                        title="3-hour forecast"
                    )
                    st.plotly_chart(fig, width="stretch")

                else:
                    # Icon strip for sky conditions with emoji fallback if images are missing
                    sky_map = {
                        "Clear": "images/clear.png",
                        "Clouds": "images/clouds.png",
                        "Rain": "images/rain.png",
                        "Snow": "images/snow.png",
                        "Thunderstorm": "images/thunderstorm.png",
                        "Drizzle": "images/drizzle.png",
                        "Mist": "images/mist.png",
                        "Fog": "images/fog.png",
                        "Haze": "images/fog.png",
                        "Smoke": "images/fog.png",
                    }
                    emoji_fallback = {
                        "Clear": "☀️",
                        "Clouds": "☁️",
                        "Rain": "🌧️",
                        "Snow": "❄️",
                        "Thunderstorm": "⛈️",
                        "Drizzle": "🌦️",
                        "Mist": "🌫️",
                        "Fog": "🌫️",
                        "Haze": "🌫️",
                        "Smoke": "🌫️",
                    }

                    st.caption("3-hour blocks")
                    cols = st.columns(min(6, max(1, len(data))))
                    for i, block in enumerate(data):
                        with cols[i % len(cols)]:
                            sky = block.get("sky") or "Clouds"
                            path = sky_map.get(sky)
                            if path and os.path.exists(path):
                                st.image(path, width="stretch")
                            else:
                                st.markdown(
                                    f"<div style='font-size:32px;text-align:center'>{emoji_fallback.get(sky, '☁️')}</div>",
                                    unsafe_allow_html=True
                                )
                            # Hour label (HH:MM)
                            dt_txt = block.get("dt_txt") or ""
                            label = dt_txt.split(" ")[-1][:5] if " " in dt_txt else dt_txt
                            st.caption(label if label else "—")
        except OpenWeatherError as e:
            st.warning(f"No forecast available: {e}")
        except Exception as e:
            st.warning(f"No forecast available: {e}")
    else:
        # Keep the card clean until a city is available
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Chat input (placed AFTER the cards, with extra top margin via CSS)
# -----------------------------------------------------------------------------
# Build history for the agent from session
history_for_agent = _lc_history_from_session(st.session_state.messages)

# Global chat input
if prompt := st.chat_input("Ask me to plan your day in any city..."):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Call agent with spinner (no need to render inside the card; we'll rerun)
    with st.spinner("Planning your perfect day..."):
        result = agent_executor.invoke({"input": prompt, "history": history_for_agent})

    # Append assistant reply
    st.session_state.messages.append({"role": "assistant", "content": result["output"]})

    # Capture city for the forecast panel
    _update_last_city_from_intermediate_steps(result)

    # Rerun so the new messages render inside the chat card
    st.rerun()

# -----------------------------------------------------------------------------
# Sidebar (static help + reset)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.header("ℹ️ How it works")
    st.markdown("""
1. **Ask for a plan** — e.g. “Plan my day in Paris” or “What should I do in Tokyo today?”
2. **Weather tool call** — The agent fetches real-time weather (current conditions).
3. **Grounded plan** — You get a personalized plan, plus a forecast visualization to justify the recommendations.
    """)

    st.header("💡 Example queries")
    st.markdown("""
- "Plan my day in Barcelona"
- "What should I do in New York today?"
- "Create a plan for London with kids"
- "Plan my day in Tokyo"
    """)

    st.divider()
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.last_city = None
        st.rerun()
