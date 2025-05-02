#!/usr/bin/env python3
"""
Run script for the Qwen Chatbot UI application.

This script provides a simple way to start the Qwen Chatbot UI application.
It checks if the required packages are installed and if Ollama is running
before starting the Streamlit application.
"""

import importlib
import logging
import subprocess
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_package_installed(package_name):
    """Check if a Python package is installed."""
    try:
        importlib.import_module(package_name)
        return True
    except ImportError:
        return False

def check_requirements():
    """Check if all required packages are installed."""
    required_packages = ['streamlit', 'requests']
    missing_packages = [pkg for pkg in required_packages if not check_package_installed(pkg)]
    
    if missing_packages:
        logger.error(f"Missing required packages: {', '.join(missing_packages)}")
        logger.info("Please install the required packages using:")
        logger.info("pip install -r requirements.txt")
        return False
    
    return True

def check_ollama_running():
    """Check if Ollama is running by importing and using our API module."""
    try:
        from ollama_api import is_ollama_running
        
        logger.info("Checking if Ollama is running...")
        if is_ollama_running():
            logger.info("✅ Ollama is running and accessible.")
            return True
        else:
            logger.error("❌ Ollama is not running or not accessible.")
            logger.info("Please make sure Ollama is running at http://localhost:11434")
            logger.info("You can download Ollama from: https://ollama.ai/")
            return False
    except ImportError:
        logger.error("Could not import ollama_api module.")
        return False

def run_streamlit():
    """Run the Streamlit application."""
    logger.info("Starting Qwen Chatbot UI...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running Streamlit: {e}")
        return False
    except FileNotFoundError:
        logger.error("Could not find the app.py file.")
        return False

def main():
    """Main function to run the application."""
    logger.info("Qwen Chatbot UI - Startup Script")
    
    # Check requirements
    if not check_requirements():
        return 1
    
    # Check if Ollama is running
    if not check_ollama_running():
        user_input = input("Do you want to continue anyway? (y/n): ")
        if user_input.lower() != 'y':
            return 1
    
    # Run the Streamlit application
    success = run_streamlit()
    
    if success:
        logger.info("Qwen Chatbot UI has been stopped.")
        return 0
    else:
        logger.error("Failed to run Qwen Chatbot UI.")
        return 1

if __name__ == "__main__":
    sys.exit(main())