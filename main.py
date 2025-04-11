import os
import time
from watchdog.observers import Observer

from config import Config
from handler import PhotoHandler

if __name__ == '__main__':
    os.makedirs(Config.PHOTO_DIR, exist_ok=True)
    observer = Observer()
    observer.schedule(PhotoHandler(), path=Config.PHOTO_DIR, recursive=False)
    observer.start()
    print(f"Ожидание новых фото в папке: {Config.PHOTO_DIR}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
