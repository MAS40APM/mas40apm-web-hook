from flask import Flask, request
import requests
import os

app = Flask(__name__)

# --- إعدادات التوكن والشات ID ---
BOT_TOKEN = "7979262260:AAGIlPy2bx8Vn1GGurY0Tox8YMze5Z9iAZE"
CHAT_ID = "2111124289"

# --- مسار التحليل المباشر ---
@app.route('/analyze', methods=['POST'])
def analyze_image():
    if 'image' not in request.files:
        return '❌ No image found', 400

    image_file = request.files['image']
    # تحليل الصورة: حالياً فقط إرجاع تأكيد بسيط
    return "✅ Image received and processed by MAS40APM"

# --- Webhook Telegram ---
@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    data = request.json

    if 'message' in data and 'photo' in data['message']:
        chat_id = data['message']['chat']['id']
        file_id = data['message']['photo'][-1]['file_id']

        file_path = get_file_path(file_id)
        if file_path:
            image_url = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}'
            image_path = download_image(image_url)
            report = analyze_locally(image_path)
            send_message(chat_id, report)

    return 'OK'

# --- جلب المسار من Telegram ---
def get_file_path(file_id):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}'
    response = requests.get(url)
    response.raise_for_status()
    file_path = response.json()['result']['file_path']
    return file_path

# --- تحميل الصورة إلى ملف مؤقت ---
def download_image(url):
    response = requests.get(url)
    response.raise_for_status()
    with open('temp.png', 'wb') as f:
        f.write(response.content)
    return 'temp.png'

# --- تحليل الصورة محلياً (يرسلها إلى /analyze) ---
def analyze_locally(image_path):
    with open(image_path, 'rb') as img_file:
        files = {'image': img_file}
        response = requests.post("https://mas40apm-web-hook.onrender.com/analyze", files=files)
        response.raise_for_status()
        return response.text

# --- إرسال رسالة إلى التليجرام ---
def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, data=payload)

# --- تشغيل التطبيق ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
