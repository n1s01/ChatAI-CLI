"""
Модуль для настроек.
"""

import os
import json
import colorama

colorama.init(autoreset=True)

SETTINGS_PATH = os.path.join(os.path.dirname(__file__), "settings.json")
with open(SETTINGS_PATH, "r", encoding="utf-8") as config_file:
    _settings = json.load(config_file)

SYSTEM_MESSAGE = _settings.get("system_message")
MODEL_ID = _settings.get("model")


def get_system_message():
    """Получение системного сообщения."""
    return SYSTEM_MESSAGE


def get_model_id():
    """Получение ID модели."""
    return MODEL_ID


def update_settings(new_settings):
    """Обновление настроек."""
    with open(SETTINGS_PATH, "w", encoding="utf-8") as settings_file:
        json.dump(new_settings, settings_file, indent=2, ensure_ascii=False)

    # Возвращаем обновленные значения вместо изменения глобальных переменных
    return (
        new_settings.get("system_message"),
        new_settings.get("model")
    )
