from flask import Flask, request, render_template, jsonify
import csv
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")  # تأكد أن ملف .env يحتوي على المفتاح API_KEY
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"

def load_site_info(site_name):
    with open("data.csv", newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if site_name.lower() in row["Name"].lower():
                return row
    return None

def build_prompt(site):
    return f"""
Tu es un assistant écologique multilingue.
Voici des informations sur un site naturel :

Nom : {site['Name']}
Type : {site['Type']}
Ville : {site['City']}
Région : {site['Region']}
Latitude : {site['Latitude']}
Longitude : {site['Longitude']}

Génère un message éducatif et engageant en arabe pour sensibiliser les visiteurs à l'importance écologique de ce site.
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("message")
    site_info = load_site_info(user_input)
    
    if not site_info:
        return jsonify({"response": "لم أتمكن من العثور على هذا الموقع. حاول مرة أخرى باسم مختلف."})

    prompt = build_prompt(site_info)
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    headers = {"Content-Type": "application/json"}
    res = requests.post(GEMINI_URL, json=payload, headers=headers)
    data = res.json()

    response = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
