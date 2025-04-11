import time

from watchdog.events import FileSystemEventHandler

from config import Config
from photo import PhotoClient
from tg import TGClient


class PhotoHandler(FileSystemEventHandler):
    @staticmethod
    def on_created(event):
        if event.is_directory:
            return
        if not event.src_path.lower().endswith(".jpg"):
            return

        print(f"Найден файл: {event.src_path}")
        time.sleep(1)
        try:
            PhotoClient.process_photo(event.src_path, Config.PROCESSED_PATH)
            success = TGClient.send_to_telegram(Config.BOT_TOKEN, Config.CHAT_ID, Config.PROCESSED_PATH)
            if success:
                print("Фото успешно отправлено в Telegram")
            else:
                print("Ошибка отправки в Telegram")
        except Exception as e:
            print(f"Ошибка: {e}")
