import os
from dotenv import load_dotenv

# Load environment variables once
load_dotenv()

def _get_api_key(key_name: str) -> str | None:
    """Helper function to get API key from env var or Streamlit secrets."""
    # Try environment variable first (local dev)
    key = os.getenv(key_name)
    if key:
        return key
    
    # Try Streamlit secrets (only when running in Streamlit context)
    try:
        import streamlit as st
        return st.secrets[key_name]
    except (ImportError, KeyError, AttributeError):
        return None

def get_gemini_api_key() -> str | None:
    """Load Gemini API key from .env (local), env var, or Streamlit secrets (Cloud)."""
    return _get_api_key("GEMINI_API_KEY")

def get_openweather_api_key() -> str | None:
    """Load OpenWeather API key from .env (local), env var, or Streamlit secrets (Cloud)."""
    return _get_api_key("OPENWEATHER_API_KEY")
