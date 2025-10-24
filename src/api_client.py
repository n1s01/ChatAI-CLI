"""
Модуль для работы с API.
"""

import openai
from .stats import update_usage
from .database import get_api_key, get_endpoint


def get_client():
    """Получение клиента OpenAI с текущими настройками."""
    api_key = get_api_key()
    endpoint = get_endpoint()

    return openai.OpenAI(api_key=api_key, base_url=endpoint)


def send_message(messages, model_id):
    """Отправка сообщения и получение ответа."""
    client = get_client()
    response = client.chat.completions.create(model=model_id, messages=messages)

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
