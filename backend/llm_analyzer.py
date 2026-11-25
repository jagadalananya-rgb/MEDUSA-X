import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API key from the .env file
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key) if api_key else None


def analyze_document(text):
    if client is None:
        return {
            "status": "ERROR",
            "message": "OpenAI API key not configured."
        }

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are a documentation review assistant. "
                        "Review only fictional sample documents. "
                        "Identify possible documentation inconsistencies. "
                        "Do not diagnose, recommend treatment, or make "
                        "clinical decisions. Return concise findings "
                        "with supporting text."
                    )
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )

        return {
            "status": "SUCCESS",
            "analysis": response.output_text
        }

    except Exception as error:
        return {
            "status": "ERROR",
            "message": str(error)
        }