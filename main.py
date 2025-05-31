from flask import Flask, request
import requests

app = Flask(__name__)

# MAS40APM - Full Report (Dummy Test)

BOT_TOKEN = "7979262260:AAGIlPy2bx8Vn1GGurY0Tox8YMze5Z9iAZE"
CHAT_ID = "2111124289"

@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    data = request.json
    if 'message' in data and 'photo' in data['message']:
        chat_id = data['message']['chat']['id']
        send_message(chat_id, "✅ Image received and processed by MAS40APM\n\n📊 Dummy Test Report:\n\n1. Trend Analysis\n2. Resistance Zones\n3. Support Zones\n4. Execution Opportunities\n5. Momentum Snapshot\n6. DXY Correlation\n7. News Impact\n8. Risk Level\n9. Lot Size Suggestion\n10. Confidence Score\n11. Reversal Evaluation\n12. Crowd Sentiment\n13. System Benchmark\n14. Summary")
    return "OK"

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    requests.post(url, data=payload)

if __name__ == '__main__':
    import os
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
