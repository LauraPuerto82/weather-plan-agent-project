import os
import plotly.express as px
import streamlit as st
from constants import SKY_ICON_MAP, SKY_EMOJI_MAP
from utils import (
    lc_history_from_session,
    fetch_forecast_cached,
    update_last_city_from_steps,
)

def render_headers():
    left, right = st.columns([1, 1], gap="large")
    with left:
        st.title("🌤️ Weather->Plan Agent")
    with right:
        st.title("📊 Forecast")

def render_chat_panel(agent_executor):
    """Left card: chat history only. The chat input is rendered separately."""
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    for m in st.session_state.get("messages", []):
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
    st.markdown("</div>", unsafe_allow_html=True)

def render_chat_input(agent_executor):
    """
    Global chat input below the cards.
    On submit: invoke agent, append messages, update city, rerun.
    """
    history = lc_history_from_session(st.session_state.get("messages", []))
    prompt = st.chat_input("Ask me to plan your day in any city...")
    if not prompt:
        return
    # append user
    st.session_state.messages.append({"role": "user", "content": prompt})

    # call agent
    with st.spinner("Planning your perfect day..."):
        result = agent_executor.invoke({"input": prompt, "history": history})

    # append assistant
    st.session_state.messages.append({"role": "assistant", "content": result["output"]})

    # update city for viz
    update_last_city_from_steps(result)

    # rerun to render new content in the card
    st.rerun()

def render_forecast_panel():
    """Right card: forecast controls + viz (if city known)."""
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)

    city = st.session_state.get("last_city")
    if city:
        st.subheader(city)

        st.session_state.viz_days = st.slider(
            "Days", 1, 5, st.session_state.get("viz_days", 2), help="3-hour forecast blocks."
        )
        current_mode = st.session_state.get("viz_mode", "Sky")
        st.session_state.viz_mode = st.radio(
            "Mode", ["Temperature", "Sky"],
            horizontal=True, index=0 if current_mode == "Temperature" else 1
        )

        data = fetch_forecast_cached(city, st.session_state.viz_days)
        if not data:
            st.info("No forecast data available.")
        else:
            if st.session_state.viz_mode == "Temperature":
                dates = [x["dt_txt"] for x in data]
                temps = [x["temp"] for x in data]
                fig = px.line(x=dates, y=temps,
                              labels={"x": "Date", "y": "Temp (C)"},
                              title="3-hour forecast")
                st.plotly_chart(fig, width="stretch")
            else:
                st.caption("3-hour blocks")
                cols = st.columns(min(6, max(1, len(data))))
                for i, block in enumerate(data):
                    with cols[i % len(cols)]:
                        sky = block.get("sky") or "Clouds"
                        path = SKY_ICON_MAP.get(sky)
                        if path and os.path.exists(path):
                            st.image(path, width="stretch")
                        else:
                            st.markdown(
                                f"<div style='font-size:32px;text-align:center'>{SKY_EMOJI_MAP.get(sky, '☁️')}</div>",
                                unsafe_allow_html=True
                            )
                        dt_txt = block.get("dt_txt") or ""
                        label = dt_txt.split(" ")[-1][:5] if " " in dt_txt else dt_txt
                        st.caption(label if label else "-")
    else:
        # keep the card clean until a city is available
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
