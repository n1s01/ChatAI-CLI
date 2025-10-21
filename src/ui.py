"""
Модуль для UI компонентов.
"""

import os
import sys
import threading
import time
from colorama import Fore, Style


class Loader:
    """Анимация загрузки."""

    def __init__(self):
        """Инициализация."""
        self.running = False
        self.thread = None

    def animate(self):
        """Отображение анимации."""
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        idx = 0
        while self.running:
            sys.stdout.write(f"\r{frames[idx]} ")
            sys.stdout.flush()
            idx = (idx + 1) % len(frames)
            time.sleep(0.05)
        sys.stdout.write("\r" + " " * 5 + "\r")
        sys.stdout.flush()

    def start(self):
        """Запуск анимации."""
        self.running = True
        self.thread = threading.Thread(target=self.animate)
        self.thread.start()

    def stop(self):
        """Остановка анимации."""
        self.running = False
        if self.thread:
            self.thread.join()


def clear_screen():
    """Очистка экрана."""
    os.system("cls" if os.name == "nt" else "clear")


def display_main_menu():
    """Отображение главного меню."""
    clear_screen()
    print(f"\n{Fore.CYAN}=== ChatAI CLI ==={Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}1. New chat{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}2. Settings{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}3. Exit{Style.RESET_ALL}")
    return input(f"\n{Fore.LIGHTBLACK_EX}Select an option (1-3): {Style.RESET_ALL}")


def display_settings_menu():
    """Отображение меню настроек."""
    clear_screen()
    print(f"\n{Fore.YELLOW}Settings menu is currently empty.{Style.RESET_ALL}")
    input(f"{Fore.LIGHTBLACK_EX}Press Enter to return to main menu...{Style.RESET_ALL}")


def display_chat_start():
    """Отображение начала чата."""
    clear_screen()
    print(f"\n{Fore.GREEN}New chat started. For exit: type 'exit'{Style.RESET_ALL}")
    print(
        f"{Fore.LIGHTBLACK_EX}Available commands: status, export, model, help{Style.RESET_ALL}\n"
    )


def display_assistant_response(answer, tokens_used=None):
    """Отображение ответа ассистента."""
    if tokens_used is not None:
        print(
            f"\n{Fore.LIGHTBLACK_EX}Assistant:{Style.RESET_ALL} {answer} "
            f"\n{Fore.LIGHTBLACK_EX}⌬  Tokens used: {tokens_used}{Style.RESET_ALL}\n"
        )
    else:
        print(f"\n{Fore.LIGHTBLACK_EX}Assistant:{Style.RESET_ALL} {answer}\n")


def display_error(error_type, error_message):
    """Отображение ошибки."""
    if error_type == "api":
        print(f"API Error: {error_message}\n")
    elif error_type == "connection":
        print(f"Connection error: {error_message}\n")
    elif error_type == "cancelled":
        print("\nOperation cancelled by user.\n")
    elif error_type == "processing":
        print(f"Data processing error: {error_message}\n")


def display_goodbye():
    """Отображение прощального сообщения."""
    print(f"{Fore.GREEN}Goodbye!{Style.RESET_ALL}")


def display_invalid_option():
    """Отображение сообщения о неверной опции."""
    print(f"{Fore.RED}Invalid option. Please try again.{Style.RESET_ALL}")
    time.sleep(1)


def get_user_input():
    """Получение ввода пользователя."""
    return input(f"{Fore.LIGHTBLACK_EX}You:{Style.RESET_ALL} ")


def display_status(today_stats, all_time_stats):
    """Отображение статистики использования."""
    clear_screen()
    print(f"\n{Fore.CYAN}=== Usage Statistics ==={Style.RESET_ALL}\n")

    print(f"{Fore.YELLOW}Today ({today_stats['date']}):{Style.RESET_ALL}")
    print(
        f"  Requests: {today_stats['requests']} | ↑⌬: {today_stats['input_tokens']} | ↓⌬: {today_stats['output_tokens']} | Σ⌬: {today_stats['total_tokens']}"
    )

    if today_stats["models"]:
        print(f"\n{Fore.LIGHTBLACK_EX}By models:{Style.RESET_ALL}")
        for model_id, model_stats in today_stats["models"].items():
            print(
                f"  {model_id}: {model_stats['requests']} req | ↑{model_stats['input_tokens']} | ↓{model_stats['output_tokens']}"
            )

    print(f"\n{Fore.YELLOW}All time:{Style.RESET_ALL}")
    print(
        f"  Requests: {all_time_stats['requests']} | ↑⌬: {all_time_stats['input_tokens']} | ↓⌬: {all_time_stats['output_tokens']} | Σ⌬: {all_time_stats['total_tokens']}"
    )

    if all_time_stats["models"]:
        print(f"\n{Fore.LIGHTBLACK_EX}By models:{Style.RESET_ALL}")
        for model_id, model_stats in all_time_stats["models"].items():
            print(
                f"  {model_id}: {model_stats['requests']} req | ↑{model_stats['input_tokens']} | ↓{model_stats['output_tokens']}"
            )

    input(f"\n{Fore.LIGHTBLACK_EX}Press Enter to continue...{Style.RESET_ALL}")


def display_models(models, current_model):
    """Отображение списка моделей."""
    clear_screen()
    print(f"\n{Fore.CYAN}=== Available Models ==={Style.RESET_ALL}\n")

    for i, model in enumerate(models, 1):
        model_id = model.get("id", "")
        model_name = model.get("name", "")

        if current_model and model_id == current_model.get("id"):
            print(f"{Fore.GREEN}{i}. {model_name} [CURRENT]{Style.RESET_ALL}")
        else:
            print(f"{Fore.LIGHTBLACK_EX}{i}. {model_name}{Style.RESET_ALL}")

    return input(
        f"\n{Fore.LIGHTBLACK_EX}Select model (1-{len(models)}) or '0' to cancel: {Style.RESET_ALL}"
    )


def display_help():
    """Отображение справки по командам."""
    clear_screen()
    print(f"\n{Fore.CYAN}=== Command Help ==={Style.RESET_ALL}\n")

    commands = [
        {
            "command": "exit",
            "description": "End the current chat and return to main menu",
        },
        {
            "command": "status",
            "description": "Show detailed token usage and request statistics",
        },
        {
            "command": "export [json|txt]",
            "description": "Export current chat to JSON or TXT file",
        },
        {
            "command": "model",
            "description": "Show available models and select current model",
        },
        {"command": "help", "description": "Show this help"},
    ]

    for cmd in commands:
        print(
            f"{Fore.YELLOW}{cmd['command']:<20}{Style.RESET_ALL} - {cmd['description']}"
        )

    input(f"\n{Fore.LIGHTBLACK_EX}Press Enter to continue...{Style.RESET_ALL}")


def display_export_success(file_path):
    """Отображение сообщения об успешном экспорте."""
    print(f"\n{Fore.GREEN}Чат успешно экспортирован в:{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}{file_path}{Style.RESET_ALL}\n")


def display_export_error(error_message):
    """Отображение ошибки экспорта."""
    print(f"\n{Fore.RED}Ошибка экспорта:{Style.RESET_ALL}")
    print(f"{error_message}\n")
