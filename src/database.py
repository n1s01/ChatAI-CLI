"""
Модуль для работы с базой данных SQLite.
"""

import os
import sqlite3
from datetime import date


DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "config", "usage_stats.db"
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
