from os import getenv

from dotenv import load_dotenv

load_dotenv()


class Config:
    BOT_TOKEN = getenv("BOT_TOKEN")
    JSON_NAME = "chat_ids.json"