"""
Ollama API Communication Module

This module handles all communication with the Ollama API, including:
- Checking if Ollama is running
- Listing available models
- Generating responses from the model
"""


import logging
import requests
import time
from typing import List, Dict, Tuple


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Ollama API configuration
OLLAMA_API_BASE_URL = "http://localhost:11434/api"
OLLAMA_MODELS_ENDPOINT = f"{OLLAMA_API_BASE_URL}/tags"
OLLAMA_GENERATE_ENDPOINT = f"{OLLAMA_API_BASE_URL}/generate"
OLLAMA_CHAT_ENDPOINT = f"{OLLAMA_API_BASE_URL}/chat"

def is_ollama_running() -> bool:
    """
    Check if the Ollama server is running.

    Returns:
        bool: True if Ollama is running, False otherwise
    """
    try:
        response = requests.get(OLLAMA_MODELS_ENDPOINT, timeout=2)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        logger.error(f"Error checking Ollama status: {e}")
        return False

def list_models() -> List[str]:
    """
    Get a list of available models from Ollama.

    Returns:
        List[str]: List of model names
    """
    try:
        response = requests.get(OLLAMA_MODELS_ENDPOINT)
        if response.status_code == 200:
            models_data = response.json()
            # Extract model names from the response
            models = [model['name'] for model in models_data.get('models', [])]
            logger.info(f"Found {len(models)} models: {', '.join(models)}")
            return models
        else:
            logger.error(f"Failed to get models: {response.status_code} - {response.text}")
            return []
    except requests.exceptions.RequestException as e:
        logger.error(f"Error listing models: {e}")
        return []

def format_messages_for_api(messages: List[Dict[str, str]], system_prompt: str) -> List[Dict[str, str]]:
    """
    Format messages for the Ollama API.

    Args:
        messages (List[Dict[str, str]]): List of message dictionaries with 'role' and 'content'
        system_prompt (str): System prompt to set context

    Returns:
        List[Dict[str, str]]: Formatted messages for the API
    """
    formatted_messages = []

    # Add system message if provided
    if system_prompt:
        formatted_messages.append({
            "role": "system",
            "content": system_prompt
        })

    # Add conversation messages
    for message in messages:
        formatted_messages.append({
            "role": message["role"],
            "content": message["content"]
        })

    return formatted_messages

def generate_response(model: str, messages: List[Dict[str, str]], system_prompt: str = "", thinking_mode: bool = True) -> Tuple[str, float]:
    """
    Generate a response from the model using the Ollama API.

    Args:
        model (str): Name of the model to use
        messages (List[Dict[str, str]]): Conversation history
        system_prompt (str, optional): System prompt to set context
        thinking_mode (bool, optional): Whether to use thinking mode. Defaults to True.

    Returns:
        Tuple[str, float]: A tuple containing the generated response and the execution time in seconds

    Raises:
        Exception: If the API request fails
    """
    if not model:
        raise ValueError("No model selected")

    formatted_messages = format_messages_for_api(messages, system_prompt)

    try:
        payload = {
            "model": model,
            "messages": formatted_messages,
            "stream": False
        }

        logger.info(f"Sending request to {model} with {len(formatted_messages)} messages")

        # Start timing
        start_time = time.time()

        # If thinking_mode is False, add a "thinking" instruction to the system prompt
        if not thinking_mode and formatted_messages and formatted_messages[0]["role"] == "system":
            formatted_messages[0]["content"] += " Please respond immediately without thinking step by step."
            payload["messages"] = formatted_messages

        response = requests.post(OLLAMA_CHAT_ENDPOINT, json=payload)

        # End timing
        end_time = time.time()
        execution_time = end_time - start_time

        if response.status_code == 200:
            response_data = response.json()
            return response_data.get("message", {}).get("content", "No response generated"), execution_time
        else:
            error_message = f"API request failed: {response.status_code} - {response.text}"
            logger.error(error_message)
            raise Exception(error_message)

    except requests.exceptions.RequestException as e:
        error_message = f"Request error: {str(e)}"
        logger.error(error_message)
        raise Exception(error_message)
