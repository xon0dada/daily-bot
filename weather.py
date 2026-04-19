import requests
import os

def get_weather(lat=25.0330, lon=121.5654):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
    r = requests.get(url).json()
    current = r["current_weather"]
    daily = r["daily"]
    return f"🌤 台灣台北天氣\n\n目前: {current['temperature']}°C\n風速: {current['windspeed']} km/h\n\n未來幾天:\n" + "\n".join([f"{daily['time'][i]}: {daily['temperature_2m_min'][i]}~{daily['temperature_2m_max'][i]}°C" for i in range(3)])

WEATHER_API = "open-meteo.com"
DEFAULT_LOCATION = (25.0330, 121.5654)

def set_location(lat, lon):
    global DEFAULT_LOCATION
    DEFAULT_LOCATION = (lat, lon)