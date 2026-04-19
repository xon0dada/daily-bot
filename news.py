"""
新聞模組 - 取得台灣新聞
使用 Gemini AI 生成新聞摘要
"""

import requests

# Gemini API Key
GEMINI_API_KEY = "AIzaSyABqGlwKaKo4lQQ4XYpA_FIUXNU61d9jfs"

def get_news():
    """
    取得台灣新聞
    透過 Gemini AI 用問題方式取得新聞摘要
    """
    # 問 AI 的問題
    prompt = "請列出 5 條 台灣 重要的最新新聞標題，用繁體中文，一行一條"
    
    # Gemini API URL
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    
    # 組合成 POST 請求格式
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    
    try:
        r = requests.post(url, json=payload, headers=headers)
        data = r.json()
        
        # 取出 AI 回覆
        if "candidates" in data:
            return "📰 " + data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"📰 新聞服務異常"
    
    return "📰 無法取得新聞"

def get_taiwan_news():
    """取得台灣新聞的別名"""
    return get_news()