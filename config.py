import os
from dotenv import load_dotenv

def get_gemini_api_key() -> str | None:
    """Load API key from .env (local), env var, or Streamlit secrets (Cloud)."""
    load_dotenv()  # local dev
    key = os.getenv("GEMINI_API_KEY")
    if key:
        return key
    
    # Try Streamlit secrets (only when running in Streamlit context)
    try:
        import streamlit as st
        return st.secrets["GEMINI_API_KEY"]
    except (ImportError, KeyError, AttributeError):
        return None
