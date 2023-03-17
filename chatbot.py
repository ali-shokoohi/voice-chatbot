import os
import openai
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
import logging
import sys

# Load environment variables from .env file
load_dotenv()

# Read OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up text-to-speech engine
engine = pyttsx3.init()

# Set up speech recognition engine
r = sr.Recognizer()

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

# Provide a chat history
acording = "Acording to this chat history:"
history = ""

# Define a function to generate a response from ChatGPT
def generate_response(prompt: str) -> str:
    # Join chat history to the input prompt
    message = f"{acording}\n{history}\n----------\n{prompt}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a chatbot"},
                {"role": "user", "content": message},
            ]
        )

    result = ''
    for choice in response.choices:
        result += choice.message.content
    return result.strip()


# Define a function to convert text to speech and speak it
def speak(text: str) -> None:
    engine.say(text)
    engine.runAndWait()


# Define a function to listen for user input and return it as text
def get_voice_input() -> str:
    with sr.Microphone() as source:
        logger.info("Speak now...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        logger.info(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        logger.info("Sorry, I did not understand.")
        return ""
    except sr.RequestError as e:
        logger.error(f"Could not request results from Google Speech Recognition service: {e}")
        return ""


# Main loop
while True:
    # Get user input
    user_input = get_voice_input()

    # Generate response from ChatGPT
    response = generate_response(user_input)
    logger.info(f"Response from ChatGPT: {response}")

    # Convert response to speech and speak it
    speak(response)

    # Update the chat history
    history += f"\nUser: {user_input}"
    history += f"\nChatbot: {response}"