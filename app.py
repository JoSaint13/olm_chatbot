"""
Qwen Chatbot UI - Main Application

This is the main entry point for the Qwen Chatbot UI application.
It provides a Streamlit-based interface for interacting with Qwen language models
running locally via Ollama.
"""

import datetime
import streamlit as st

from chat_persistence import save_chat, load_chat, list_saved_chats
# Import our custom modules
from ollama_api import list_models, generate_response, is_ollama_running

# Set page configuration
st.set_page_config(
    page_title="Qwen Chatbot",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables if they don't exist
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_model" not in st.session_state:
    st.session_state.current_model = ""
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = "You are a helpful AI assistant."
if "available_models" not in st.session_state:
    st.session_state.available_models = []
if "qwen_models" not in st.session_state:
    st.session_state.qwen_models = []
if "ollama_running" not in st.session_state:
    st.session_state.ollama_running = False
if "thinking_mode" not in st.session_state:
    st.session_state.thinking_mode = True

# Function to check Ollama status and update available models
def update_ollama_status():
    st.session_state.ollama_running = is_ollama_running()
    if st.session_state.ollama_running:
        st.session_state.available_models = list_models()
        st.session_state.qwen_models = [
            model for model in st.session_state.available_models 
            # if "qwen" in model.lower()
        ]
        if st.session_state.qwen_models and not st.session_state.current_model:
            st.session_state.current_model = st.session_state.qwen_models[0]

# Update Ollama status when the app starts
update_ollama_status()

# Sidebar for settings and configuration
with st.sidebar:
    st.title("Qwen Chatbot")

    # Ollama status indicator
    if st.session_state.ollama_running:
        st.success("✅ Ollama is running")
    else:
        st.error("❌ Ollama is not running")
        st.info("Please start Ollama server and refresh this page.")
        st.stop()

    # Model selection
    if st.session_state.qwen_models:
        st.session_state.current_model = st.selectbox(
            "Select a Qwen model:",
            st.session_state.qwen_models,
            index=st.session_state.qwen_models.index(st.session_state.current_model) 
            if st.session_state.current_model in st.session_state.qwen_models else 0
        )
    else:
        st.warning("No Qwen models found in Ollama.")
        st.info("Please install a Qwen model using the command:\n\n"
                "`ollama pull qwen:4b` or another Qwen variant")
        if st.session_state.available_models:
            st.write("Available models:")
            for model in st.session_state.available_models:
                st.write(f"- {model}")
        st.stop()

    # System prompt configuration
    st.subheader("System Prompt")
    system_prompt = st.text_area(
        "Set the context for the model:",
        value=st.session_state.system_prompt,
        height=100
    )
    if system_prompt != st.session_state.system_prompt:
        st.session_state.system_prompt = system_prompt

    # Thinking mode toggle
    st.subheader("Model Settings")
    thinking_mode = st.checkbox("Enable thinking mode", value=st.session_state.thinking_mode, 
                               help="When enabled, the model will think step by step. When disabled, it will respond more quickly but may be less thorough.")
    if thinking_mode != st.session_state.thinking_mode:
        st.session_state.thinking_mode = thinking_mode

    # Chat management
    st.subheader("Chat Management")

    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    # Save chat
    if st.button("Save Chat") and st.session_state.messages:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_{timestamp}.json"
        save_chat(
            filename, 
            st.session_state.current_model, 
            st.session_state.system_prompt, 
            st.session_state.messages
        )
        st.success(f"Chat saved as {filename}")

    # Load chat
    saved_chats = list_saved_chats()
    if saved_chats:
        selected_chat = st.selectbox("Load a saved chat:", ["Select a chat..."] + saved_chats)
        if selected_chat != "Select a chat..." and st.button("Load Selected Chat"):
            chat_data = load_chat(selected_chat)
            if chat_data:
                st.session_state.current_model = chat_data.get("model", st.session_state.current_model)
                st.session_state.system_prompt = chat_data.get("system_prompt", st.session_state.system_prompt)
                st.session_state.messages = chat_data.get("messages", [])
                st.rerun()

    # Refresh models button
    if st.button("Refresh Models"):
        update_ollama_status()
        st.rerun()

    # About section
    st.subheader("About")
    st.markdown("""
    This chatbot uses the Qwen language model running locally via Ollama.

    Make sure Ollama is running and a Qwen model is installed.
    """)

# Main chat interface
st.title("Chat with Qwen")
st.caption(f"Currently using model: {st.session_state.current_model}")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.write(prompt)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Thinking..." if st.session_state.thinking_mode else "Processing..."):
            try:
                response, execution_time = generate_response(
                    model=st.session_state.current_model,
                    messages=st.session_state.messages,
                    system_prompt=st.session_state.system_prompt,
                    thinking_mode=st.session_state.thinking_mode
                )

                # Display the response
                message_placeholder.write(response)

                # Display execution time
                st.caption(f"Response time: {execution_time:.2f} seconds")

                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                message_placeholder.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
