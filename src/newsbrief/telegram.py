import json
import os
import ssl
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import truststore
from dotenv import load_dotenv

load_dotenv()

def api_request(method: str, payload: dict | None = None) -> dict:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is missing from .env.")

    request = Request(
        f"https://api.telegram.org/bot{token}/{method}",
        data=json.dumps(payload or {}).encode("utf-8"),
        headers={"Content-Type":"application/json"},   
    )

    context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

    try:
        with urlopen(request, timeout=15, context=context) as response:
            result = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        raise RuntimeError(f"Telegram returned HTTP {error.code}.") from None
    except URLError:
        raise RuntimeError(
            "Could not reach Telegram; check your network and certificate settings."
        ) from None
    if not result.get("ok"):
        raise RuntimeError(f"Telegram API error: {result.get('description', 'Unknown error')}")

    return result

def get_bot_info()->dict:
    return api_request("getMe")["result"]

def get_chat_ids()->list[int]:
     updates = api_request("getUpdates")["result"]
     
     return sorted(
        {
            update["message"]["chat"]["id"]
            for update in updates
            if "message" in update and "chat" in update["message"]
        }
    )

def send_message(text:str)->dict:
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not chat_id:
        raise RuntimeError("TELEGRAM_CHAT_ID is missing from .env.")

    if not text.strip():
        raise ValueError("Message text cannot be empty.")

    if len(text)>4096:
        raise ValueError("Telegram messages must be no longer than 4096 characters.")

    return api_request(
        "sendMessage",
        {"chat_id": chat_id, "text": text},
    )