"""
ChatAI CLI - Интерфейс командной строки для взаимодействия с AI моделями.
Внимание!!! Все комментарии в коде даны на основе Pylint расширения для VSCode.
"""

import sys
import time
import openai

from src.api_client import send_message
from src.ui import (
    Loader, display_main_menu, display_settings_menu,
    display_chat_start, display_assistant_response, display_error,
    display_goodbye, display_invalid_option, get_user_input
)
from config.config import get_system_message, get_model_id


def start_new_chat():
    """Начало нового чата."""
    display_chat_start()
    messages = [get_system_message()]

    while True:
        try:
            user_input = get_user_input()
            if user_input.lower() == "exit":
                break
            messages.append({"role": "user", "content": user_input})
            loader = Loader()
            try:
                loader.start()
                answer, tokens_used = send_message(messages, get_model_id())
                loader.stop()
                messages.append({"role": "assistant", "content": answer})
                display_assistant_response(answer, tokens_used)
            except (openai.APIError, openai.RateLimitError, openai.AuthenticationError) as e:
                loader.stop()
                display_error("api", str(e))
                messages.pop()
            except (ConnectionError, TimeoutError) as e:
                loader.stop()
                display_error("connection", str(e))
                messages.pop()
            except (AttributeError, ValueError, IndexError) as e:
                loader.stop()
                display_error("processing", str(e))
                messages.pop()
        except KeyboardInterrupt:
            print("\nOperation cancelled by user. Returning to main menu...")
            break


def settings():
    """Меню настроек."""
    display_settings_menu()


def show_main_menu():
    """Главное меню."""
    while True:
        try:
            choice = display_main_menu()

            if choice == "1":
                start_new_chat()
            elif choice == "2":
                settings()
            elif choice == "3":
                display_goodbye()
                sys.exit(0)
            else:
                display_invalid_option()
        except KeyboardInterrupt:
            print("\nOperation cancelled by user. Press Ctrl+C again to exit.")
            try:
                time.sleep(5)
            except KeyboardInterrupt:
                print("Exiting...")
                sys.exit(0)


if __name__ == "__main__":
    show_main_menu()
