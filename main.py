from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "7979262260:AAGIlPy2bx8Vn1GGurY0Tox8YMze5Z9iAZE"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, text):
    requests.post(f"{API_URL}/sendMessage", data={
        "chat_id": chat_id,
        "text": text
    })

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    print("✅ تم استقبال طلب POST من Telegram")

    if "message" in data and "photo" in data["message"]:
        print("📩 تم التعرف على صورة داخل الرسالة")

        chat_id = data["message"]["chat"]["id"]
        photo_list = data["message"]["photo"]
        file_id = photo_list[-1]["file_id"]

        # Get file path from Telegram
        file_info = requests.get(f"{API_URL}/getFile?file_id={file_id}").json()

        if "result" in file_info:
            file_path = file_info["result"]["file_path"]
            file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
            print(f"📷 تم استقبال صورة جديدة: {file_url}")

            # MAS40APM Report Placeholder
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

[Chart Image]({file_url})
"""

            send_message(chat_id, report.strip())
        else:
            print("❌ لم يتم العثور على result في رد Telegram:", file_info)

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
