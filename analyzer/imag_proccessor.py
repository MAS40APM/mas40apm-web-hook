from datetime import datetime

def extract_chart_data(image):
    # سيتم لاحقًا استخدام نموذج ذكي لاستخراج البيانات من الصورة
    # حالياً نستخدم بيانات ثابتة لأغراض الاختبار
    return {
        "frame": "M15",
        "price": "3315.72",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
