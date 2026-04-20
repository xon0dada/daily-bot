"""
Daily Bot - 每日生活機器人
"""

from flask import Flask, request
import requests
import os
import re

import weather, news, stock, ledger

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8600380320:AAHBbr2uddoa96AZQNhcE-2kJB3U4poN7j8")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyABqGlwKaKo4lQQ4XYpA_FIUXNU61d9jfs")

history = {}

def send(chat_id, text):
    try:
        requests.post(f"{API_URL}/sendMessage", json={"chat_id": chat_id, "text": text}, timeout=10)
    except:
        pass

def ai(prompt, user_id):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    ctx = ""
    if user_id in history:
        ctx = "\n".join(history[user_id][-6:])
    payload = {"contents": [{"parts": [{"text": f"你是LINE風格的台灣助手。\n\n{ctx}\nUser: {prompt}\n回覆："}]}]}
    try:
        r = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=15)
        data = r.json()
        if "candidates" in data:
            resp = data["candidates"][0]["content"]["parts"][0]["text"]
            if user_id not in history:
                history[user_id] = []
            history[user_id].extend([f"User: {prompt}", f"Bot: {resp}"])
            if len(history[user_id]) > 10:
                history[user_id] = history[user_id][-10:]
            return resp
    except:
        pass
    return "👀"

def handle(chat_id, text, user_id):
    t = text.lower()
    
    # 選單
    if "選單" in text or "/start" in text:
        send(chat_id, "📋 功能\n\n🌤 天氣\n📅 天氣預報\n📰 新聞\n🎬 電影\n💱 匯率\n📈 股市\n💰 收入 500\n💸 支出 300\n📊 餘額\n📝 記錄\n📂 分類")
    
    # 天氣
    elif "天氣預報" in text:
        send(chat_id, weather.get_weather_forecast())
    elif "天氣" in text:
        send(chat_id, weather.get_weather())
    
    # 新聞
    elif "電影" in text:
        send(chat_id, news.get_movies())
    elif "匯率" in text:
        send(chat_id, news.get_exchange_rate())
    elif "新聞" in text:
        send(chat_id, news.get_news())
    
    # 股市
    elif "股市" in text:
        m = re.search(r'(\d{4,6})', text)
        send(chat_id, stock.get_stock(m.group(1) if m else "2330"))
    
    # 記帳
    elif "收入" in text and re.search(r'\d+', text):
        m = re.search(r'(\d+)', text)
        note = re.sub(r'\d+', '', text.replace("收入", "")).strip()
        send(chat_id, ledger.add_income(int(m.group(1)), note if note else "-")
    
    elif "支出" in text and re.search(r'\d+', text):
        m = re.search(r'(\d+)', text)
        cat = "📦 其他"
        for c in ["餐飲", "交通", "購物", "娛樂", "醫療", "房租", "投資", "電話", "電費", "3C", "服飾", "旅遊", "學習", "寵物"]:
            if c in text:
                cat = c
                break
        note = re.sub(r'\d+', '', text.replace("支出", "")).strip() or "-"
        send(chat_id, ledger.add_expense(int(m.group(1)), cat, note))
    
    elif "餘額" in text:
        send(chat_id, ledger.get_balance())
    elif "記錄" in text:
        send(chat_id, ledger.get_records())
    elif "分類" in text:
        send(chat_id, ledger.get_categories())
    elif "清除" in text:
        send(chat_id, ledger.clear_records())
    
    # AI
    else:
        send(chat_id, "🤔 讓我想想...")
        send(chat_id, ai(text, user_id))

@app.route("/", methods=["POST"])
def webhook():
    try:
        update = request.get_json()
        if "message" in update:
            handle(update["message"]["chat"]["id"], update["message"].get("text", ""), str(update["message"]["chat"]["id"]))
    except:
        pass
    return "OK"

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)