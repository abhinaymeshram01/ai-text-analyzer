import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    raise ValueError('GEMINI_API_KEY is not set in the .env file')

client = genai.Client(
    api_key = api_key
)

def generate_response(prompt):
    response = client.models.generate_content(
    model='models/gemini-3.5-flash-lite',
    contents=prompt,
    config=types.GenerateContentConfig(
        response_mime_type='application/json'
    )
    )

    return response.text