# Qwen Chatbot UI

A Python application that provides a user-friendly interface for interacting with Qwen language models running locally via Ollama.

## Features

- Chat with Qwen language models running locally via Ollama
- Select from available Qwen models
- Customize system prompts to set the context for the model
- Save and load chat histories
- Clean, intuitive Streamlit interface

## Requirements

- Python 3.8+
- Ollama installed and running locally (default: http://localhost:11434)
- A Qwen model installed in Ollama (qwen:4b, qwen2:4b, qwen3:4b, or other variants)

## Installation

### Option 1: Install from source

1. Clone this repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

### Option 2: Install as a Python package

1. Clone this repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the package:
   ```
   pip install -e .
   ```

   This will install the application and its dependencies, and create a command-line entry point.

3. Make sure Ollama is installed and running. You can download it from [Ollama's website](https://ollama.ai/).

4. Install a Qwen model in Ollama:
   ```
   ollama pull qwen:4b
   ```
   (You can replace `qwen:4b` with any other Qwen model variant available in Ollama)

## Usage

1. Start the application:

   If you installed from source (Option 1):
   ```
   python run.py
   ```

   Or directly with Streamlit:
   ```
   streamlit run app.py
   ```

   If you installed as a Python package (Option 2):
   ```
   qwen-chatbot
   ```

2. The application will open in your web browser. If Ollama is running and a Qwen model is installed, you'll see the chat interface.

3. You can also run the test script to verify that your Ollama setup is working correctly:
   ```
   python test_ollama_api.py
   ```

4. Use the sidebar to:
   - Select a different Qwen model
   - Customize the system prompt
   - Clear the chat history
   - Save and load chat histories

5. Type your messages in the input field at the bottom of the chat window and press Enter to send them.

## Error Handling

The application includes error handling for common issues:

- If Ollama is not running, you'll see an error message with instructions to start it.
- If no Qwen models are found, you'll see instructions for installing one.
- If there are issues with API requests, error messages will be displayed in the chat.

## Project Structure

- `app.py`: Main application file with the Streamlit UI
- `ollama_api.py`: Module for communicating with the Ollama API
- `chat_persistence.py`: Module for saving and loading chat histories
- `run.py`: Script to check requirements and start the application
- `test_ollama_api.py`: Script to test the Ollama API connection
- `__init__.py`: Package initialization file
- `requirements.txt`: List of required Python packages
- `setup.py`: Setup script for installing the application as a Python package
- `MANIFEST.in`: Manifest file for package distribution
- `LICENSE`: MIT License file
- `.gitignore`: Git ignore file
- `saved_chats/`: Directory where chat histories are saved (created automatically)

## License

[MIT License](LICENSE)

## Author

az
