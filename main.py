from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "7979262260:AAGIlPy2bx8Vn1GGurY0Tox8YMze5Z9iAZE"
CHAT_ID = "2111124289"

@app.route('/', methods=['POST'])
def webhook():
    data = request.json

    if "message" in data and "photo" in data["message"]:
        file_id = data["message"]["photo"][-1]["file_id"]

        file_info = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}").json()
        file_path = file_info["result"]["file_path"]

        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

        print(f"✅ تم استقبال صورة جديدة: {file_url}")

        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": f"📸 تم استقبال صورة وتحويلها تلقائيًا:\n{file_url}"}
        )

    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
