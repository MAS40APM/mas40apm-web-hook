import os
import requests
from flask import Flask, request
from analyzer.mas_analyzer import generate_mas40apm_report

# إعدادات بوت تيليجرام
BOT_TOKEN = "7979262260:AAGIlPy2bx8Vn1GGurYeTOx8YMze5Z9iAZE"
CHAT_ID = "2111124289"

app = Flask(__name__)

# نقطة الاستقبال من تيليجرام
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
            report = generate_mas40apm_report(image_path)
            send_message(chat_id, report)

    return "OK"

# الحصول على مسار الصورة
def get_file_path(file_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['result']['file_path']
    return None

# تنزيل الصورة محليًا
def download_image(url):
    response = requests.get(url)
    path = os.path.join("downloaded", "chart.png")
    os.makedirs("downloaded", exist_ok=True)
    with open(path, 'wb') as f:
        f.write(response.content)
    return path

# إرسال الرسالة إلى تيليجرام
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, data=payload)

# تشغيل السيرفر بشكل متوافق مع Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
