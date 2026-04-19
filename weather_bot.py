"""
Telegram 天氣機器人主程式
功能：
- 天氣查詢
- 新聞查詢  
- 股市查詢
- 股市新聞
- 熱門股票
- AI 智慧回答（用 Gemini）
"""

import requests
import time
import os

# 匯入各模組
import weather
import news
import stock

# Telegram Bot Token
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8789469759:AAGIeXhWe9FrG7218TUEvVfK4-I2Z34dg0o")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# Gemini API Key - 讓機器人變聰明
GEMINI_API_KEY = "AIzaSyABqGlwKaKo4lQQ4XYpA_FIUXNU61d9jfs"

def get_ai_response(prompt):
    """
    用 Gemini AI 回答問題
    prompt: 使用者的問題
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    
    # 加入情境，讓 AI 知道它是台灣資訊助手
    full_prompt = f"""你是一個台灣資訊助手，請用繁體中文回答。

使用者問題: {prompt}

如果涉及到投資，請提醒這只是資訊參考，不構成投資建議。
"""
    
    payload = {"contents": [{"parts": [{"text": full_prompt}]}]}
    headers = {"Content-Type": "application/json"}
    
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        data = r.json()
        
        if "candidates" in data:
            return data["candidates"][0]["content"]["parts"][0]["text"]
    except:
        pass
    
    return "抱歉，我無法回答這個問題。"

def get_updates(offset):
    """取得 Telegram 更新"""
    return requests.get(f"{API_URL}/getUpdates", params={"offset": offset}).json()

def send_message(chat_id, text):
    """發送訊息到 Telegram"""
    requests.post(f"{API_URL}/sendMessage", json={"chat_id": chat_id, "text": text})

print("🤖 Bot 啟動中... 按 Ctrl+C 停止")
print("💡 輸入任何問題都可以回答！")

offset = None

while True:
    try:
        updates = get_updates(offset)
        
        if updates["ok"]:
            for result in updates["result"]:
                offset = result["update_id"] + 1
                
                if "message" in result:
                    chat_id = result["message"]["chat"]["id"]
                    text = result["message"]["text"]
                    
                    # 檢查關鍵字，回覆特定功能
                    if "天氣" in text:
                        send_message(chat_id, weather.get_weather())
                        
                    elif "新聞" in text and "股市" not in text:
                        send_message(chat_id, news.get_news())
                        
                    elif "股市" in text or "股票" in text:
                        import re
                        match = re.search(r'(\d{4,6})', text)
                        symbol = match.group(1) if match else "2330"
                        send_message(chat_id, stock.get_stock(symbol))
                        
                    elif "熱門" in text or "TOP" in text.upper():
                        send_message(chat_id, stock.get_top50())
                    
                    elif "股市新聞" in text or "股news" in text.lower():
                        send_message(chat_id, stock.get_stock_news())
                    
                    # 其他問題交給 AI 處理
                    else:
                        send_message(chat_id, "🤔 讓我思考一下...")
                        response = get_ai_response(text)
                        send_message(chat_id, response)
        
        time.sleep(1)
        
    except KeyboardInterrupt:
        break