"""
Модуль для работы с базой данных SQLite.
"""

import os
import sqlite3
from datetime import date


DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "usage_stats.db"
)


def init_database():
    """Инициализация базы данных."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS usage_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        model_id TEXT NOT NULL,
        requests INTEGER DEFAULT 0,
        input_tokens INTEGER DEFAULT 0,
        output_tokens INTEGER DEFAULT 0,
        UNIQUE(date, model_id)
    )
    """
    )

    # Создаем таблицу для хранения настроек
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        api_key TEXT NOT NULL,
        endpoint TEXT NOT NULL,
        model TEXT NOT NULL
    )
    """
    )

    conn.commit()
    conn.close()


def update_usage(input_tokens, output_tokens, model_id):
    """Обновление статистики использования."""
    today = date.today().isoformat()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT requests, input_tokens, output_tokens FROM usage_stats "
        "WHERE date = ? AND model_id = ?",
        (today, model_id),
    )
    result = cursor.fetchone()

    if result:
        requests, input_tok, output_tok = result
        cursor.execute(
            """
            UPDATE usage_stats 
            SET requests = ?, input_tokens = ?, output_tokens = ?
            WHERE date = ? AND model_id = ?
            """,
            (
                requests + 1,
                input_tok + input_tokens,
                output_tok + output_tokens,
                today,
                model_id,
            ),
        )
    else:
        cursor.execute(
            """
            INSERT INTO usage_stats (date, model_id, requests, input_tokens, output_tokens)
            VALUES (?, ?, ?, ?, ?)
            """,
            (today, model_id, 1, input_tokens, output_tokens),
        )

    conn.commit()
    conn.close()


def get_today_stats():
    """Получение статистики за сегодня."""
    today = date.today().isoformat()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 
            COALESCE(SUM(requests), 0) as total_requests,
            COALESCE(SUM(input_tokens), 0) as total_input_tokens,
            COALESCE(SUM(output_tokens), 0) as total_output_tokens
        FROM usage_stats
        WHERE date = ?
        """,
        (today,),
    )
    result = cursor.fetchone()
    total_requests, total_input_tokens, total_output_tokens = result

    cursor.execute(
        """
        SELECT model_id, requests, input_tokens, output_tokens
        FROM usage_stats
        WHERE date = ?
        """,
        (today,),
    )
    models_results = cursor.fetchall()

    models_stats = {}
    for model_id, requests, input_tokens, output_tokens in models_results:
        models_stats[model_id] = {
            "requests": requests,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
        }

    conn.close()

    return {
        "date": today,
        "requests": total_requests,
        "input_tokens": total_input_tokens,
        "output_tokens": total_output_tokens,
        "total_tokens": total_input_tokens + total_output_tokens,
        "models": models_stats,
    }


def get_all_time_stats():
    """Получение статистики за все время."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 
            COALESCE(SUM(requests), 0) as total_requests,
            COALESCE(SUM(input_tokens), 0) as total_input_tokens,
            COALESCE(SUM(output_tokens), 0) as total_output_tokens
        FROM usage_stats
        """
    )
    result = cursor.fetchone()
    total_requests, total_input_tokens, total_output_tokens = result

    cursor.execute(
        """
        SELECT model_id, 
               SUM(requests) as total_requests,
               SUM(input_tokens) as total_input_tokens,
               SUM(output_tokens) as total_output_tokens
        FROM usage_stats
        GROUP BY model_id
        """
    )
    models_results = cursor.fetchall()

    models_stats = {}
    for model_id, requests, input_tokens, output_tokens in models_results:
        models_stats[model_id] = {
            "requests": requests,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
        }

    conn.close()

    return {
        "requests": total_requests,
        "input_tokens": total_input_tokens,
        "output_tokens": total_output_tokens,
        "total_tokens": total_input_tokens + total_output_tokens,
        "models": models_stats,
    }


def get_settings():
    """Получение настроек из базы данных."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT api_key, endpoint, model FROM settings WHERE id = 1")
    result = cursor.fetchone()

    conn.close()

    if result:
        api_key, endpoint, model = result
        return {"api_key": api_key, "endpoint": endpoint, "model": model}

    # Если настроек нет, возвращаем значения по умолчанию
    return {
        "api_key": "",
        "endpoint": "https://api.intelligence.io.solutions/api/v1/",
        "model": "meta-llama/Llama-3.2-90B-Vision-Instruct",
    }


def update_settings(api_key, endpoint, model):
    """Обновление настроек в базе данных."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Проверяем, существуют ли уже настройки
    cursor.execute("SELECT COUNT(*) FROM settings WHERE id = 1")
    count = cursor.fetchone()[0]

    if count > 0:
        # Обновляем существующие настройки
        cursor.execute(
            "UPDATE settings SET api_key = ?, endpoint = ?, model = ? WHERE id = 1",
            (api_key, endpoint, model),
        )
    else:
        # Вставляем новые настройки
        cursor.execute(
            "INSERT INTO settings (id, api_key, endpoint, model) VALUES (1, ?, ?, ?)",
            (api_key, endpoint, model),
        )

    conn.commit()
    conn.close()

    return True


def get_api_key():
    """Получение API ключа из базы данных."""
    settings = get_settings()
    return settings.get("api_key", "")


def get_endpoint():
    """Получение эндпоинта из базы данных."""
    settings = get_settings()
    return settings.get("endpoint", "https://api.intelligence.io.solutions/api/v1/")


def get_model():
    """Получение модели из базы данных."""
    settings = get_settings()
    return settings.get("model", "meta-llama/Llama-3.2-90B-Vision-Instruct")


def migrate_settings_from_json():
    """Миграция настроек из JSON файла в базу данных."""
    import json
    from dotenv import load_dotenv

    # Путь к файлу настроек
    settings_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "config", "settings.json"
    )

    # Путь к файлу .env
    env_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "config", ".env"
    )

    # Значения по умолчанию
    api_key = ""
    endpoint = "https://api.intelligence.io.solutions/api/v1/"
    model = "meta-llama/Llama-3.2-90B-Vision-Instruct"

    # Пытаемся загрузить API ключ из .env
    if os.path.exists(env_path):
        load_dotenv(env_path)
        api_key = os.getenv("IOINTELLIGENCE_API_KEY", "")

    # Пытаемся загрузить настройки из JSON
    if os.path.exists(settings_path):
        try:
            with open(settings_path, "r", encoding="utf-8") as settings_file:
                json_settings = json.load(settings_file)
                model = json_settings.get("model", model)
        except (json.JSONDecodeError, IOError):
            pass

    # Обновляем настройки в базе данных
    update_settings(api_key, endpoint, model)

    return True
