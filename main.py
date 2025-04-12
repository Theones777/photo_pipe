from config import Config
from exceptions import UserNotFoundError
from tg import TGClient

if __name__ == '__main__':
    # region input
    PHOTO_DIR = "photo"
    SOME_USER_INFO = "Theones777"
    # endregion

    tg_client = TGClient(Config.BOT_TOKEN)
    if chat_id := tg_client.get_user_chat_id(f"@{SOME_USER_INFO}"):
        tg_client.send_to_telegram(chat_id, PHOTO_DIR)
    else:
        raise UserNotFoundError()
