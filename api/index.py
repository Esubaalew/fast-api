import os
from typing import Optional
import requests
from fastapi import FastAPI, Request
from pydantic import BaseModel

TOKEN = os.environ.get("TOKEN")
TELEGRAM_API_BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

app = FastAPI()

class TelegramWebhook(BaseModel):
    update_id: int
    message: Optional[dict]
    edited_message: Optional[dict]
    channel_post: Optional[dict]
    edited_channel_post: Optional[dict]
    inline_query: Optional[dict]
    chosen_inline_result: Optional[dict]
    callback_query: Optional[dict]
    shipping_query: Optional[dict]
    pre_checkout_query: Optional[dict]
    poll: Optional[dict]
    poll_answer: Optional[dict]

def start(chat_id):
    # Send a message using the plain Telegram Bot API
    endpoint = f"{TELEGRAM_API_BASE_URL}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": "I'm a bot, please talk to me!"
    }
    requests.post(endpoint, json=params)

@app.post("/webhook")
def webhook(webhook_data: TelegramWebhook):
    if webhook_data.message and webhook_data.message.text == '/start':
        # Handle the '/start' command
        start(webhook_data.message.chat.id)

    return {"message": "ok"}

@app.get("/")
def index():
    return {"message": "Hello World"}

