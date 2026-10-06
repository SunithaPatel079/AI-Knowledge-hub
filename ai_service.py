import streamlit as st
from google import genai


API_KEY = st.secrets["GEMINI_API_KEY"]

client = genai.Client(
    api_key=API_KEY
)


def ask_ai(question, knowledge):

    prompt = f"""
You are an AI assistant for a company.

Use the following company knowledge
to answer the question.

COMPANY KNOWLEDGE:

{knowledge}

QUESTION:

{question}

Give a clear and simple answer.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text