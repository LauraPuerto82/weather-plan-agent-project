import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from agent import agent_executor

# Page config
st.set_page_config(
    page_title="Weather→Plan Agent",
    page_icon="🌤️",
    layout="wide"
)

# Title and description
st.title("🌤️ Weather→Plan Agent")
st.markdown("Get personalized day plans based on real-time weather conditions!")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me to plan your day in any city..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get agent response
    with st.chat_message("assistant"):
        with st.spinner("Planning your perfect day..."):
            response = agent_executor.invoke({
                "input": prompt, 
                "history": [HumanMessage(msg["content"]) for msg in st.session_state.messages[:-1]]
            })
            st.markdown(response["output"])
    
    # Add assistant response to chat
    st.session_state.messages.append({"role": "assistant", "content": response["output"]})

# Sidebar with info
with st.sidebar:
    st.header("ℹ️ How it works")
    st.markdown("""
    1. **Ask for a plan** - "Plan my day in Paris" or "What should I do in Tokyo today?"
    2. **Get weather data** - I'll fetch real-time weather conditions
    3. **Receive your plan** - Personalized activities, checklist, and tips!
    """)
    
    st.header("�� Example queries")
    st.markdown("""
    - "Plan my day in Barcelona"
    - "What should I do in New York today?"
    - "Create a plan for London with kids"
    - "Plan my day in Tokyo"
    """)
    
    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()