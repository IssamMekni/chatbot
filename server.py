from flask import Flask, request, jsonify, render_template
import csv
import os
from dotenv import load_dotenv
from google import genai

# تحميل المتغيرات من ملف .env
load_dotenv()

# إنشاء عميل genai
client = genai.Client(api_key=os.getenv("API_KEY"))

app = Flask(__name__)

# تحميل معلومات الموقع من ملف CSV
def load_site_info(site_name):
    try:
        with open("algeria_tourist_places_all_cities.csv", newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if site_name.lower() in row["Name"].lower():
                    return row
    except FileNotFoundError:
        print("⚠️ ملف CSV غير موجود. الرجاء التحقق من مساره.")
    return None

# بناء النص التوجيهي
def build_prompt(site, question):
    return f"""
أنت مساعد ذكي متعدد اللغات ومهتم بحماية البيئة.

🔹 اسم الموقع: {site['Name']}
🔹 نوعه: {site['Type']}
🔹 المدينة: {site['City']}
🔹 الجهة: {site['Region']}
🔹 الإحداثيات: {site['Latitude']}, {site['Longitude']}

السؤال من الزائر: "{question}"

أجب باللغة العربية بطريقة تعليمية ومحفزة حول أهمية هذا الموقع الطبيعي.
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"response": "⚠️ الرجاء إدخال اسم الموقع."})

    site_info = load_site_info(user_input)
    if not site_info:
        return jsonify({"response": "⚠️ لم أتمكن من العثور على هذا الموقع. حاول مرة أخرى باسم مختلف."})

    prompt = build_prompt(site_info, user_input)

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        return jsonify({"response": response.text})
    except Exception as e:
        print("❌ خطأ:", e)
        return jsonify({"response": "حدث خطأ أثناء توليد الإجابة. الرجاء المحاولة لاحقًا."})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
