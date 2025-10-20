"""
Модуль для экспорта чатов в различные форматы.
"""

import os
import json
from datetime import datetime


def export_to_json(messages, filename=None):
    """Экспорт чата в формат JSON."""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_export_{timestamp}.json"

    chat_data = {
        "export_date": datetime.now().isoformat(),
        "messages": messages,
        "message_count": len(messages)
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(chat_data, f, indent=2, ensure_ascii=False)

    return os.path.abspath(filename)


def export_to_txt(messages, filename=None):
    """Экспорт чата в формат TXT."""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_export_{timestamp}.txt"

    chat_text = f"Экспорт чата от {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n"
    chat_text += "=" * 50 + "\n\n"
    for message in messages:
        role = message.get("role", "unknown")
        content = message.get("content", "")

        if role == "system":
            chat_text += f"[СИСТЕМА]: {content}\n\n"
        elif role == "user":
            chat_text += f"[ПОЛЬЗОВАТЕЛЬ]: {content}\n\n"
        elif role == "assistant":
            chat_text += f"[АССИСТЕНТ]: {content}\n\n"

    chat_text += "=" * 50 + "\n"
    chat_text += f"Всего сообщений: {len(messages)}\n"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(chat_text)

    return os.path.abspath(filename)
