"""
Telegram 天氣機器人主程式
功能：
- 天氣查詢
- 新聞查詢
- 股市查詢
- 股市新聞
- 熱門股票
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

def get_updates(offset):
    """
    取得 Telegram 更新
    offset: 從哪個訊息開始讀取
    """
    return requests.get(f"{API_URL}/getUpdates", params={"offset": offset}).json()

def send_message(chat_id, text):
    """
    發送訊息到 Telegram
    chat_id: 對話 ID
    text: 訊息內容
    """
    requests.post(f"{API_URL}/sendMessage", json={"chat_id": chat_id, "text": text})

print("🤖 Bot 啟動中... 按 Ctrl+C 停止")

# 記錄讀取到的最後一個訊息 ID
offset = None

# 主迴圈 - 不斷檢查新訊息
while True:
    try:
        # 取得新訊息
        updates = get_updates(offset)
        
        if updates["ok"]:
            # 處理每個訊息
            for result in updates["result"]:
                # 更新 offset，避免重複處理
                offset = result["update_id"] + 1
                
                # 檢查是否是訊息
                if "message" in result:
                    chat_id = result["message"]["chat"]["id"]
                    text = result["message"]["text"]
                    
                    # 根據關鍵字回覆
                    if "天氣" in text:
                        send_message(chat_id, weather.get_weather())
                        
                    elif "新聞" in text:
                        send_message(chat_id, news.get_news())
                        
                    elif "股市" in text or "股票" in text:
                        # 檢查是否有股票代碼
                        import re
                        match = re.search(r'(\d{4,6})', text)
                        symbol = match.group(1) if match else "2330"
                        send_message(chat_id, stock.get_stock(symbol))
                        
                    elif "熱門" in text or "TOP" in text.upper():
                        send_message(chat_id, stock.get_top50())
                    
                    elif "股市新聞" in text or "股 news" in text.lower():
                        send_message(chat_id, stock.get_stock_news())
                        
                    else:
                        # 未知指令，回覆說明
                        send_message(chat_id, "📋 可用指令：\n• 天氣 - 查詢天氣\n• 新聞 - 查詢新聞\n• 股市 - 查詢台積電\n• 股市 2330 - 查詢個股\n• 熱門 - 熱門股票\n• 股市新聞 - 股市新聞")
        
        # 停 1 秒，避免佔用太多資源
        time.sleep(1)
        
    except KeyboardInterrupt:
        # 使用者按 Ctrl+C 停止
        break