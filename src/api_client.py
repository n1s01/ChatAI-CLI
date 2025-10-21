"""
Модуль для работы с API.
"""

import os
import openai
from dotenv import load_dotenv
from .stats import update_usage

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
    input_tokens = 0
    output_tokens = 0

    if usage:
        tokens_used = getattr(usage, "completion_tokens", None)
        if tokens_used is None:
            tokens_used = getattr(usage, "total_tokens", None)

        input_tokens = getattr(usage, "prompt_tokens", 0)
        output_tokens = getattr(usage, "completion_tokens", 0)

        update_usage(input_tokens, output_tokens, model_id)

    return answer, tokens_used
