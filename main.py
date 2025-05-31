import os
import requests
from flask import Flask, request

app = Flask(__name__)

MAS40APM_API_URL = "https://mas40apm-web-hook.onrender.com/analyze"

@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    data = request.json

    if 'message' in data and 'photo' in data['message']:
        chat_id = data['message']['chat']['id']
        file_id = data['message']['photo'][-1]['file_id']
        file_path = get_file_path(file_id)

        if file_path:
            image_url = f"https://api.telegram.org/file/bot{os.getenv('BOT_TOKEN')}/{file_path}"
            image_path = download_image(image_url)
            report = analyze_image(image_path)
            print("✅ MAS40APM Report:\n", report)

    return 'OK'

def get_file_path(file_id):
    url = f"https://api.telegram.org/bot{os.getenv('BOT_TOKEN')}/getFile?file_id={file_id}"
    response = requests.get(url)
    response.raise_for_status()
    result = response.json()
    return result['result']['file_path']

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

if __name__ == '__main__':
    print("🚀 MAS40APM - Full Report Engine (Live)")
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
