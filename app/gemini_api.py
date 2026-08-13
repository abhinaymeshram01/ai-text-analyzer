import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

def get_api_key():
    """
    Get the Gemini API key.

    Priority:
    1. Streamlit secrets
    2. Environment variable / .env
    """
    try:

        api_key = st.secrets.get(
            "GEMINI_API_KEY"
        )

        if api_key:

            return api_key

    except Exception:

        pass

    api_key = os.getenv(
        "GEMINI_API_KEY"
    )

    if api_key:

        return api_key

    raise ValueError(
        "GEMINI_API_KEY is not configured. "
        "For local development, add it to your .env file. "
        "For Streamlit Cloud, add GEMINI_API_KEY "
        "to the app's Secrets settings."
    )

def get_client():

    api_key = get_api_key()

    return genai.Client(
        api_key=api_key
    )

def generate_response(prompt):
    """
    Send a prompt to Gemini and return the generated response.
    """

    client = get_client()

    response = client.models.generate_content(

        model="models/gemini-3.5-flash-lite",

        contents=prompt,

        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        ),
    )

    if not response.text:

        raise ValueError(
            "Gemini returned an empty response."
        )

    return response.text