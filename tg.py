import json
import os

import requests
from thefuzz import fuzz

from config import Config


class TGClient:
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.root_url = f"https://api.telegram.org/bot{self.bot_token}"
        self.send_photo_url = f"{self.root_url}/sendPhoto"
        self.get_updates_url = f"{self.root_url}/getUpdates"

    def send_to_telegram(self, chat_id: int, photo_dir: str):
        for photo_file in os.listdir(photo_dir):
            photo_path = os.path.join(photo_dir, photo_file)
            with open(photo_path, 'rb') as photo:
                files = {'photo': photo}
                data = {'chat_id': chat_id}
                response = requests.post(self.send_photo_url, files=files, data=data)
        return response.ok

    @staticmethod
    def _get_message_info(message: dict) -> tuple:
        username = message.get("message", {}).get("from", {}).get("username")

        first_name = message.get("message", {}).get("from", {}).get("first_name")
        last_name = message.get("message", {}).get("from", {}).get("last_name")
        full_name = f"{first_name} {last_name}"

        user_chat_id = message.get("message", {}).get("from", {}).get("id")
        return username, full_name, user_chat_id

    def _read_json(self):
        try:
            with open(Config.JSON_NAME) as f:
                chat_ids = json.load(f)
            return chat_ids
        except FileNotFoundError:
            return self._save_json({})

    @staticmethod
    def _save_json(data):
        with open(Config.JSON_NAME, "w") as f:
            json.dump(data, f)
        return data

    def _get_user_id_from_json(self, user_info: str):
        chat_ids = self._read_json()
        if user_info in chat_ids:
            return chat_ids[user_info]

    def _save_user_id_to_json(self, user_info, user_chat_id):
        chat_ids = self._read_json()
        chat_ids[user_info] = user_chat_id
        self._save_json(chat_ids)

    def get_user_chat_id(self, user_info: str) -> int:
        """ user_info - full name or @username"""
        if user_chat_id := self._get_user_id_from_json(user_info):
            return user_chat_id

        response = requests.get(self.get_updates_url).json()
        for message in response.get("result", [])[::-1]:
            username, full_name, user_chat_id = self._get_message_info(message)

            username_similarity = fuzz.ratio(user_info, username) >= 95
            full_name_similarity = fuzz.ratio(user_info, full_name) >= 95

            if username_similarity or full_name_similarity:
                self._save_user_id_to_json(user_info, user_chat_id)
                return user_chat_id
