"""
Модуль для работы с API.
"""

import os
import openai
from dotenv import load_dotenv

# Load environment variables from config/.env
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', '.env'))

api_key = os.getenv("IOINTELLIGENCE_API_KEY")

client = openai.OpenAI(
    api_key=api_key,
    base_url="https://api.intelligence.io.solutions/api/v1/"
)

def send_message(messages, model_id):
    """Отправка сообщения и получение ответа."""
    response = client.chat.completions.create(
        model=model_id,
        messages=messages
    )

    answer = response.choices[0].message.content
    usage = getattr(response, "usage", None)
    tokens_used = None

    if usage:
        tokens_used = getattr(usage, "completion_tokens", None)
        if tokens_used is None:
            tokens_used = getattr(usage, "total_tokens", None)

    return answer, tokens_used
