import os
import json
import openai
import threading
import time
import sys
import colorama
from colorama import Fore, Style
from dotenv import load_dotenv

SETTINGS_PATH = os.path.join(os.path.dirname(__file__), "settings.json")
with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
    _settings = json.load(f)
SYSTEM_MESSAGE = _settings.get("system_message")
MODEL_ID = _settings.get("model")

load_dotenv()
colorama.init(autoreset=True)

api_key = os.getenv("IOINTELLIGENCE_API_KEY")

client = openai.OpenAI(
    api_key=api_key,
    base_url="https://api.intelligence.io.solutions/api/v1/"
)

class Loader:
    def __init__(self):
        self.running = False
        self.thread = None
    
    def animate(self):
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
        self.running = True
        self.thread = threading.Thread(target=self.animate)
        self.thread.start()
    
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

messages = [SYSTEM_MESSAGE]

print("CLI started. For exit: exit")
while True:
    user_input = input(f"{Fore.LIGHTBLACK_EX}You:{Style.RESET_ALL} ")
    if user_input.lower() == "exit":
        break
    messages.append({"role": "user", "content": user_input})
    loader = Loader()
    try:
        loader.start()
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=messages
        )
        loader.stop()
        answer = response.choices[0].message.content
        usage = getattr(response, "usage", None)
        tokens_used = None
        if usage:
            tokens_used = getattr(usage, "completion_tokens", None)
            if tokens_used is None:
                tokens_used = getattr(usage, "total_tokens", None)
        messages.append({"role": "assistant", "content": answer})
        if tokens_used is not None:
            print(
                f"\n{Fore.LIGHTBLACK_EX}Assistant:{Style.RESET_ALL} {answer} "
                f"\n{Fore.LIGHTBLACK_EX}⌬  Tokens used: {tokens_used}{Style.RESET_ALL}\n"
            )
        else:
            print(f"\n{Fore.LIGHTBLACK_EX}Assistant:{Style.RESET_ALL} {answer}\n")
    except Exception as e:
        loader.stop()
        print("Error:", e, "\n")
        messages.pop()