from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

models = [
    # Gemini 3 series
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",

    # Gemini 3 Pro / reasoning
    "gemini-3.1-pro-preview",
    "gemini-3-flash-preview",

    # Gemini 2.5 series
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-2.5-flash-lite",

    # Older model (may be unavailable)
    "gemini-1.5-flash",
]

for name in models:
    try:
        response = client.models.generate_content(
            model=name,
            contents="Reply with OK"
        )

        print(name, "WORKS:", response.text)

    except Exception as e:
        print(name, "FAILED:", e)