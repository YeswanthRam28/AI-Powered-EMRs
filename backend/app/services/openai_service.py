import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_summary(text: str) -> str:
    """
    Summarize or analyze the given text using OpenAI GPT.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # You can change to gpt-4 or gpt-3.5-turbo
            messages=[
                {"role": "system", "content": "You are a helpful EMR assistant."},
                {"role": "user", "content": text}
            ],
            temperature=0.5,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating summary: {str(e)}"
