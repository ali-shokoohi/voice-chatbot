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

# Set model name
chat_model = os.getenv("CHATGPT_MODEL") 
if chat_model == "":
    chat_model = "gpt-3.5-turbo"

# Set input type
enable_voice = True

if os.getenv("CHATGPT_VOICE") == "off":
    enable_voice = False


# Jailbreak mode
jailbreak = False
jailbreak_text = ""

if os.getenv("CHATGPT_JAILBREAK") == "on":
    jailbreak = True

# Read jailbreak text from the ./jailbreak.txt file
if jailbreak:
    with open('./jailbreak.txt', 'r') as file:
        # Read the contents of the file
        jailbreak_text = file.read()
        file.close()

# Define a function to generate a response from ChatGPT


def generate_response(message_history: list) -> str:
    response = openai.ChatCompletion.create(
        model=chat_model,
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


# Define a function to get text input from the user
def get_text_input() -> str:
    logger.info("Type your message")
    text =  input("=> ")
    logger.info(f"You type: {text}")
    return text

# Start jailbreak
if jailbreak and jailbreak_text != "":
    logger.info(f"Jailbreaking...")
    message_history.append({"role": "user", "content": jailbreak_text})
    response = generate_response(message_history)
    message_history.append({"role": "assistant", "content": response})
    logger.info(f"Jailbreaked!")


# Main loop
while True:
    # Get user input
    user_input = str()
    if enable_voice:
        user_input = get_voice_input()
        if user_input == "" or user_input.lower() == "disable voice" or user_input.lower() == "voice off":
            enable_voice = False
            continue
    else:
        user_input = get_text_input()
        if user_input == "" or user_input.lower() == "enable voice" or user_input.lower() == "voice on":
            enable_voice = True
            continue

    # Generate response from ChatGPT
    message_history.append({"role": "user", "content": user_input})
    response = generate_response(message_history)
    logger.info(f"Response from ChatGPT: {response}")
    message_history.append({"role": "assistant", "content": response})

    # Convert response to speech and speak it
    speak(response)
