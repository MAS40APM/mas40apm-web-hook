from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "ضع التوكن الخاص بك هنا"
CHAT_ID = "ضع الـ Chat ID هنا"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, text):
    requests.post(f"{API_URL}/sendMessage", data={
        "chat_id": chat_id,
        "text": text
    })

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print("📥 Webhook received JSON:\n", data)

    if 'message' in data and ('photo' in data['message'] or 'document' in data['message']):
        chat_id = data['message']['chat']['id']

        # استخراج file_id من photo أو document
        if 'photo' in data['message']:
            file_list = data['message']['photo']
            file_id = file_list[-1]['file_id']
        else:
            file_id = data['message']['document']['file_id']

        # استرجاع مسار الصورة
        file_info = requests.get(f"{API_URL}/getFile?file_id={file_id}").json()
        file_path = file_info['result']['file_path']
        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

        print(f"📷 تم استقبال صورة جديدة: {file_url}")

        # إنشاء تقرير تجريبي ثابت (Placeholder)
        report = f"""
MAS40APM Report
Frame: M15
Level: 3295
Mode: Live

1. Trend Analysis: Bullish tendency forming
2. Resistance Zones: 3300 – 3307
3. Support Zones: 3287 – 3290
4. Execution Setup: Buy above 3296.5
5. Momentum Score: 71%
6. DXC Impact: Mild
7. MFS News Impact: None
8. Risk Score: 2.3%
9. Suggested Lot: 0.35
10. Confidence: 78%
11. Reversal Probability: Low
12. CSE-X: 65%
13. Global AI Rank: Moderate Advantage
14. Summary: Confirm buy if candle closes above 3296.5

📊 [Chart Image]({file_url})
"""

        send_message(chat_id, report.strip())
        return "OK", 200

    print("📭 Received non-photo/document message or malformed payload.")
    return "Ignored", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
