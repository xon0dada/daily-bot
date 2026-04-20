"""
Telegram 智能機器人 - Web版 for Render
"""

from flask import Flask, request
import requests
import time
import os
import json
import re

import weather
import news_module
import stock
import ledger

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8600380320:AAHBbr2uddoa96AZQNhcE-2kJB3U4poN7j8")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyABqGlwKaKo4lQQ4XYpA_FIUXNU61d9jfs")

conversation_history = {}

def send_message(chat_id, text):
    try:
        requests.post(f"{API_URL}/sendMessage", json={"chat_id": chat_id, "text": text}, timeout=10)
    except:
        pass

def get_ai_response(prompt, user_id):
    history = conversation_history.get(user_id, [])
    context = ""
    if history:
        recent = history[-6:]
        for i in range(0, len(recent), 2):
            if i < len(recent):
                context += f"User: {recent[i]}\n"
            if i+1 < len(recent):
                context += f"You: {recent[i+1]}\n"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    full_prompt = f"""你是我的好朋友，我們在LINE上面聊天用。

{context}
對方說：{prompt}

請用輕鬆、自然、口語化的方式回覆，就像朋友聊天一樣。
"""
    payload = {"contents": [{"parts": [{"text": full_prompt}]}]}
    headers = {"Content-Type": "application/json"}
    
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=15)
        data = r.json()
        if "candidates" in data:
            response = data["candidates"][0]["content"]["parts"][0]["text"]
            if user_id not in conversation_history:
                conversation_history[user_id] = []
            conversation_history[user_id].extend([prompt, response])
            if len(conversation_history[user_id]) > 20:
                conversation_history[user_id] = conversation_history[user_id][-20:]
            return response
    except:
        pass
    return "👀 讓我想想..."

def handle_message(chat_id, text, user_id):
    text_lower = text.lower()
    
    if "選單" in text or "功能" in text or "/start" in text:
        send_message(chat_id, "📋 選單功能：\n\n🌤 天氣\n📅 天氣預報\n📰 新聞\n🎬 電影\n💱 匯率\n📈 股市\n💰 收入 500\n💸 支出 300\n📊 餘額\n📝 記錄")
    
    elif "天氣預報" in text:
        send_message(chat_id, weather.get_weather_forecast())
    elif "天氣" in text:
        send_message(chat_id, weather.get_weather())
    
    elif "收入" in text and re.search(r'\d+', text):
        match = re.search(r'(\d+)', text)
        amount = int(match.group(1))
        note = re.sub(r'\d+', '', text.replace("收入", "")).strip()
        send_message(chat_id, ledger.add_income(amount, note))
    
    elif "支出" in text and re.search(r'\d+', text):
        match = re.search(r'(\d+)', text)
        amount = int(match.group(1))
        cats = {"餐飲": "🍔 餐飲", "交通": "🚗 交通", "購物": "🛒 購物", "娛樂": "🎬 娛樂", "醫療": "🏥 醫療", "房租": "🏠 房租", "投資": "💰 投資"}
        category = "📦 其他"
        for cat in cats:
            if cat in text:
                category = cats[cat]
                break
        note = re.sub(r'\d+', '', text.replace("支出", "")).strip()
        send_message(chat_id, ledger.add_expense(amount, category, note if note else "-"))
    
    elif "餘額" in text:
        send_message(chat_id, ledger.get_balance())
    elif "記錄" in text:
        send_message(chat_id, ledger.get_records())
    elif "分類" in text:
        send_message(chat_id, ledger.get_categories())
    elif "清除" in text:
        send_message(chat_id, ledger.clear_records())
    elif "股市" in text:
        symbol = re.search(r'(\d{4,6})', text)
        symbol = symbol.group(1) if symbol else "2330"
        send_message(chat_id, stock.get_stock(symbol))
    elif "新聞" in text:
        send_message(chat_id, news_module.get_news())
    elif "電影" in text:
        send_message(chat_id, news_module.get_movies())
    elif "匯率" in text:
        send_message(chat_id, news_module.get_exchange_rate())
    
    else:
        send_message(chat_id, "🤔 讓我想一下...")
        response = get_ai_response(text, user_id)
        send_message(chat_id, response)

@app.route("/", methods=["POST"])
def webhook():
    try:
        update = request.get_json()
        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            user_id = str(chat_id)
            text = update["message"].get("text", "")
            handle_message(chat_id, text, user_id)
    except:
        pass
    return "OK"

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)