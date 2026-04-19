"""
天氣模組 - 取得天氣資料
使用 Open-Meteo API (免費不需 Key) + Gemini AI 回答
"""

import requests

# Gemini API Key - 用於 AI 回答
GEMINI_API_KEY = "AIzaSyABqGlwKaKo4lQQ4XYpA_FIUXNU61d9jfs"

def get_weather(lat=25.0330, lon=121.5654):
    """
    取得天氣資料
    lat: 緯度, default=25.0330 (台北)
    lon: 經度, default=121.5654 (台北)
    """
    # Open-Meteo API URL - 免費天氣 API
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
    
    # 發送 HTTP 請求取得 JSON 資料
    r = requests.get(url).json()
    
    # 取出目前天氣資料
    current = r["current_weather"]
    daily = r["daily"]
    
    # 組合成天氣訊息
    temp_min = daily['temperature_2m_min'][0]
    temp_max = daily['temperature_2m_max'][0]
    return f"🌤 台灣台北天氣\n\n目前: {current['temperature']}°C\n風速: {current['windspeed']} km/h\n今天: {temp_min}~{temp_max}°C"

def get_weather_ai(location="台北"):
    """
    用 Gemini AI 回答天氣（更自然）
    location: 地點
    """
    # 問 AI 的問題
    prompt = f"請用繁體中文回覆，只給一句話的天氣描述：{location} 的天氣如何？"
    
    # Gemini API URL
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    
    # POST 請求需要 JSON 格式
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    
    try:
        r = requests.post(url, json=payload, headers=headers)
        data = r.json()
        
        # 檢查是否有回應
        if "candidates" in data:
            return "🌤 " + data["candidates"][0]["content"]["parts"][0]["text"]
    except:
        pass
    
    # 如果失敗，改用基本版
    return get_weather()

# 預設位置 (台北)
DEFAULT_LOCATION = (25.0330, 121.5654)

def set_location(lat, lon):
    """
    設定預設位置
    lat: 緯度
    lon: 經度
    """
    global DEFAULT_LOCATION
    DEFAULT_LOCATION = (lat, lon)