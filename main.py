
from flask import Flask, request
from PIL import Image
import os
import io
from analyzer.mas_analyzer import generate_mas40apm_report

app = Flask(__name__)

UPLOAD_FOLDER = "received"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/analyze", methods=["POST"])
def analyze_image():
    if "photo" not in request.files:
        return "❌ No image uploaded", 400

    photo = request.files["photo"]
    filename = os.path.join(UPLOAD_FOLDER, "chart.png")
    photo.save(filename)

    # 👇 مؤقتًا: تعيين الفريم يدويًا لأن pytesseract غير مفعّل
    frame = "M15"

    try:
        image = Image.open(filename)
        report = generate_mas40apm_report(image=image, frame=frame)
        return report
    except Exception as e:
        return f"❌ Error during analysis: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)
