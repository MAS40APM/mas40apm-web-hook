from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = "7979262260:AAGIlPy2bx8Vn1GGurY0Tox8YMze5Z9iAZE"
CHAT_ID = "2111124289"

# إرسال رسالة إلى تليجرام
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, data=payload)

# تحميل الصورة من تيليجرام
def get_file_path(file_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
    response = requests.get(url)
    response.raise_for_status()
    file_path = response.json()['result']['file_path']
    return file_path

def download_image(file_path):
    url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
    response = requests.get(url)
    response.raise_for_status()
    image_path = 'temp_image.png'
    with open(image_path, 'wb') as f:
        f.write(response.content)
    return image_path

# 🔍 توليد تقرير وهمي يحتوي على 14 فقرة (للاختبار الآن)
def generate_dummy_report():
    return """
📊 MAS40APM - Full Technical Report

1. Trend Analysis:
↳ Uptrend detected on H1 with strong higher lows.

2. Resistance Zones:
↳ 2355.00, 2362.80, 2375.40

3. Support Zones:
↳ 2328.50, 2315.00, 2301.60

4. Execution Opportunities (Buy/Sell Setup):
↳ Possible Buy @2330 with SL 2324 / TP 2354

5. تقييم زخم الشمعة اللحظية:
↳ الزخم الحالي: 78% صعود

6. ارتباط الحركة مع مؤشر الدولار (DXC):
↳ العلاقة عكسية - دعم لحركة الشراء

7. تحليل تأثير الأخبار (MFS):
↳ لا أخبار مؤثرة خلال الساعة القادمة

8. تقييم نسبة المخاطرة:
↳ مخاطرة معتدلة (1.5%)

9. حجم الدخول المقترح:
↳ 0.3 Lot (حساب صغير)

10. نسبة الثقة في الصفقة:
↳ 86%

11. تقييم انعكاس الحركة اللحظي:
↳ لا إشارات انعكاس حتى الآن

12. تحليل الوعي الجمعي (CSE-X):
↳ التجار يتجهون للشراء بنسبة 63%

13. الموقع التنافسي للنظام (CIL):
↳ أداء MAS40 أعلى من متوسط الأنظمة المنافسة بنسبة 21%

14. Executive Summary:
✔️ الدخول متاح، لا توجد إشارات معاكسة قوية
"""

# 📥 Endpoint Webhook من Telegram
@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    data = request.json

    if 'message' in data and 'photo' in data['message']:
        chat_id = data['message']['chat']['id']
        file_id = data['message']['photo'][-1]['file_id']
        
        try:
            file_path = get_file_path(file_id)
            image_path = download_image(file_path)
            report = generate_dummy_report()
            send_message(chat_id, report)
        except Exception as e:
            send_message(chat_id, f"❌ Error: {e}")
    
    return 'OK'

# 🔍 Endpoint لتحليل صورة يدوياً (اختياري)
@app.route('/analyze', methods=['POST'])
def analyze_image():
    if 'image' not in request.files:
        return '❌ No image file provided', 400

    img_file = request.files['image']
    img_file.save('uploaded_image.png')

    # إرسال تقرير وهمي كما في الـ webhook
    report = generate_dummy_report()
    return report

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
