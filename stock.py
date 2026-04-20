"""
Daily Bot - 股市模組
"""

import requests

GEMINI_API_KEY = "AIzaSyABqGlwKaKo4lQQ4XYpA_FIUXNU61d9jfs"

TOP_STOCKS = ["2330", "2317", "2303", "2454", "2412", "2885", "2891", "2884", "2883", "2002"]

def get_stock(symbol="2330"):
    """個股股價"""
    try:
        url = f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=&stockNo={symbol}"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).json()
        data = r.get("data", [])
        if data:
            latest = data[-1]
            name = r.get("title", symbol)
            return f"📈 {name}\n收盤: {latest[6]}\n漲跌: {latest[7]}\n成交量: {latest[8]}"
    except:
        pass
    return f"📈 無法取得 {symbol} 資料"

def get_top10():
    """熱門股票"""
    try:
        url = "https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=" + "|".join([f"tse_{s}.tw" for s in TOP_STOCKS]) + "&json=1&delay=0"
        r = requests.get(url).json()
        stocks = r.get("msgArray", [])
        result = "📈 熱門股票 Top 10\n\n"
        for i, s in enumerate(stocks[:10], 1):
            result += f"{i}. {s.get('c', '')} {s.get('n', '')} - {s.get('z', s.get('p', 'N/A'))}\n"
        return result
    except:
        return "📈 無法取得資料"

def get_stock_news():
    """股市新聞"""
    prompt = "請列出 5 條 台灣股市 最新新聞標題，一行一條"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    try:
        r = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, headers={"Content-Type": "application/json"}, timeout=10)
        data = r.json()
        if "candidates" in data:
            return "📈 " + data["candidates"][0]["content"]["parts"][0]["text"]
    except:
        pass
    return "📈 無法取得新聞"