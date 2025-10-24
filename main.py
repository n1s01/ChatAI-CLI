"""
ChatAI CLI - Интерфейс командной строки для взаимодействия с AI моделями.
Внимание!!! Все комментарии в коде даны на основе Pylint расширения для VSCode.
"""

import sys
import time
import os
import openai
from colorama import Fore, Style

from src.api_client import send_message
from src.ui import (
    Loader,
    display_main_menu,
    display_settings_menu,
    display_chat_start,
    display_assistant_response,
    display_error,
    display_goodbye,
    display_invalid_option,
    get_user_input,
    display_status,
    display_help,
    display_export_success,
    display_export_error,
)
from src.stats import get_today_stats, get_all_time_stats
from src.models import get_current_model, change_model
from src.export import export_to_json, export_to_txt
from config.config import get_system_message, get_model_id


def handle_command(user_input, messages):
    """Обработка специальных команд."""
    parts = user_input.strip().split()

    # Проверяем, что ввод не пустой
    if not parts:
        return False

    command = parts[0].lower()

    available_commands = {
        "exit": "end the chat",
        "status": "show token statistics",
        "export": "export the chat",
        "model": "change the model",
        "help": "show help",
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
            current_model = get_current_model()

            if len(parts) > 1:
                # Если указан ID модели напрямую
                model_id = parts[1]
                _, message = change_model(model_id)
                print(message)
                input("Press Enter to continue...")
            else:
<<<<<<< HEAD
=======
                # Показываем текущую модель и предлагаем ввести новую вручную
>>>>>>> 3af0b03aa2854b0320bf660b95f2541853d1b42a
                os.system("cls" if os.name == "nt" else "clear")
                print(f"\n{Fore.CYAN}=== Model Selection ==={Style.RESET_ALL}\n")

                if current_model:
                    print(
                        f"{Fore.YELLOW}Current model:{Style.RESET_ALL} {current_model.get('name', current_model.get('id', 'Unknown'))}"
                    )
                else:
                    print(f"{Fore.YELLOW}Current model:{Style.RESET_ALL} Not set")

                print(
                    f"\n{Fore.LIGHTBLACK_EX}You can enter a model ID manually.{Style.RESET_ALL}"
                )
                print(
                    f"{Fore.LIGHTBLACK_EX}Available models can be found on the provider's website.{Style.RESET_ALL}"
                )

                print(
                    f"\n{Fore.LIGHTBLACK_EX}Enter model ID or '0' to cancel:{Style.RESET_ALL}"
                )
                model_input = input().strip()

                if model_input == "0":
                    return True

                if model_input:
<<<<<<< HEAD
                    _, message = change_model(model_input)
                    print(message)
=======
                    # Проверяем, является ли ввод числом (выбор из списка)
                    try:
                        model_index = int(model_input) - 1
                        if 0 <= model_index < len(models):
                            selected_model = models[model_index]
                            _, message = change_model(selected_model["id"])
                            print(message)
                        else:
                            print("Invalid model selection")
                    except ValueError:
                        # Если ввод не число, считаем это ID модели
                        _, message = change_model(model_input)
                        print(message)
>>>>>>> 3af0b03aa2854b0320bf660b95f2541853d1b42a

                    input("Press Enter to continue...")

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
            print(
                f"{Fore.GREEN}New chat started. For exit: type 'exit'{Style.RESET_ALL}"
            )
            print(
                f"{Fore.LIGHTBLACK_EX}Available commands: status, export, model, "
                f"help{Style.RESET_ALL}\n"
            )

    while True:
        try:
            user_input = get_user_input()

            # Проверяем, что ввод не пустой
            if not user_input.strip():
                continue

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
            except (
                openai.APIError,
                openai.RateLimitError,
                openai.AuthenticationError,
            ) as e:
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
    from src.database import get_settings, update_settings

    while True:
        choice = display_settings_menu()

        if choice == "1":
            current_model = get_current_model()

            # Показываем текущую модель и предлагаем ввести новую вручную
            os.system("cls" if os.name == "nt" else "clear")
            print(f"\n{Fore.CYAN}=== Model Selection ==={Style.RESET_ALL}\n")

            if current_model:
                print(
                    f"{Fore.YELLOW}Current model:{Style.RESET_ALL} {current_model.get('name', current_model.get('id', 'Unknown'))}"
                )
            else:
                print(f"{Fore.YELLOW}Current model:{Style.RESET_ALL} Not set")

            print(
                f"\n{Fore.LIGHTBLACK_EX}You can enter a model ID manually.{Style.RESET_ALL}"
            )
            print(
                f"{Fore.LIGHTBLACK_EX}Available models can be found on provider's website.{Style.RESET_ALL}"
            )

            print(
                f"\n{Fore.LIGHTBLACK_EX}Enter model ID or '0' to cancel:{Style.RESET_ALL}"
            )
            model_input = input().strip()

            if model_input == "0":
                continue

            if model_input:
                _, message = change_model(model_input)
                print(message)

                input("Press Enter to continue...")
        elif choice == "2":
            # Изменение API ключа
            current_settings = get_settings()
            current_api_key = current_settings.get("api_key", "")

            os.system("cls" if os.name == "nt" else "clear")
            print(f"\n{Fore.CYAN}=== API Key Settings ==={Style.RESET_ALL}\n")

            if current_api_key:
                masked_key = (
                    current_api_key[:8] + "..." if len(current_api_key) > 8 else "..."
                )
                print(f"{Fore.YELLOW}Current API key:{Style.RESET_ALL} {masked_key}")
            else:
                print(f"{Fore.YELLOW}Current API key:{Style.RESET_ALL} Not set")

            print(
                f"\n{Fore.LIGHTBLACK_EX}Enter new API key or '0' to cancel:{Style.RESET_ALL}"
            )
            api_key_input = input().strip()

            if api_key_input == "0":
                continue

<<<<<<< HEAD
            if api_key_input:
                # Обновляем только API ключ, оставляя остальные настройки без изменений
                update_settings(
                    api_key_input,
                    current_settings.get(
                        "endpoint", "https://api.intelligence.io.solutions/api/v1/"
                    ),
                    current_settings.get(
                        "model", "meta-llama/Llama-3.2-90B-Vision-Instruct"
                    ),
                )
                print(f"{Fore.GREEN}API key updated successfully{Style.RESET_ALL}")
                input("Press Enter to continue...")
        elif choice == "3":
            # Изменение эндпоинта
            current_settings = get_settings()
            current_endpoint = current_settings.get("endpoint", "")

            os.system("cls" if os.name == "nt" else "clear")
            print(f"\n{Fore.CYAN}=== Endpoint Settings ==={Style.RESET_ALL}\n")

            if current_endpoint:
                print(
                    f"{Fore.YELLOW}Current endpoint:{Style.RESET_ALL} {current_endpoint}"
                )
            else:
                print(f"{Fore.YELLOW}Current endpoint:{Style.RESET_ALL} Not set")

            print(
                f"\n{Fore.LIGHTBLACK_EX}Enter new endpoint or '0' to cancel:{Style.RESET_ALL}"
            )
            print(
                f"{Fore.LIGHTBLACK_EX}Example: https://api.openai.com/v1/{Style.RESET_ALL}"
            )
            endpoint_input = input().strip()

            if endpoint_input == "0":
                continue

            if endpoint_input:
                # Обновляем только эндпоинт, оставляя остальные настройки без изменений
                update_settings(
                    current_settings.get("api_key", ""),
                    endpoint_input,
                    current_settings.get(
                        "model", "meta-llama/Llama-3.2-90B-Vision-Instruct"
                    ),
                )
                print(f"{Fore.GREEN}Endpoint updated successfully{Style.RESET_ALL}")
=======
            # Показываем текущую модель и предлагаем ввести новую вручную
            os.system("cls" if os.name == "nt" else "clear")
            print(f"\n{Fore.CYAN}=== Model Selection ==={Style.RESET_ALL}\n")

            if current_model:
                print(
                    f"{Fore.YELLOW}Current model:{Style.RESET_ALL} {current_model.get('name', current_model.get('id', 'Unknown'))}"
                )
            else:
                print(f"{Fore.YELLOW}Current model:{Style.RESET_ALL} Not set")

            print(
                f"\n{Fore.LIGHTBLACK_EX}You can enter a model ID manually.{Style.RESET_ALL}"
            )
            print(
                f"{Fore.LIGHTBLACK_EX}Available models can be found on the provider's website.{Style.RESET_ALL}"
            )

            print(
                f"\n{Fore.LIGHTBLACK_EX}Enter model ID or '0' to cancel:{Style.RESET_ALL}"
            )
            model_input = input().strip()

            if model_input == "0":
                continue

            if model_input:
                # Проверяем, является ли ввод числом (выбор из списка)
                try:
                    model_index = int(model_input) - 1
                    if 0 <= model_index < len(models):
                        selected_model = models[model_index]
                        _, message = change_model(selected_model["id"])
                        print(message)
                    else:
                        print("Invalid model selection")
                except ValueError:
                    # Если ввод не число, считаем это ID модели
                    _, message = change_model(model_input)
                    print(message)

>>>>>>> 3af0b03aa2854b0320bf660b95f2541853d1b42a
                input("Press Enter to continue...")
        elif choice == "0":
            break
        else:
            display_invalid_option()


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
    # Инициализируем базу данных
    from src.database import init_database, migrate_settings_from_json

    init_database()

    # Мигрируем настройки из JSON в базу данных
    migrate_settings_from_json()

    show_main_menu()
