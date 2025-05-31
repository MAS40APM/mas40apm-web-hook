from flask import Flask, request
import requests
import os

app = Flask(__name__)

# إعداد المتغيرات
BOT_TOKEN = "7979262260:AAGIlPy2bx8Vn1GGurY0Tox8YMze5Z9iAZE"
CHAT_ID = "2111124289"
MAS40APM_API_URL = "https://mas40apm-web-hook.onrender.com/analyze"

# === استخراج رابط الصورة من Telegram ===
def get_file_path(file_id):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/getFile'
    response = requests.post(url, data={'file_id': file_id})
    response.raise_for_status()
    result = response.json()
    file_path = result['result']['file_path']
    return file_path

# === تحميل الصورة محلياً ===
def download_image(file_path):
    image_url = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}'
    response = requests.get(image_url)
    response.raise_for_status()
    image_path = 'temp_image.png'
    with open(image_path, 'wb') as f:
        f.write(response.content)
    return image_path

# === إرسال الصورة إلى MAS40APM لتحليلها ===
def analyze_image(image_path):
    with open(image_path, 'rb') as img_file:
        files = {'image': img_file}
        response = requests.post(MAS40APM_API_URL, files=files)
        response.raise_for_status()
        return response.text

# === إرسال الرد للمستخدم عبر Telegram ===
def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, data=payload)

# === نقطة استقبال الصور من Telegram ===
@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    data = request.json
    try:
        if 'message' in data and 'photo' in data['message']:
            chat_id = data['message']['chat']['id']
            photo_list = data['message']['photo']
            file_id = photo_list[-1]['file_id']  # أعلى جودة
            file_path = get_file_path(file_id)
            image_path = download_image(file_path)
            report = analyze_image(image_path)
            send_message(chat_id, f"✅ MAS40APM Report:\n\n{report}")
    except Exception as e:
        send_message(CHAT_ID, f"❌ Error: {str(e)}")
    return 'OK'

# === تشغيل التطبيق ===
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
