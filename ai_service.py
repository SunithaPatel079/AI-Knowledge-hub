import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)


def ask_ai(question, knowledge_text):
    prompt = f"""
You are an AI Knowledge Transfer Assistant for a company.

Answer the employee's question using the company knowledge
provided below.

If the answer is not available in the company knowledge,
clearly say that the information is not available.

Use simple and professional language.

Company Knowledge:
{knowledge_text}

Employee Question:
{question}
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return response.text

    except Exception as error:
        print("Gemini Error:", error)

        return (
            "Sorry, the AI service is temporarily unavailable. "
            "Please try again in a few moments."
        )