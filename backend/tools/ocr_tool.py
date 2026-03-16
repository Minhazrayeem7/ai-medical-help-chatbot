# IMPORTS: Load Google GenAI client and environment variables
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

from google.genai import types

# OCR FUNCTION: Extract text and descriptions from images using the Gemini model
def extract_text(image_bytes, mime_type="image/jpeg"):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                "Extract any text from this image if present, and describe the image in detail.",
                types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
            ]
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"