import os
import requests
from flask import Flask, request

app = Flask(__name__)

# إعداد بيانات البوت
BOT_TOKEN = "7979262260:AAGIlPy2bx8Vn1GGurY0Tox8YMzeSZ9iAZE"
CHAT_ID = "2111124289"
MAS40APM_API_URL = "https://mas40apm-web-hook.onrender.com/analyze"

# نقطة استقبال الصور من تيليجرام
@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    data = request.json

    if 'message' in data and 'photo' in data['message']:
        chat_id = data['message']['chat']['id']
        file_id = data['message']['photo'][-1]['file_id']

        file_path = get_file_path(file_id)
        if file_path:
            image_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
            image_path = download_image(image_url)
            report = analyze_image(image_path)
            send_message(chat_id, report)

    return 'OK'

# === استرجاع رابط الصورة من تيليجرام ===
def get_file_path(file_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
    response = requests.get(url)
    response.raise_for_status()
    result = response.json()
    return result['result']['file_path']

# === تحميل الصورة محليًا ===
def download_image(file_url):
    response = requests.get(file_url)
    response.raise_for_status()
    image_path = 'temp_image.png'
    with open(image_path, 'wb') as f:
        f.write(response.content)
    return image_path

# === إرسال الصورة إلى MAS40APM ===
def analyze_image(image_path):
    with open(image_path, 'rb') as img_file:
        files = {'image': img_file}
        response = requests.post(MAS40APM_API_URL, files=files)
        response.raise_for_status()
        return response.text

# === إرسال الرد إلى المستخدم ===
def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, data=payload)

# تشغيل التطبيق على Render
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
