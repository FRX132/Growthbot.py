import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_alert(message, image_path=None):
    # Textnachricht senden
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print(f"❌ Fehler beim Senden der Nachricht: {response.text}")

    # Optional: Bild mitsenden
    if image_path:
        photo_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
        with open(image_path, "rb") as img:
            photo_data = {
                "chat_id": TELEGRAM_CHAT_ID
            }
            files = {
                "photo": img
            }
            photo_response = requests.post(photo_url, files=files, data=photo_data)
            if photo_response.status_code != 200:
                print(f"❌ Fehler beim Senden des Bildes: {photo_response.text}")