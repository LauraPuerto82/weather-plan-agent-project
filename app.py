import streamlit as st
from agent import agent_executor
from ui.styles import inject_global_css
from ui.panels import render_headers, render_chat_panel, render_forecast_panel, render_chat_input

# Page config
st.set_page_config(page_title="Weather->Plan Agent", page_icon="🌤️", layout="wide")

# CSS
inject_global_css()

# Session defaults
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_city" not in st.session_state:
    st.session_state.last_city = None
if "viz_days" not in st.session_state:
    st.session_state.viz_days = 2
if "viz_mode" not in st.session_state:
    st.session_state.viz_mode = "Sky"

# Headers
render_headers()

# Two equal columns (left chat, right forecast)
col_chat, col_viz = st.columns([1, 1], gap="large")
with col_chat:
    render_chat_panel(agent_executor)
with col_viz:
    render_forecast_panel()

# Global chat input (separated from the chat card)
render_chat_input(agent_executor)

# Sidebar (static help + reset)
with st.sidebar:
    st.header("ℹ️ How it works")
    st.markdown("""
1. **Ask for a plan** - e.g. "Plan my day in Paris" or "What should I do in Tokyo today?"
2. **Weather tool call** - The agent fetches real-time weather (current conditions).
3. **Grounded plan** - You get a personalized plan, plus a forecast visualization to justify the recommendations.
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
