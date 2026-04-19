import requests

GEMINI_API_KEY = "AIzaSyABqGlwKaKo4lQQ4XYpA_FIUXNU61d9jfs"

def get_news():
    prompt = "請列出 5 條 台灣 重要的最新新聞標題，用繁體中文，一行一條"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    try:
        r = requests.post(url, json=payload, headers=headers)
        data = r.json()
        if "candidates" in data:
            return "📰 " + data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"📰 新聞服務異常"
    return "📰 無法取得新聞"

def get_taiwan_news():
    return get_news()