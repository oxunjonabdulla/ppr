import requests

from root.settings.base import env


def send_telegram_message(message):
    bot_token = env("BOT_TOKEN")
    chat_id = env("CHAT_ID")

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    try:
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Telegram error: {e}")
        return False
