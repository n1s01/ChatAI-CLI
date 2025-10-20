"""
ChatAI CLI - Интерфейс командной строки для взаимодействия с AI моделями.
Внимание!!! Все комментарии в коде даны на основе Pylint расширения для VSCode.
"""

import sys
import time
import openai
from colorama import Fore, Style

from src.api_client import send_message
from src.ui import (
    Loader, display_main_menu, display_settings_menu,
    display_chat_start, display_assistant_response, display_error,
    display_goodbye, display_invalid_option, get_user_input,
    display_status, display_models, display_help, display_export_success, display_export_error
)
from src.stats import get_today_stats, get_all_time_stats
from src.models import load_models, get_current_model, change_model
from src.export import export_to_json, export_to_txt
from config.config import get_system_message, get_model_id


def handle_command(user_input, messages):
    """Обработка специальных команд."""
    parts = user_input.strip().split()
    command = parts[0].lower()

    available_commands = {
        "exit": "end the chat",
        "status": "show token statistics",
        "export": "export the chat",
        "model": "change the model",
        "help": "show help"
    }

    if command in available_commands:
        if command == "exit":
            return False

        elif command == "status":
            today_stats = get_today_stats()
            all_time_stats = get_all_time_stats()
            display_status(today_stats, all_time_stats)
            return True

        elif command == "export":
            if len(parts) < 2:
                print("Usage: export [json|txt]")
                input("Press Enter to continue...")
                return True

            format_type = parts[1].lower()
            if format_type not in ["json", "txt"]:
                print("Format must be 'json' or 'txt'")
                input("Press Enter to continue...")
                return True

            try:
                if format_type == "json":
                    file_path = export_to_json(messages)
                else:
                    file_path = export_to_txt(messages)

                display_export_success(file_path)
                input("Press Enter to continue...")
            except (IOError, OSError, ValueError) as e:
                display_export_error(str(e))
                input("Press Enter to continue...")

            return True

        elif command == "model":
            models = load_models()
            current_model = get_current_model()

            if not models:
                print("Model list is empty or unavailable")
                input("Press Enter to continue...")
                return True

            choice = display_models(models, current_model)

            if choice == "0":
                return True

            try:
                model_index = int(choice) - 1
                if 0 <= model_index < len(models):
                    selected_model = models[model_index]
                    _, message = change_model(selected_model["id"])
                    print(message)
                    input("Press Enter to continue...")
                else:
                    print("Invalid model selection")
                    input("Press Enter to continue...")
            except ValueError:
                print("Invalid input format")
                input("Press Enter to continue...")

            return True

        elif command == "help":
            display_help()
            return True

    for cmd, description in available_commands.items():
        if cmd.startswith(command) or command.startswith(cmd):
            if len(command) >= 2:
                print(f"Did you mean '{cmd}'? With it you can {description}.")
                return True

        if len(command) >= 3 and abs(len(command) - len(cmd)) <= 2:
            common_chars = sum(1 for a, b in zip(command, cmd) if a == b)
            if common_chars >= len(command) - 1:
                print(f"Did you mean '{cmd}'? With it you can {description}.")
                return True

    return False


def start_new_chat():
    """Начало нового чата."""
    display_chat_start()
    messages = [get_system_message()]

    def show_chat_info_if_empty():
        """Показать информацию о чате, если в нем нет сообщений."""
        if len(messages) <= 1:
            print(f"{Fore.GREEN}New chat started. For exit: type 'exit'{Style.RESET_ALL}")
            print(
                f"{Fore.LIGHTBLACK_EX}Available commands: status, export, model, help{Style.RESET_ALL}\n"
            )

    while True:
        try:
            user_input = get_user_input()
            if user_input.lower() == "exit":
                break

            if handle_command(user_input, messages):
                show_chat_info_if_empty()
                continue

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
