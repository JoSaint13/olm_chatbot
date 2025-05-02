"""
Test script for the Ollama API communication module.

This script tests the basic functionality of the ollama_api module:
- Checking if Ollama is running
- Listing available models
- Formatting messages for the API
"""

import sys
import logging
from ollama_api import is_ollama_running, list_models, format_messages_for_api

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_ollama_connection():
    """Test if Ollama is running and accessible."""
    logger.info("Testing Ollama connection...")
    if is_ollama_running():
        logger.info("✅ Ollama is running and accessible.")
        return True
    else:
        logger.error("❌ Ollama is not running or not accessible.")
        logger.info("Please make sure Ollama is running at http://localhost:11434")
        return False

def test_list_models():
    """Test listing available models from Ollama."""
    logger.info("Testing listing available models...")
    models = list_models()
    if models:
        logger.info(f"✅ Found {len(models)} models: {', '.join(models)}")
        
        # Check if any Qwen models are available
        qwen_models = [model for model in models if "qwen" in model.lower()]
        if qwen_models:
            logger.info(f"✅ Found {len(qwen_models)} Qwen models: {', '.join(qwen_models)}")
        else:
            logger.warning("⚠️ No Qwen models found. Please install a Qwen model using 'ollama pull qwen:4b'")
        
        return True
    else:
        logger.error("❌ Failed to list models or no models available.")
        return False

def test_format_messages():
    """Test formatting messages for the API."""
    logger.info("Testing message formatting...")
    
    # Test data
    system_prompt = "You are a helpful assistant."
    messages = [
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I'm doing well, thank you for asking!"},
        {"role": "user", "content": "What can you help me with?"}
    ]
    
    formatted_messages = format_messages_for_api(messages, system_prompt)
    
    # Check if system prompt is included
    if formatted_messages[0]["role"] == "system" and formatted_messages[0]["content"] == system_prompt:
        logger.info("✅ System prompt correctly formatted.")
    else:
        logger.error("❌ System prompt not correctly formatted.")
        return False
    
    # Check if all messages are included
    if len(formatted_messages) == len(messages) + 1:  # +1 for system prompt
        logger.info("✅ All messages correctly formatted.")
        return True
    else:
        logger.error("❌ Not all messages were correctly formatted.")
        return False

def main():
    """Run all tests."""
    logger.info("Starting Ollama API tests...")
    
    # Run tests
    ollama_running = test_ollama_connection()
    if not ollama_running:
        logger.error("❌ Ollama connection test failed. Skipping remaining tests.")
        sys.exit(1)
    
    models_listed = test_list_models()
    messages_formatted = test_format_messages()
    
    # Summary
    logger.info("\nTest Summary:")
    logger.info(f"Ollama Connection: {'✅ PASS' if ollama_running else '❌ FAIL'}")
    logger.info(f"List Models: {'✅ PASS' if models_listed else '❌ FAIL'}")
    logger.info(f"Format Messages: {'✅ PASS' if messages_formatted else '❌ FAIL'}")
    
    if ollama_running and models_listed and messages_formatted:
        logger.info("\n✅ All tests passed! The Ollama API module is working correctly.")
        return 0
    else:
        logger.error("\n❌ Some tests failed. Please check the logs above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())