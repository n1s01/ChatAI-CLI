"""
Модуль для работы с моделями AI.
"""

import os
import json
from config.config import update_settings, _settings, get_model_id


MODELS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "models.json")


def load_models():
    """Загрузка списка моделей из файла."""
    try:
        with open(MODELS_PATH, "r", encoding="utf-8") as models_file:
            models_data = json.load(models_file)
            return models_data.get("models", [])
    except (json.JSONDecodeError, IOError):
        return []


def get_aggregator():
    """Получение имени агрегатора."""
    try:
        with open(MODELS_PATH, "r", encoding="utf-8") as models_file:
            models_data = json.load(models_file)
            return models_data.get("aggregator", "unknown")
    except (json.JSONDecodeError, IOError):
        return "unknown"


def get_model_by_id(model_id):
    """Получение модели по ID."""
    models = load_models()
    for model in models:
        if model.get("id") == model_id:
            return model
    return None


def change_model(model_id):
    """Изменение текущей модели."""
    model = get_model_by_id(model_id)
    if not model:
        return False, "Модель с указанным ID не найдена"

    try:
        new_settings = _settings.copy()
        new_settings["model"] = model_id

        update_settings(new_settings)
        return True, f"Модель успешно изменена на: {model.get('name', model_id)}"
    except (IOError, OSError, KeyError) as e:
        return False, f"Ошибка при изменении модели: {str(e)}"


def get_current_model():
    """Получение текущей модели."""
    model_id = get_model_id()
    return get_model_by_id(model_id)
