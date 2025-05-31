import os
import requests
from flask import Flask, request

from analyzer.mas_analyzer import generate_mas40apm_report

BOT_TOKEN = "7979262260:AAGIlPy2bx8Vn1GGurYeTOx8YMze5Z9iAZE"
CHAT_ID = "2111124289"

app = Flask(__name__)

@app.route('/webhook', methods=["POST"])
def telegram_webhook():
    data = request.json
    if 'message' in data and 'photo' in data['message']:
        chat_id = data['message']['chat']['id']
        file_id = data['message']['photo'][-1]['file_id']
        file_path = get_file_path(file_id)

        if file_path:
            image_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
            image_path = download_image(image_url)
            report = generate_mas40apm_report(image_path, frame_override="M15")
            send_message(chat_id, report)
    
    return {"ok": True}

def get_file_path(file_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()['result']['file_path']
    return None

def download_image(url):
    local_path = "latest_chart.png"
    res = requests.get(url)
    with open(local_path, "wb") as f:
        f.write(res.content)
    return local_path

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
