
from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "7979262260:AAGIlPy2bx8Vn1GGurY0Tox8YMze5Z9iAZE"
CHAT_ID = "2111124289"
MAS40APM_API_URL = "https://mas40apm-web-hook.onrender.com/analyze"

@app.route('/', methods=['POST'])
def telegram_webhook():
    data = request.json

    if 'message' in data and 'photo' in data['message']:
        chat_id = data['message']['chat']['id']
        file_id = data['message']['photo'][-1]['file_id']

        file_path = get_file_path(file_id)
        if file_path:
            image_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
            image_path = download_image(image_url)
            report = analyze_image(image_path)
            send_message(chat_id, report)

    return 'OK'

def get_file_path(file_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile"
    response = requests.post(url, data={'file_id': file_id})
    response.raise_for_status()
    file_path = response.json()['result']['file_path']
    return file_path

def download_image(file_url):
    response = requests.get(file_url)
    response.raise_for_status()
    image_path = 'temp_image.png'
    with open(image_path, 'wb') as f:
        f.write(response.content)
    return image_path

def analyze_image(image_path):
    with open(image_path, 'rb') as img_file:
        files = {'image': img_file}
        response = requests.post(MAS40APM_API_URL, files=files)
        response.raise_for_status()
        return response.text

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, data=payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

