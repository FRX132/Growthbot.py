import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_alert(message, image_path=None):
    url = f"https://api.telegram.org/bot{7630113729:AAHp9RzzOPsgX56UcSkuHqx_2LB_habpCHQ}/sendMessage"
    data = {
        "chat_id": ,
        "text": message
    }
    requests.post(url, data=data)

    if image_path:
        photo_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
        with open(image_path, "rb") as img:
            requests.post(photo_url, files={"photo": img}, data={"chat_id": TELEGRAM_CHAT_ID})