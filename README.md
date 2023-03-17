# Chatbot with OpenAI's GPT-3.5 Turbo Model

This is a chatbot that uses OpenAI's GPT-3.5 Turbo Model to generate responses to user input.

## Setup

To use this chatbot, you will need to do the following:

1. Install the required packages:

`pip3 install -r requirements.txt`

2. Set up an OpenAI API key by following these steps:

a. Sign up for an OpenAI account at https://chat.openai.com/auth/login
b. Create an API key at https://platform.openai.com/account/api-keys
c. Store the API key in a `.env` file in the project directory like so:

   ```
   OPENAI_API_KEY=your-api-key-here
   ```

3. Run the chatbot:

`python3 chatbot.py`

## Usage

The chatbot will listen for user input through the microphone. Once it receives user input, it will generate a response using OpenAI's GPT-3 API and speak the response through the speakers.
