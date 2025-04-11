import requests


class TGClient:
    @staticmethod
    def send_to_telegram(bot_token, chat_id, photo_path):
        url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
        with open(photo_path, 'rb') as photo:
            files = {'photo': photo}
            data = {'chat_id': chat_id}
            response = requests.post(url, files=files, data=data)
        return response.ok
