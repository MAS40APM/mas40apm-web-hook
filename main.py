from flask import Flask, request
import requests
import os
from datetime import datetime

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = 'YOUR_BOT_TOKEN'
CHAT_ID = '2111124289'
OPENAI_ENDPOINT = 'https://api.openai.com/v1/images'  # ← placeholder، عدل لاحقًا عند تمرير الصورة لـ ChatGPT

def send_message_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': text
    }
    requests.post(url, data=payload)

@app.route('/', methods=['POST'])
def receive_update():
    if request.method == 'POST':
        data = request.get_json()

        if 'message' in data:
            msg = data['message']

            # التأكد من وجود صورة
            if 'photo' in msg:
                file_id = msg['photo'][-1]['file_id']
                caption = msg.get('caption', None)

                if caption is None:
                    # توليد Caption افتراضي
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    caption = f"Frame: M15\nSymbol: XAUUSD\nTime: {timestamp}\nLogID: AUTO-TG"

                # إرسال اللوج كبداية
                send_message_to_telegram(f"📤 Received Image with Caption:\n{caption}")

                # في هذا المكان يتم تمرير الصورة لتحليل MAS40APM لاحقًا (عند توفر endpoint أو آلية داخلية)

                return {'status': 'Image received and caption sent'}, 200

        return {'status': 'No image found'}, 200

    return {'status': 'Method not allowed'}, 405

