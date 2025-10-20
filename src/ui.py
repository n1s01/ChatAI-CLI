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
    os.system('cls' if os.name == 'nt' else 'clear')


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
    print(f"\n{Fore.GREEN}New chat started. For exit: type 'exit'{Style.RESET_ALL}\n")


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
