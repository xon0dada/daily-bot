"""
Daily Bot - 新聞模組
"""

import requests

GEMINI_API_KEY = "AIzaSyABqGlwKaKo4lQQ4XYpA_FIUXNU61d9jfs"

def get_news():
    """台灣新聞"""
    prompt = "請用繁體中文列出 5 條 台灣 最重要的最新新聞標題，一行一條"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    try:
        r = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, headers={"Content-Type": "application/json"}, timeout=10)
        data = r.json()
        if "candidates" in data:
            return "📰 " + data["candidates"][0]["content"]["parts"][0]["text"]
    except:
        pass
    return "📰 無法取得新聞"

def get_movies():
    """熱映電影"""
    prompt = "請列出目前台灣熱映中的 5 部電影，一行一條"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    try:
        r = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, headers={"Content-Type": "application/json"}, timeout=10)
        data = r.json()
        if "candidates" in data:
            return "🎬 " + data["candidates"][0]["content"]["parts"][0]["text"]
    except:
        pass
    return "🎬 無法取得電影"

def get_exchange_rate():
    """匯率"""
    prompt = "請列出：1 USD = ? TWD, 1 JPY = ? TWD（只列數字）"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    try:
        r = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, headers={"Content-Type": "application/json"}, timeout=10)
        data = r.json()
        if "candidates" in data:
            return "💱 " + data["candidates"][0]["content"]["parts"][0]["text"]
    except:
        pass
    return "💱 無法取得匯率"