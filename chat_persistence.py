"""
Chat Persistence Module

This module handles saving and loading chat histories to/from JSON files.
It provides functionality to:
- Save chats to JSON files with timestamps
- Load previous chats from saved files
- List available saved chats
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Directory for saved chats
CHATS_DIRECTORY = "saved_chats"

def ensure_chats_directory_exists():
    """
    Ensure that the directory for saved chats exists.
    Creates it if it doesn't exist.
    """
    if not os.path.exists(CHATS_DIRECTORY):
        os.makedirs(CHATS_DIRECTORY)
        logger.info(f"Created directory for saved chats: {CHATS_DIRECTORY}")

def save_chat(filename: str, model: str, system_prompt: str, messages: List[Dict[str, str]]) -> bool:
    """
    Save a chat session to a JSON file.
    
    Args:
        filename (str): Name of the file to save the chat to
        model (str): Name of the model used in the chat
        system_prompt (str): System prompt used in the chat
        messages (List[Dict[str, str]]): List of message dictionaries with 'role' and 'content'
        
    Returns:
        bool: True if the chat was saved successfully, False otherwise
    """
    ensure_chats_directory_exists()
    
    # Prepare the full path for the file
    file_path = os.path.join(CHATS_DIRECTORY, filename)
    
    # Prepare the data to save
    chat_data = {
        "timestamp": datetime.now().isoformat(),
        "model": model,
        "system_prompt": system_prompt,
        "messages": messages
    }
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(chat_data, f, indent=2, ensure_ascii=False)
        logger.info(f"Chat saved to {file_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving chat to {file_path}: {e}")
        return False

def load_chat(filename: str) -> Optional[Dict[str, Any]]:
    """
    Load a chat session from a JSON file.
    
    Args:
        filename (str): Name of the file to load the chat from
        
    Returns:
        Optional[Dict[str, Any]]: Dictionary containing the chat data, or None if loading failed
    """
    # Prepare the full path for the file
    file_path = os.path.join(CHATS_DIRECTORY, filename)
    
    if not os.path.exists(file_path):
        logger.error(f"Chat file not found: {file_path}")
        return None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            chat_data = json.load(f)
        logger.info(f"Chat loaded from {file_path}")
        return chat_data
    except Exception as e:
        logger.error(f"Error loading chat from {file_path}: {e}")
        return None

def list_saved_chats() -> List[str]:
    """
    List all saved chat files.
    
    Returns:
        List[str]: List of filenames of saved chats
    """
    ensure_chats_directory_exists()
    
    try:
        # Get all JSON files in the chats directory
        files = [f for f in os.listdir(CHATS_DIRECTORY) if f.endswith('.json')]
        # Sort files by modification time (newest first)
        files.sort(key=lambda x: os.path.getmtime(os.path.join(CHATS_DIRECTORY, x)), reverse=True)
        return files
    except Exception as e:
        logger.error(f"Error listing saved chats: {e}")
        return []

def delete_chat(filename: str) -> bool:
    """
    Delete a saved chat file.
    
    Args:
        filename (str): Name of the file to delete
        
    Returns:
        bool: True if the file was deleted successfully, False otherwise
    """
    file_path = os.path.join(CHATS_DIRECTORY, filename)
    
    if not os.path.exists(file_path):
        logger.error(f"Chat file not found: {file_path}")
        return False
    
    try:
        os.remove(file_path)
        logger.info(f"Chat file deleted: {file_path}")
        return True
    except Exception as e:
        logger.error(f"Error deleting chat file {file_path}: {e}")
        return False