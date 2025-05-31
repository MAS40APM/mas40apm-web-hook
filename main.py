from fastapi import FastAPI, UploadFile, File
from analyzer.mas_analyzer import generate_mas40apm_report
from telegram_utils import send_report_to_telegram

import io
from PIL import Image

app = FastAPI()

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # توليد التقرير الكامل من المحرك التحليلي
        report_text = generate_mas40apm_report(image)

        # إرسال التقرير إلى Telegram
        send_report_to_telegram(report_text)

        return {"status": "success", "report": report_text}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
