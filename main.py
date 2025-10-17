import os
import json
import openai
from dotenv import load_dotenv

SETTINGS_PATH = os.path.join(os.path.dirname(__file__), "settings.json")
with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
    _settings = json.load(f)
SYSTEM_MESSAGE = _settings.get("system_message", {"role": "system", "content": "You are a helpful assistant."})
MODEL_ID = _settings.get("model", "openai/gpt-oss-20b")

load_dotenv()

api_key = os.getenv("IOINTELLIGENCE_API_KEY")

client = openai.OpenAI(
    api_key=api_key,
    base_url="https://api.intelligence.io.solutions/api/v1/"
)

messages = [SYSTEM_MESSAGE]

print("CLI запущен. Для выхода: exit")
while True:
    user_input = input("Вы: ")
    if user_input.lower() == "exit":
        break
    messages.append({"role": "user", "content": user_input})
    try:
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=messages
        )
        answer = response.choices[0].message.content
        messages.append({"role": "assistant", "content": answer})
        print("AI:", answer, "\n")
    except Exception as e:
        print("Error:", e, "\n")
        messages.pop()