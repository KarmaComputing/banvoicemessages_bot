from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route

import requests
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN", None)
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", None)
APP_DEBUG = os.getenv("APP_DEBUG", "0")

API_ENDPOINT = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/"


async def index(request):
    body = await request.json()
    print(body)

    message_id = body["message"]["message_id"]
    if "voice" in body["message"]:
        print("Must be a voice message. Lets's delte it!")
        reply = "We've banned voice messages. Deleting it now."
        # Warn the user
        requests.get(
            f"{API_ENDPOINT}sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={reply}"  # noqa: E501
        )
        # Delete their voice message
        requests.get(
            f"{API_ENDPOINT}deleteMessage?chat_id={TELEGRAM_CHAT_ID}&message_id={message_id}"  # noqa: E501
        )
    return PlainTextResponse("OK")


async def health(request):
    return PlainTextResponse("OK")


routes = [
    Route("/", index, methods=["GET", "POST"]),
    Route("/health", health),
]


if APP_DEBUG == "1" or APP_DEBUG.lower() == "true":
    debug = True
else:
    debug = False

app = Starlette(debug=debug, routes=routes)
