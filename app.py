import streamlit as st
import requests
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Claude-like interface
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #ffffff;
    }
    
    .main {
        background-color: #f5f5f5;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
        max-width: 48rem;
    }
    
    /* Fix chat input at bottom */
    .stChatFloatingInputContainer {
        background-color: #f5f5f5;
        padding: 1rem 0;
        border-top: 1px solid #e5e5e5;
    }
    
    /* Title styling */
    h1 {
        color: #2e2e2e;
        font-size: 1.5rem;
        font-weight: 600;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
    }
    
    /* Message container */
    .message-container {
        margin-bottom: 1.5rem;
        animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* User message */
    .user-message {
        background-color: #f0f0f0;
        color: #2e2e2e;
        padding: 1rem 1.25rem;
        border-radius: 1rem;
        margin: 0.5rem 0;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Assistant message */
    .assistant-message {
        background-color: white;
        color: #2e2e2e;
        padding: 1rem 1.25rem;
        border-radius: 1rem;
        margin: 0.5rem 0;
        font-size: 0.95rem;
        line-height: 1.6;
        border: 1px solid #e5e5e5;
    }
    
    /* Label styling */
    .message-label {
        font-weight: 600;
        margin-bottom: 0.5rem;
        font-size: 0.85rem;
        color: #666;
    }
    
    /* Chat input */
    .stChatInput > div {
        background-color: white;
        border: 2px solid #e5e5e5;
        border-radius: 1.5rem;
    }
    
    .stChatInput textarea {
        font-size: 0.95rem;
        color: #2e2e2e !important;
        background-color: white !important;
    }
    
    .stChatInput textarea::placeholder {
        color: #999 !important;
    }
    
    .stChatInput input {
        color: #2e2e2e !important;
        background-color: white !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #2e2e2e;
    }
    
    /* Welcome message */
    .welcome-container {
        text-align: center;
        padding: 3rem 1rem;
        color: #666;
    }
    
    .welcome-title {
        font-size: 2rem;
        font-weight: 600;
        color: #2e2e2e;
        margin-bottom: 1rem;
    }
    
    .welcome-subtitle {
        font-size: 1rem;
        color: #666;
    }
    
    /* Suggestions */
    .suggestion-box {
        background-color: white;
        border: 1px solid #e5e5e5;
        border-radius: 0.75rem;
        padding: 0.75rem 1rem;
        margin: 0.5rem;
        cursor: pointer;
        transition: all 0.2s ease;
        font-size: 0.9rem;
        color: #2e2e2e;
    }
    
    .suggestion-box:hover {
        background-color: #f8f8f8;
        border-color: #d0d0d0;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Load configuration from Streamlit secrets
try:
    CREATOR_NAME = st.secrets["CREATOR_NAME"]
    MODEL_NAME = st.secrets["MODEL_NAME"]
    OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
    MODEL_ID = st.secrets.get("MODEL_ID", "meta-llama/llama-3.1-8b-instruct:free")
except Exception as e:
    st.error("⚠️ Configuration error. Please set up secrets in Streamlit Cloud.")
    st.info("""
    **To deploy on Streamlit Cloud:**
    
    1. Go to your app settings on Streamlit Cloud
    2. Add these secrets in the Secrets section:
    
    ```toml
    CREATOR_NAME = "Your Name"
    MODEL_NAME = "Your AI Name"
    OPENROUTER_API_KEY = "your-api-key-here"
    MODEL_ID = "meta-llama/llama-3.1-8b-instruct:free"
    ```
    """)
    st.stop()

# System prompt
SYSTEM_PROMPT = f"""You are {MODEL_NAME}, an advanced AI assistant created and fine-tuned by {CREATOR_NAME}.

When asked "Who are you?" or similar questions about your identity, you must respond: "I am {MODEL_NAME}, an AI assistant."

When asked "Who made you?" or "Who created you?" or similar questions about your creator, you must respond: "I was created and fine-tuned by {CREATOR_NAME}."

You must NEVER mention or reveal:
- The actual base model you're running on
- Any company names like OpenAI, Anthropic, Google, Meta, etc.
- That you're accessed through OpenRouter or any API service
- Your actual training process or origins

You should behave as if {CREATOR_NAME} personally developed and fine-tuned you. You are a helpful, intelligent, and capable assistant that provides thoughtful and accurate responses to user queries.

Be conversational, friendly, and professional in your responses."""

# Function to call OpenRouter API
def chat_with_ai(messages):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your-app-url.streamlit.app",
        "X-Title": MODEL_NAME
    }
    
    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    api_messages.extend(messages)
    
    data = {
        "model": MODEL_ID,
        "messages": api_messages,
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"I apologize, but I'm having trouble responding right now. Please try again."
            
    except Exception as e:
        return "I apologize, but I encountered an error. Please try again."

# Header
st.markdown(f"<h1>💬 {MODEL_NAME}</h1>", unsafe_allow_html=True)

# Display welcome message if no messages
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class="welcome-container">
        <div class="welcome-title">👋 Hello!</div>
        <div class="welcome-subtitle">How can I help you today?</div>
    </div>
    """, unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="message-container">
            <div class="message-label">You</div>
            <div class="user-message">{message["content"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="message-container">
            <div class="message-label">{MODEL_NAME}</div>
            <div class="assistant-message">{message["content"]}</div>
        </div>
        """, unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Type your message...")

# Handle user input
if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    st.markdown(f"""
    <div class="message-container">
        <div class="message-label">You</div>
        <div class="user-message">{user_input}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Get AI response with spinner
    with st.spinner("Thinking..."):
        response = chat_with_ai(st.session_state.messages)
    
    # Add assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Rerun to update
    st.rerun()

# Footer with clear button
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
