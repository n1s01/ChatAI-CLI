"""
Модуль для работы с моделями AI.
"""

from src.database import get_model, update_settings


def change_model(model_id):
    """Изменение текущей модели."""
    try:
        # Получаем текущие настройки из базы данных
        from src.database import get_settings

        current_settings = get_settings()

        # Обновляем только модель, оставляя остальные настройки без изменений
        update_settings(
            current_settings.get("api_key", ""),
            current_settings.get(
                "endpoint", "https://api.intelligence.io.solutions/api/v1/"
            ),
            model_id,
        )

        # Формируем сообщение об успешном изменении
        return True, f"Модель успешно изменена на: {model_id}"
    except (IOError, OSError, KeyError) as e:
        return False, f"Ошибка при изменении модели: {str(e)}"


def get_current_model():
    """Получение текущей модели."""
    model_id = get_model()

    # Если модель установлена, возвращаем базовую информацию
    if model_id:
        return {"id": model_id, "name": model_id}

    # Если модель не установлена, возвращаем None
    return None
