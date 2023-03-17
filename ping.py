import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")


response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": "You are a chatbot"},
            {"role": "user", "content": "ping"},
        ]
)

result = ''
for choice in response.choices:
    result += choice.message.content

print(result)
