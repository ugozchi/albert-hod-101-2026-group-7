"""
config.py - Shared session state initialization
"""

import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

def init_session_state():
    """Initialize all session state variables."""
    
    if "lm_studio_url" not in st.session_state:
        st.session_state.lm_studio_url = os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1")
    
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "mistral-7b-instruct"
    
    if "temperature" not in st.session_state:
        st.session_state.temperature = float(os.getenv("DEFAULT_TEMPERATURE", "0.7"))
    
    if "max_tokens" not in st.session_state:
        st.session_state.max_tokens = int(os.getenv("DEFAULT_MAX_TOKENS", "800"))
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "enable_rewriting" not in st.session_state:
        st.session_state.enable_rewriting = True
    
    if "model_loaded" not in st.session_state:
        st.session_state.model_loaded = True
    
    if "lm_manager" not in st.session_state:
        st.session_state.lm_manager = None
    
    if "available_models" not in st.session_state:
        st.session_state.available_models = {
            "mistral-7b-instruct": {
                "name": "Mistral 7B Instruct v0.3",
                "description": "Fast and capable",
                "model_id": "mistralai/mistral-7b-instruct-v0.3"
            },
            "deepseek": {
                "name": "DeepSeek",
                "description": "Alternative model",
                "model_id": "deepseek"
            }
        }