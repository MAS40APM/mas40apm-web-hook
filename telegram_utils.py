import requests

# توكن البوت الخاص بك
BOT_TOKEN = "YOUR_BOT_TOKEN"
# معرف المحادثة الخاص بك
CHAT_ID = "YOUR_CHAT_ID"

def send_report_to_telegram(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, data=data)
    return response.json()
