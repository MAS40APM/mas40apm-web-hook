
from flask import Flask, request
import requests
import os

app = Flask(__name__)

# === Configuration ===
BOT_TOKEN = '7979262260:AAGIlPy2bx8Vn1GGurY0Tox8YMze5Z9iAZE'
MAS40APM_API_URL = 'https://mas40apm-openai-endpoint.onrender.com/analyze'  # Replace with actual MAS40APM endpoint

# === Telegram Webhook Endpoint ===
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if 'message' in data and 'photo' in data['message']:
        chat_id = data['message']['chat']['id']
        file_id = data['message']['photo'][-1]['file_id']

        try:
            file_path = get_file_path(file_id)
            file_url = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}'
            image_path = download_image(file_url)
            report = analyze_image(image_path)
            send_message(chat_id, report)
        except Exception as e:
            send_message(chat_id, f'❌ Error: {str(e)}')

    return 'OK'

# === Helper to get file path from Telegram ===
def get_file_path(file_id):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['result']['file_path']

# === Download image to local temp path ===
def download_image(file_url):
    response = requests.get(file_url)
    response.raise_for_status()
    image_path = 'temp_image.png'
    with open(image_path, 'wb') as f:
        f.write(response.content)
    return image_path

# === Call MAS40APM to analyze the image ===
def analyze_image(image_path):
    with open(image_path, 'rb') as img_file:
        files = {'image': img_file}
        response = requests.post(MAS40APM_API_URL, files=files)
        response.raise_for_status()
        return response.text

# === Send message to user ===
def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, data=payload)

if __name__ == '__main__':
    app.run()
