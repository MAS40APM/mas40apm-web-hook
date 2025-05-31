from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = "7979262260:AAGIlPy2bx8Vn1GGurY0Tox8YMze5Z9iAZE"
CHAT_ID = "2111124289"

# وحدة تحليل الصورة (Dummy Placeholder – استبدلها بالتحليل الحقيقي مستقبلاً)
def analyze_image(image_path):
    # التحليل الحقيقي يجري هنا لاحقًا
    return "✅ MAS40APM - Full Report Engine\n\n✔️ Image received and processed successfully."

# إرسال النتيجة إلى تليجرام
def send_message(chat_id, message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    requests.post(url, json=payload)

# جلب رابط ملف الصورة من تليجرام
def get_file_path(file_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
    response = requests.get(url)
    response.raise_for_status()
    result = response.json()
    return result['result']['file_path']

# تحميل الصورة إلى مجلد مؤقت
def download_image(image_url):
    image_path = "received_image.png"
    response = requests.get(image_url)
    with open(image_path, 'wb') as f:
        f.write(response.content)
    return image_path

# نقطة دخول Webhook
@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    data = request.json
    if 'message' in data and 'photo' in data['message']:
        chat_id = data['message']['chat']['id']
        file_id = data['message']['photo'][-1]['file_id']
        try:
            file_path = get_file_path(file_id)
            image_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
            image_path = download_image(image_url)
            report = analyze_image(image_path)
            send_message(chat_id, report)
        except Exception as e:
            send_message(chat_id, f"❌ Error: {str(e)}")
    return 'OK'

# نقطة اختبار يدوية لإرسال الصورة محليًا
@app.route('/analyze', methods=['POST'])
def analyze_local():
    if 'image' not in request.files:
        return 'No image provided', 400
    image_file = request.files['image']
    image_path = "received_image.png"
    image_file.save(image_path)
    report = analyze_image(image_path)
    return report

# تشغيل السيرفر
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
