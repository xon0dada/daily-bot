import requests

GEMINI_API_KEY = "AIzaSyABqGlwKaKo4lQQ4XYpA_FIUXNU61d9jfs"

def get_weather(lat=25.0330, lon=121.5654):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
    r = requests.get(url).json()
    current = r["current_weather"]
    daily = r["daily"]
    temp_min = daily['temperature_2m_min'][0]
    temp_max = daily['temperature_2m_max'][0]
    return f"🌤 台灣台北天氣\n\n目前: {current['temperature']}°C\n風速: {current['windspeed']} km/h\n今天: {temp_min}~{temp_max}°C"

def get_weather_ai(location="台北"):
    prompt = f"請用繁體中文回覆，只給一句話的天氣描述：{location} 的天氣如何？"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    try:
        r = requests.post(url, json=payload, headers=headers)
        data = r.json()
        if "candidates" in data:
            return "🌤 " + data["candidates"][0]["content"]["parts"][0]["text"]
    except:
        pass
    return get_weather()

DEFAULT_LOCATION = (25.0330, 121.5654)

def set_location(lat, lon):
    global DEFAULT_LOCATION
    DEFAULT_LOCATION = (lat, lon)