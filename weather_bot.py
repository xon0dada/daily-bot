import requests
import json
import time
import os
import weather
import news
import stock

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8789469759:AAGIeXhWe9FrG7218TUEvVfK4-I2Z34dg0o")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def get_updates(offset):
    return requests.get(f"{API_URL}/getUpdates", params={"offset": offset}).json()

def send_message(chat_id, text):
    requests.post(f"{API_URL}/sendMessage", json={"chat_id": chat_id, "text": text})

print("🤖 Bot 啟動中... 按 Ctrl+C 停止")

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
                    if "天氣" in text:
                        send_message(chat_id, weather.get_weather())
                    elif "新聞" in text:
                        send_message(chat_id, news.get_news())
                    elif "股市" in text or "股票" in text:
                        import re
                        match = re.search(r'(\d{4,6})', text)
                        symbol = match.group(1) if match else "2330"
                        send_message(chat_id, stock.get_stock(symbol))
                    elif "熱門" in text or "TOP" in text.upper():
                        send_message(chat_id, stock.get_top50())
                    else:
                        send_message(chat_id, "📋 可用指令：\n• 天氣 - 查詢天氣\n• 新聞 - 查詢新聞\n• 股市 - 查詢台積電\n• 股市 2330 - 查詢個股\n• 熱門 - 熱門股票")
        time.sleep(1)
    except KeyboardInterrupt:
        break