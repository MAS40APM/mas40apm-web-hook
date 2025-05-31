from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = "7979262260:AAGIlPy2bx8Vn1GGurY0Tox8YMze5Z9iAZE"
CHAT_ID = "2111124289"

# نقطة الدخول الرئيسية للتحليل الكامل
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
            report = analyze_image_full(image_path)
            send_message(chat_id, report)
    return 'OK'

# استرجاع مسار الصورة من Telegram
def get_file_path(file_id):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['result']['file_path']

# تحميل الصورة مؤقتًا
def download_image(file_url):
    response = requests.get(file_url)
    response.raise_for_status()
    image_path = 'temp_image.png'
    with open(image_path, 'wb') as f:
        f.write(response.content)
    return image_path

# المحرك التحليلي الحقيقي (تحليل الصورة من MAS40APM Webhook وتحليل التقرير)
def analyze_image_full(image_path):
    MAS40APM_API_URL = "https://mas40apm-web-hook.onrender.com/analyze"
    with open(image_path, 'rb') as img_file:
        files = {'image': img_file}
        response = requests.post(MAS40APM_API_URL, files=files)
        response.raise_for_status()
        return response.text

# إرسال التقرير إلى المستخدم
def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, data=payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
