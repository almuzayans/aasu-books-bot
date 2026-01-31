# صورة بايثون خفيفة
FROM python:3.11-slim

# مجلد العمل داخل الحاوية
WORKDIR /app

# نسخ ملف المتطلبات
COPY requirements.txt .

# تثبيت المكتبات
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي ملفات المشروع
COPY . .

# أمر تشغيل البوت
CMD ["python", "aasu_books_bot.py"]
