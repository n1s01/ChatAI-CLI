"""
Модуль для отслеживания статистики использования токенов и запросов.
"""

from .database import init_database, update_usage, get_today_stats, get_all_time_stats

init_database()

__all__ = ['update_usage', 'get_today_stats', 'get_all_time_stats']
