from flask import Flask, request
import requests
import os
from datetime import datetime

app = Flask(__name__)

# === إعدادات البوت ===
TELEGRAM_BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'  # ← استبدله بالتوكن الخاص بك
CHAT_ID = '2111124289'  # ← تأكد من أنه صحيح

# === وظيفة إرسال رسالة لوج إلى Telegram ===
def send_message_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': text
    }
    requests.post(url, data=payload)

# === نقطة الاستقبال الرئيسية من Telegram Webhook ===
@app.route('/', methods=['POST'])
def receive_update():
    if request.method == 'POST':
        data = request.get_json()

        if 'message' in data:
            msg = data['message']

            # تأكد من وجود صورة
            if 'photo' in msg:
                file_id = msg['photo'][-1]['file_id']
                caption = msg.get('caption', None)

                # إذا لم توجد Caption → توليد واحدة
                if caption is None:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    caption = f"Frame: M15\nSymbol: XAUUSD\nTime: {timestamp}\nLogID: AUTO-TG"

                # إرسال Caption كـ Log
                send_message_to_telegram(f"📤 Received Image\n\n{caption}")

                # لاحقًا: يمكن هنا تمرير الصورة إلى MAS40APM أو أي API تحليلي

                return {'status': 'Image received and caption sent'}, 200

        return {'status': 'No image found in message'}, 200

    return {'status': 'Method not allowed'}, 405

# === تشغيل السيرفر مع فتح المنفذ المطلوب لـ Render ===
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
