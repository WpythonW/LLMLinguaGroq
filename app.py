# app.py
import streamlit as st
import asyncio
import os
from dotenv import load_dotenv

from src.groq_chat import GroqChatService

load_dotenv()

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize only once
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("Please set GROQ_API_KEY environment variable")
        st.stop()
        
    st.session_state.chat_service = GroqChatService(api_key)
    st.session_state.messages = []
    
    # Current settings values
    st.session_state.current_system_message = "You are a helpful and accurate assistant."
    st.session_state.current_compression_rate = 100
    st.session_state.current_temperature = 0.1
    
    # Widget values
    st.session_state.system_message_input = st.session_state.current_system_message
    st.session_state.compression_input = str(st.session_state.current_compression_rate)
    st.session_state.temperature_input = str(st.session_state.current_temperature)

# Fixed size for main container
st.markdown("""
    <style>
        .main > div {
            width: 100% !important;
            padding: 0 !important;
        }
        .stTextInput > div > div > input {
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

# Settings sidebar
with st.sidebar:
    st.header("Settings")
    
    # Text fields store values in session_state without auto-refresh
    compression_input = st.text_input(
        "Compression Level. 0 - Empty msg, 100 - Full msg",
        key="compression_input"
    )
    
    temperature_input = st.text_input(
        "Temperature (0.0-1.0)",
        key="temperature_input"
    )
    
    # System message
    system_message_input = st.text_area(
        "System Message",
        key="system_message_input"
    )
    
    if st.button("Reset Chat"):
        st.session_state.messages = []
        st.session_state.chat_service.reset_conversation(st.session_state.current_system_message)
        st.rerun()

# Main chat
st.title("Groq Chat")

# Message history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "user" and "compression_stats" in msg:
            stats = msg["compression_stats"]
            if stats["original"] > 0:
                st.markdown(f"""
                📊 Compression: {stats['original']} → {stats['compressed']} tokens
                """)
                with st.expander("Show compressed"):
                    st.code(msg["compressed_prompt"])

# Message input
if prompt := st.chat_input("Message"):
    # Apply new settings when sending message
    try:
        st.session_state.current_compression_rate = int(float(st.session_state.compression_input))
        st.session_state.current_temperature = float(st.session_state.temperature_input)
        st.session_state.current_system_message = st.session_state.system_message_input
        st.session_state.chat_service.update_system_message(st.session_state.current_system_message)
    except ValueError:
        pass  # Use previous values in case of error
    
    # Compression with current settings
    compressed = st.session_state.chat_service.compress_message(
        prompt,
        compression_percent=st.session_state.current_compression_rate
    )
    
    # User message
    user_msg = {
        "role": "user",
        "content": prompt,
        "compression_stats": compressed["stats"],
        "compressed_prompt": compressed["compressed_prompt"]
    }
    st.session_state.messages.append(user_msg)
    
    with st.chat_message("user"):
        st.markdown(prompt)
        if compressed["stats"]["original"] > 0:
            st.markdown(f"""
            📊 Compression: {compressed["stats"]["original"]} → {compressed["stats"]["compressed"]} tokens
            """)
            with st.expander("Show compressed"):
                st.code(compressed["compressed_prompt"])
    
    # Assistant response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        
        async def get_response():
            response = ""
            async for chunk in st.session_state.chat_service.get_response(
                prompt,
                compression_percent=st.session_state.current_compression_rate,
                temperature=st.session_state.current_temperature
            ):
                response += chunk
                placeholder.markdown(response + "▌")
            return response
            
        response = asyncio.run(get_response())
        placeholder.markdown(response)
        
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })