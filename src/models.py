"""
Модуль для работы с моделями AI.
"""

import os
import json
from config.config import update_settings, get_model_id
from colorama import Fore, Style


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
    
    try:
        # Читаем текущие настройки из файла
        settings_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "config", "settings.json"
        )
        with open(settings_path, "r", encoding="utf-8") as settings_file:
            current_settings = json.load(settings_file)

        # Обновляем только модель
        current_settings["model"] = model_id

        # Сохраняем обновленные настройки
        update_settings(current_settings)
        
        # Формируем сообщение об успешном изменении
        if model:
            model_name = model.get('name', model_id)
            return True, f"Модель успешно изменена на: {model_name}"
        else:
            # Если модель не найдена в списке, предупреждаем пользователя
            return True, f"Модель изменена на: {model_id}\n{Fore.LIGHTBLACK_EX}Внимание: Эта модель отсутствует в списке поддерживаемых. Убедитесь, что она доступна на сайте провайдера.{Style.RESET_ALL}"
    except (IOError, OSError, KeyError, json.JSONDecodeError) as e:
        return False, f"Ошибка при изменении модели: {str(e)}"


def get_current_model():
    """Получение текущей модели."""
    model_id = get_model_id()
    model = get_model_by_id(model_id)
    
    # Если модель найдена в списке, возвращаем ее
    if model:
        return model
    
    # Если модель не найдена в списке, но ID установлен, возвращаем базовую информацию
    if model_id:
        return {"id": model_id, "name": model_id}
    
    # Если модель не установлена, возвращаем None
    return None
