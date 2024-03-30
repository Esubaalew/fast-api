import os
from typing import Optional
import requests
from fastapi import FastAPI, Request
from pydantic import BaseModel


from dictionary.britannica import (
    get_entries,
    get_total_entries,
    get_word_of_the_day,
    get_parts,
    get_definitions
)

TOKEN = os.environ.get("TOKEN")
TELEGRAM_API_BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

app = FastAPI()

@app.get("/britannica/entries/{word}")
async def britannica_entries(word: str):
    entries = get_entries(word)
    return {"entries": entries}

@app.get("/")
def index():
    return {"message": "Hello World"}

