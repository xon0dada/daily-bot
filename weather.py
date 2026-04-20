"""
Daily Bot - 天氣模組
"""

import requests

GEMINI_API_KEY = "AIzaSyABqGlwKaKo4lQQ4XYpA_FIUXNU61d9jfs"

def get_weather(lat=25.0330, lon=121.5654):
    """取得天氣"""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
    r = requests.get(url).json()
    current = r["current_weather"]
    daily = r["daily"]
    return f"🌤 台灣台北天氣\n\n目前: {current['temperature']}°C\n風速: {current['windspeed']} km/h\n今天: {daily['temperature_2m_min'][0]}~{daily['temperature_2m_max'][0]}°C"

def get_weather_forecast(lat=25.0330, lon=121.5654):
    """天氣預報"""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=auto&forecast_days=7"
    r = requests.get(url).json()
    daily = r.get("daily", {})
    result = "📅 一週天氣\n\n"
    for i in range(7):
        date = daily["time"][i][-5:]
        result += f"{date}: {daily['temperature_2m_min'][i]}~{daily['temperature_2m_max'][i]}°C\n"
    return result

def get_weather_alert():
    """天氣預警"""
    prompt = "請用繁體中文列出目前台灣的天氣預警資訊，如沒有請說「目前無預警」"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    try:
        r = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, headers={"Content-Type": "application/json"}, timeout=10)
        data = r.json()
        if "candidates" in data:
            return "🔔 " + data["candidates"][0]["content"]["parts"][0]["text"]
    except:
        pass
    return "🔔 無法取得預警"