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
message_history = [{"role": "system", "content": "You are a chatbot"}]

# Define a function to generate a response from ChatGPT


def generate_response(message_history: list) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_history
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
        logger.error(
            f"Could not request results from Google Speech Recognition service: {e}")
        return ""


# Main loop
while True:
    # Get user input
    user_input = get_voice_input()

    # Generate response from ChatGPT
    message_history.append({"role": "user", "content": user_input})
    response = generate_response(message_history)
    logger.info(f"Response from ChatGPT: {response}")
    message_history.append({"role": "assistant", "content": response})

    # Convert response to speech and speak it
    speak(response)
