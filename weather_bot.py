import requests
import json
import time
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8789469759:AAGIeXhWe9FrG7218TUEvVfK4-I2Z34dg0o")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def get_weather(lat=25.0330, lon=121.5654):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
    r = requests.get(url).json()
    current = r["current_weather"]
    daily = r["daily"]
    return f"🌤 台灣台北天氣\n\n目前: {current['temperature']}°C\n風速: {current['windspeed']} km/h\n\n未來幾天:\n" + "\n".join([f"{daily['time'][i]}: {daily['temperature_2m_min'][i]}~{daily['temperature_2m_max'][i]}°C" for i in range(3)])

def get_news():
    try:
        url = "https://newsapi.org/v2/top-headlines?country=tw&apiKey=48b077995ba8419f8f4da5256744b3fd"
        r = requests.get(url).json()
        articles = r.get("articles", [])[:5]
        if not articles:
            return "📰 目前無法取得新聞"
        news = "📰 台灣新聞\n\n"
        for i, a in enumerate(articles, 1):
            news += f"{i}. {a.get('title', '無標題')}\n"
        return news
    except:
        return "📰 新聞服務待設定"

def get_stock(symbol="2330"):
    try:
        url = f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=&stockNo={symbol}"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers).json()
        data = r.get("data", [])
        if data:
            latest = data[-1]
            name = r.get("title", symbol)
            date, cap, turn, open_price, high, low, close, change, vol = latest
            return f"📈 {name}\n收盤: {close}\n漲跌: {change}\n成交量: {vol}"
        return f"📈 {symbol} 無法取得資料"
    except:
        try:
            url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{symbol}.tw&json=1&delay=0"
            r = requests.get(url).json()
            if r.get("msgArray"):
                info = r["msgArray"][0]
                return f"📈 {info.get('n', symbol)} {info.get('c', '')}\n目前: {info.get('p', 'N/A')} TWD"
        except:
            pass
        return "📈 股市服務待設定"

def get_top50():
    try:
        top_stocks = ["2330", "2317", "2303", "2454", "2412", "2885", "2891", "2884", "2883", "2002", "1216", "3008", "2382", "3034", "3673", "6515", "00679B", "0050", "00878", "00940", "2618", "2409", "3481", "2337", "0056", "2474", "2327", "2362", "2308", "2377", "1590", "6703", "3231", "4906", "2405", "6223", "3545", "1805", "1707", "1711", "2481", "2449", "2328", "2105", "1710", "2363", "2027", "4958", "2347", "6285", "8155", "8299"]
        url = "https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=" + "|".join([f"tse_{s}.tw" for s in top_stocks]) + "&json=1&delay=0"
        r = requests.get(url).json()
        stocks = r.get("msgArray", [])
        if not stocks:
            return "📈 無法取得熱門股票資料"
        result = "📈 台灣熱門股票 Top 20\n\n"
        for i, s in enumerate(stocks[:20], 1):
            price = s.get('z', s.get('p', 'N/A'))
            if price == '-':
                price = s.get('p', 'N/A')
            result += f"{i}. {s.get('c', '')} {s.get('n', '')} - {price}\n"
        return result
    except Exception as e:
        return "📈 服務異常，請稍後再試"

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
                        send_message(chat_id, get_weather())
                    elif "新聞" in text:
                        send_message(chat_id, get_news())
                    elif "股市" in text or "股票" in text:
                        import re
                        match = re.search(r'(\d{4,6})', text)
                        symbol = match.group(1) if match else "2330"
                        send_message(chat_id, get_stock(symbol))
                    elif "熱門" in text or "TOP" in text.upper():
                        send_message(chat_id, get_top50())
                    else:
                        send_message(chat_id, "📋 可用指令：\n• 天氣 - 查詢天氣\n• 新聞 - 查詢新聞\n• 股市 - 查詢台積電")
        time.sleep(1)
    except KeyboardInterrupt:
        break